###############################################################################
#
# noko-fetch.rb
#
# A class to interface with and hold data from webpages collected by nokogiri. 
#
# Erik Feller
# November 8, 2016
#
###############################################################################

require 'rubygems'
require 'nokogiri'
require 'open-uri'

class NokoFetch
    @web_handle;
    
    def web_fetch
        page = Nokogiri::HTML(open("https://www.boulderhumane.org/animals/adoption/dogs")) 
        rows = page.css("div.views-row")
        
        #iterate over each of the entries
        puts rows.size()
        for dog in rows
            attribs = dog.css("div.views-field") #don't need rn but might later
            name = dog.css("div.views-field.views-field-field-pp-animalname").text.strip
            breed1 = dog.css("div.views-field.views-field-field-pp-primarybreed").text.strip
            breed2 = dog.css("div.views-field views-field-field-pp-secondarybreed").text.strip
            age = dog.css("div.views-field.views-field-field-pp-age").css("span.field-content").text.strip
            availability = dog.css("div.views-field.views-field-field-pp-splashtitle").text.strip
        end
    end
end 
