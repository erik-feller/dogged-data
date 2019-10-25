import scrapy
import time
from .dog_class import Dog

class DogSpider(scrapy.Spider):

    name ='dogspider'
    start_urls = ["https://www.boulderhumane.org/dogs/"]

    def parse(self, response):
        print("Parsing response")
        print(response)
        rows = response.selector.xpath('//html/body/div[2]/div[3]/div/div/div/div/div/div/div[1]/child::node()')
        print("rows read")
        print(len(rows))
        count = 0;

        #for row in rows:
            #name = row.xpath('div[3]/div/a/text()').get()
            #p_breed = row.xpath('div[4]/div/text()').get()
            #s_breed = row.xpath('div[5]/div/text()').get()
            #Get age as a string, split on spaces, then convert to months
            #str_age = row.xpath('div[6]/span[2]/text()').get().split()
            #age = 12*int(str_age[0]) + int(str_age[2])
            #gender = row.xpath('div[7]/span[2]/text()').get()
            #h_id = row.xpath('div[8]/span[2]/text()').get()
            #time = int(time.time())
            #cur_dog = Dog(0, h_id, name, p_breed, s_breed, age, gender, None, None)
            #self.dog_list.append(cur_dog)
        pass

#
