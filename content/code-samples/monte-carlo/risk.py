import random
import statistics
import matplotlib.pyplot as plt

def rollADie():
  return random.randint(1,6)

def fightToTheEnd(attackingPieces, defendingPieces): 
  while attackingPieces > 0 and defendingPieces > 0:
    attacks = sorted([rollADie() for i in range(min(attackingPieces, 3))], reverse=True)
    defenses = sorted([rollADie() for i in range(min(defendingPieces, 2))], reverse=True)

    i = 0
    while i < len(attacks) and i < len(defenses):
      if (attacks[i] > defenses[i]):
        defendingPieces -= 1
      else:
        attackingPieces -= 1
      i += 1

  return (attackingPieces, defendingPieces)

def getOutcome(iterations):
  output = []
  for i in range(iterations):
    output.append(fightToTheEnd(30, 20))
  return output

def probOfAttackerWinning(outcome):
  return len([x for x in outcome if x[0] > 0])/len(outcome)


xs = [1, 10, 100, 1000, 10000, 100000]
outcomes = [getOutcome(x) for x in xs]
print("Expected number of attacker pieces remaining: " + str(statistics.mean([x[0] for x in outcomes[-1]])))
print("Expected number of defender pieces remaining: " + str(statistics.mean([x[1] for x in outcomes[-1]])))

print("Probability of the attacker winning: " + str(probOfAttackerWinning(outcomes[-1])))

plt.plot(xs, [probOfAttackerWinning(x) for x in outcomes], label="100")
plt.xscale('log')

plt.title('Attacker winning percentage converges as the number of iterations increases', fontsize=20)
plt.xlabel('Number of iterations (log scale)', fontsize=18)
plt.ylabel('Probability of attacker winning', fontsize=16)

plt.show()
