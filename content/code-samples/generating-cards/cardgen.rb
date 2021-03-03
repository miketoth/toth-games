require 'squib'
require './google-drive-uploader.rb'
require './deck-size-adjuster.rb'
require 'game_icons'
require 'json'

decks = [
{
  "name" => "warrior",
  "uploadTarget" => "1hk8tZMXoBXB9Vdh0koP74iM-UhMBe1sT",
}
]

icon_renames = {
  "bonus1" => GameIcons.get("lorc/broadsword").recolor(fg: 'ff5733', bg: 'FFFFFF').string,
  "bonus2" => GameIcons.get("lorc/checked-shield").recolor(fg: '085429', bg: 'FFFFFF').string,
  "bonus3" => GameIcons.get("lorc/bubbling-flask").recolor(fg: '3b61d1', bg: 'FFFFFF').string,
  "battle_axe" => GameIcons.get("lorc/battle-axe").recolor(fg: '000000', bg: 'FFFFFF').string,
  "shield" => GameIcons.get("willdabeast/round-shield").recolor(fg: '000000', bg: 'FFFFFF').string,
}
saveGameLocation = "./generated_tts_save.json"
saveGameData = JSON.parse(File.read(saveGameLocation))
decks.each do |deck|
  data = Squib.csv file: deck["name"] + '_deck.csv'
  numCards = data["title"].size
  Squib::Deck.new(cards: numCards, layout: %w(hand.yml hand-extension.yml)) do
        background color: :white
        #hint text: '#333' # show outlines for boundary boxes - very handy for developing your layout

        text str: data["title"], layout: "title", color: :black, font: 'Sans bold 18'
        text str: data["description"], layout: "description", color: :black, font: 'Sans 12'
        text str: data["snark"], layout: "snark", color: :black, font: 'Sans italic 8'
        %w(bonus1 bonus2 bonus3).each do |key|
          svg data: data[key].map {|v| icon_renames[key]}, layout: key
          text str: data[key], layout: key + "text", color: :black
        end
        svg data: data["art"].map {|v| icon_renames[v]}, layout: "art"

        if ENV["OUTPUT"] == "printer" then
          save_pdf trim: 37.5, file: deck["name"] + '.pdf', crop_marks: true
        else
          rows = (numCards / 10) + 1
          save_sheet prefix: deck["name"], count_format: '', columns: 10, rows: rows, dir: './_output'
        end
        if ENV["OUTPUT"] == "upload" then
          upload_image('./_output/' + deck["name"] + '.png', deck["uploadTarget"], 'image/png')
          adjust_deck_size(deck["name"] + "_deck", saveGameData, data["title"])
        end
  end
end

File.open(saveGameLocation, "wb") do |f|
  f.write(JSON.pretty_generate(saveGameData))
end
