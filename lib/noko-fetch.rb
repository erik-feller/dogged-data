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
        page = Nokogiri::HTML(open(https://www.boulderhumane.org/animals/adoption/dogs)) 
        rows = page.css
end 
