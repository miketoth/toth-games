require 'optparse'

task default: [:generate]

task :generate do
  options = {}
  o = OptionParser.new
  o.banner = "Usage: rake [command] [options]"
  o.on("-o", "--output (digital|printer|upload)", "Select format of generated files. Upload will generate digital files and put them on Drive for TTS", String) { |o| ENV["OUTPUT"] = o}
  o.on_tail("-h", "--help", "Show this message") do
    puts o
    exit 0
  end
  args = o.order!(ARGV) {}
  o.parse!(args)
  load 'cardgen.rb'
  exit 0
end
