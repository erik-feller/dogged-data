#!/usr/bin/env ruby
require 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'sqlite3'
require 'time'
require_relative './lib/dog-class.rb'

@main_db_loc='data/main.sqlite'
working_map=Hash.new

@main_db_loc = File.join(File.dirname(__FILE__), "data/main.sqlite")

def web_fetch(db_handle, working_map)
    #Check for the Databases
    database_check()
    #Open the page and grab the relevant elements.
    page = Nokogiri::HTML(open("https://www.boulderhumane.org/animals/adoption/dogs")) 
    rows = page.css("div.views-row")
    #iterate over each of the entries
    for dog in rows
        #attribs = dog.css("div.views-field") #don't need rn but might later
        curr_dog = Dog.new
        curr_dog.id = dog.css("div.views-field.views-field-field-pp-animalid-1").css("span.field-content").text.strip.to_i
        curr_dog.name = dog.css("div.views-field.views-field-field-pp-animalname").text.strip
        curr_dog.breed_primary = dog.css("div.views-field.views-field-field-pp-primarybreed").text.strip
        curr_dog.breed_second = dog.css("div.views-field.views-field-field-pp-secondarybreed").text.strip
        str_age = dog.css("div.views-field.views-field-field-pp-age").css("span.field-content").text.strip.split
        curr_dog.age = 12*str_age[0].to_i + str_age[2].to_i
        curr_dog.gender = dog.css("div.views-field.views-field-field-pp-gender").css("span.field-content").text.strip
        curr_dog.status= dog.css("div.views-field.views-field-field-pp-splashtitle").text.strip
        curr_dog.intake_time = Time.now.utc.to_i
        #write to HM
        working_map[curr_dog.id]=curr_dog
        #write to database
        curr_dog.store_data(db_handle)
    end
end

def database_check
    if !(File.exist?@main_db_loc)
        puts "Main DB not found. Creating one now..."
        main_db = SQLite3::Database.new(@main_db_loc)
        main_db.execute("CREATE TABLE dogdata(id, name, breed_primary, breed_secondary, gender, age, status, in_time, hold_times, out_time)")
    end
end

if !(File.exist?@main_db_loc)
  puts "Main DB not found. Creating one now..."
  main_db = SQLite3::Database.new(@main_db_loc)
  main_db.execute("CREATE TABLE dogdata(id, name, breed_primary, breed_secondary, gender, age, status, in_time, hold_times, out_time)")
end
main_db = SQLite3::Database.new(@main_db_loc)
web_fetch(main_db, working_map)
#Compare the current list of dogs to the dogs that were present last run
main_db.execute("SELECT * FROM dogdata WHERE out_time IS NULL") do |row|
  row_dog = Dog.new
  row_dog.load_data_row(row)
  if !(working_map[row[0]])
    row_dog.set_out_time()
    row_dog.update_data(main_db)
  end
end
#working_map.each do |key, val| 
#end
