import unittest
from deck_size import cardsInDiscard,buildADeck,drawCards


class TestDeckSize(unittest.TestCase):
  def test_build_a_deck(self):
    self.assertEqual(len(buildADeck(3)), 18)

  def test_draw_cards(self):
    deck = [1,2,3]
    deck, drawn, discard = drawCards(deck, 3, {2:3})
    self.assertEqual(deck, [])
    self.assertEqual(discard, {2:3})
    self.assertEqual(drawn, [1,2,3])

    deck = [1,2,3]
    deck, drawn, discard = drawCards(deck, 5, {2:3})
    self.assertEqual(deck, [2])
    self.assertEqual(discard, {})
    self.assertEqual(drawn, [1,2,3,2,2])

  def test_cards_in_discard(self):
    self.assertEqual(sum(cardsInDiscard(3, 0, lambda : 0)[1].values()), 0)
    self.assertEqual(sum(cardsInDiscard(3, 2, lambda : 0)[1].values()), 10)
    self.assertEqual(sum(cardsInDiscard(3, 3, lambda : 0)[1].values()), 0)

# Execute all the tests when the file is executed
if __name__ == "__main__":
  unittest.main()
