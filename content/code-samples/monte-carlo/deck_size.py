import random
import statistics
from collections import defaultdict
import matplotlib.pyplot as plt
import statistics
import numpy as np

NUMBER_OF_UNIQUE_CARDS = 6
HAND_SIZE = 5

def rollADie():
  return random.randint(1,6)

def buildADeck(copiesPerCard):
  result = [x for i in range(copiesPerCard) for x in range(NUMBER_OF_UNIQUE_CARDS)]
  random.shuffle(result)
  return result

def drawCards(deck, numToDraw, discard):
  drawn = []
  if len(deck) < numToDraw:
    drawn = deck
    deck = []
    for card, count in discard.items():
      for _ in range(count):
        deck.append(card)
    random.shuffle(deck)
    discard = defaultdict(int)
  numToTakeFromDeck = numToDraw - len(drawn)
  drawn.extend(deck[:numToTakeFromDeck])
  return (deck[numToTakeFromDeck:], drawn, discard)

def additionalCards():
  r = random.random() * 100
  if r < 20:
    return 0
  if r < 50:
    return 1
  if r < 80:
    return 2
  return 3

def cardsInDiscard(copiesPerCard, roundsElapsed, additionalCards): 
  rounds = 0
  deck = buildADeck(copiesPerCard)
  discard = defaultdict(int)
  deck, hand, discard = drawCards(deck, HAND_SIZE + additionalCards(), discard)
  while rounds < roundsElapsed:
    for i in hand:
      discard[i] += 1
    deck, hand, discard = drawCards(deck, HAND_SIZE + additionalCards(), discard)
    if sum(discard.values()) + len(hand) > copiesPerCard * NUMBER_OF_UNIQUE_CARDS:
      discard = defaultdict(int)
    rounds += 1
  
  return hand, discard

def meanCardsInDiscard(totalRounds, numCopies):
  y = []
  for roundsElapsed in range(totalRounds):
    vals = []
    for i in range(10000):
      vals.append(sum([1 for count in cardsInDiscard(numCopies, roundsElapsed, additionalCards)[1].values() if count == numCopies]))
    y.append(statistics.mean(vals)/NUMBER_OF_UNIQUE_CARDS * 100)

  return y

def graphPercentageInDiscard(numRounds):
  x = range(numRounds)
  plt.title('Percentage of cards with all copies in the discard (draw fuzzed, hand size ' + str(HAND_SIZE) + ')', fontsize=20)
  plt.xlabel('Number of rounds elapsed', fontsize=18)
  plt.ylabel('Percentage of cards with all copies in the discard', fontsize=16)

  sumMeans = []
  for numCopies in [2,3,4,5,6,7]:
    meanCards = meanCardsInDiscard(numRounds, numCopies)
    plt.plot(x, meanCards, label=str(numCopies) + " copies of each card")
    sumMeans.append(max(meanCards))
  print(sumMeans)
  plt.legend(loc="upper left")
  plt.show()

def graphExpectedNumberOfUniqueCardsInHand():
  plt.title('Expected number of unique cards in hand (hand size ' + str(HAND_SIZE) + ')', fontsize=20)
  plt.xlabel('Copies of each card in deck', fontsize=18)
  plt.ylabel('Average number of unique cards in hand', fontsize=16)

  def meanNumberOfUniqueCards(numCopies):
    output = []
    for i in range(10000):
      output.append(len(set(buildADeck(numCopies)[:HAND_SIZE])))
    return output

  numCopies = [2,3,4,5,6,7]
  plt.xticks([2,3,4,5,6,7], numCopies)
  possibilities = [meanNumberOfUniqueCards(n) for n in numCopies]
  print([statistics.mean(n) for n in possibilities])
  plt.errorbar(numCopies, [statistics.mean(n) for n in possibilities], yerr=[statistics.pstdev(n) for n in possibilities], fmt='o', color='black',
             ecolor='lightgray', elinewidth=3)
  plt.show()

def bestFit(x, expectedPercentLost, numUniqueInHand):
  plt.title('Hand size ' + str(HAND_SIZE), fontsize=20)
  plt.xlabel('Copies of each card in deck', fontsize=18)
  plt.ylabel('0 is worst, 1 is best', fontsize=18)

  expectedPercentLost = [1-x for x in normalize(expectedPercentLost)]
  plt.scatter(x,expectedPercentLost)
  plt.plot(x, np.poly1d(np.polyfit(x, expectedPercentLost, 1))(x), label="Max expected percent of options lost")

  numUniqueInHand = normalize(numUniqueInHand)
  plt.scatter(x,numUniqueInHand)
  plt.plot(x, np.poly1d(np.polyfit(x, numUniqueInHand, 1))(x), label="Expected number of unique cards in hand")
  plt.legend(loc="upper left")
  plt.show()

def normalize(y):
  minVal = min(y)
  maxVal = max(y) - minVal
  return [(x - minVal)/maxVal for x in y]

if __name__ == "__main__":
  numRounds = 6
  #graphPercentageInDiscard(numRounds)
  #graphExpectedNumberOfUniqueCardsInHand()
  # best fit with average expected lost options
  #bestFit([2,3,4,5,6,7], [4.629, 3.918, 3.374, 2.734, 3.071, 2.702], [4.0953, 3.9023, 3.8007, 3.7741, 3.7296, 3.7059])
  # best fit with max expected lost options
  bestFit([2,3,4,5,6,7], [7.738, 7.125, 7.245, 10.135, 12.073, 13.048], [4.0953, 3.9023, 3.8007, 3.7741, 3.7296, 3.7059])
