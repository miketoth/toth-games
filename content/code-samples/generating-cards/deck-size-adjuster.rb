def adjust_deck_size(deckName, saveFileData, cardData)
  stack = []
  stack += saveFileData["ObjectStates"]
  while stack.length > 0 
    item = stack.pop()
    if item["Name"] == "Bag" and !item["ContainedObjects"].nil? then
      stack += item["ContainedObjects"]
    end
    if item["Nickname"] == deckName then
      deckIDs = item["DeckIDs"]
      cards = item["ContainedObjects"]
      item["CustomDeck"].values[0]["NumWidth"] = 10
      item["CustomDeck"].values[0]["NumHeight"] = 1 + (cardData.length / 10)
      # renormalize ids to prevent "double carding". something in the pipeline occasionally
      # re-orders this array. the ids must start wiith XX00 and increment from there to 
      # properly match the uploaded card images
      firstVal = deckIDs[0] / 100 * 100
      cards.each_with_index do |card,index|
        deckIDs.shift()
        deckIDs.push(firstVal+index)
        card["CardID"] = firstVal+index
      end
      while cardData.length > deckIDs.length()
        nextVal = deckIDs[deckIDs.length - 1] + 1
        deckIDs.push(nextVal)

        nextCard = cards[cards.length - 1].clone
        nextCard["CardID"] = nextVal
        nextCard["GUID"] = [*('a'..'z'),*('0'..'9')].shuffle[0,6].join
        cards.push(nextCard)
      end
      while cardData.length < deckIDs.length()
        deckIDs.pop()
        cards.pop()
      end
      cards.each_with_index do |card,index|
        card["Nickname"] = cardData[index]
      end
      return saveFileData
    end
  end
  raise "Deck " + deckName + " not found!"
end
