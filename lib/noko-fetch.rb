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
require 'sqlite3'
require 'time'

class NokoFetch
    @web_handle;
    
    def web_fetch
        #Check for the Databases
        database_check()
        #Open the page and grab the relevant elements.
        page = Nokogiri::HTML(open("https://www.boulderhumane.org/animals/adoption/dogs")) 
        rows = page.css("div.views-row")
        
        #iterate over each of the entries
        for dog in rows
            attribs = dog.css("div.views-field") #don't need rn but might later
            id = dog.css("div.views-field.views-field-field-pp-animalid-1").css("span.field-content").text.strip.to_i
            name = dog.css("div.views-field.views-field-field-pp-animalname").text.strip
            breed1 = dog.css("div.views-field.views-field-field-pp-primarybreed").text.strip
            breed2 = dog.css("div.views-field views-field-field-pp-secondarybreed").text.strip
            age = dog.css("div.views-field.views-field-field-pp-age").css("span.field-content").text.strip
            gender = dog.css("div.views-field.views-field-field-pp-gender").css("span.field-content").text.strip
            availability = dog.css("div.views-field.views-field-field-pp-splashtitle").text.strip
            time = Time.now.utc
        end
    end

    def database_check
        main_db_loc = "data/main.sqlite" #Holds information tied to ID
        data_db_loc = "data/data.sqlite" #Holds more time/length info

        if !(File.exists?main_db_loc)
            puts "Main DB not found. Creating one now..."
            main_db = SQLite3::Database.new(main_db_loc)
        end
        
        if !(File.exists?data_db_loc)
            puts "Data DB not found. Creating one now..."
            data_db = SQLite3::Database.new(data_db_loc)
        end
    end
end 

