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
require 'dog-class.rb'

class NokoFetch
    @web_handle
    @@main_db_loc = "data/main.sqlite"

    def web_fetch
        #Check for the Databases
        database_check()
        #Open the page and grab the relevant elements.
        page = Nokogiri::HTML(open("https://www.boulderhumane.org/animals/adoption/dogs")) 
        rows = page.css("div.views-row")
        curr_dog = Dog.new
        #iterate over each of the entries
        for dog in rows
            #attribs = dog.css("div.views-field") #don't need rn but might later
            curr_dog.id = dog.css("div.views-field.views-field-field-pp-animalid-1").css("span.field-content").text.strip.to_i
            curr_dog.name = dog.css("div.views-field.views-field-field-pp-animalname").text.strip
            curr_dog.breed_primary = dog.css("div.views-field.views-field-field-pp-primarybreed").text.strip
            curr_dog.breed_second = dog.css("div.views-field views-field-field-pp-secondarybreed").text.strip
            str_age = dog.css("div.views-field.views-field-field-pp-age").css("span.field-content").text.strip.split
            curr_dog.age = 12*str_age[0].to_i + str_age[2].to_i
            curr_dog.gender = dog.css("div.views-field.views-field-field-pp-gender").css("span.field-content").text.strip
            curr_dog.status= dog.css("div.views-field.views-field-field-pp-splashtitle").text.strip
            curr_dog.intake_time = Time.now.utc.to_i
            #write to database
            curr_dog.store_data(@@main_db_loc)
        end
    end

    def database_check
        #main_db_loc = "data/main.sqlite" #Holds information tied to ID
        #data_db_loc = "data/data.sqlite" #Holds more time/length info

        if !(File.exist?@@main_db_loc)
            puts "Main DB not found. Creating one now..."
            main_db = SQLite3::Database.new(@@main_db_loc)
            main_db.execute("CREATE TABLE dogdata(id, name, breed_primary, breed_secondary, gender, age, status)")
            main_db.execute("CREATE TABLE seconddata(id, time, status)")
        end
    end
end 

