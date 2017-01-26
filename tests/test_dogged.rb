require "./lib/dogged-data.rb"
require "./lib/noko-fetch.rb"
require "test/unit"

class DoggedTest < Test::Unit::TestCase

    def test_sample
        noko = NokoFetch.new
        noko.web_fetch
    end

end
