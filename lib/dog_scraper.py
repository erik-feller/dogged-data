import scrapy

class DogSpider(scrapy.Spider):

    name ='dogspider'
    start_urls = ["https://www.boulderhumane.org/animals/adoption/dogs"]

    def parse(self, response):
        rows = response.css("div.views-row")
        count = 0;

        for row in rows:
            name = row.xpath('div[3]/div/a/text()').get()
            p_breed = row.xpath('div[4]/div/text()').get()
            s_breed = row.xpath('div[5]/div/text()').get()
            str_age = row.xpath('div[6]/span[2]/text()').get().split()
            age = 12*int(str_age[0]) + int(str_age[2])
            gender = row.xpath('div[7]/span[2]/text()').get()
            h_id = row.xpath('div[8]/span[2]/text()').get()
            #name = row.css("div.views-field.views-field-field-pp-animalid-1").css("span.field-content")
            if s_breed == None:
                print(name + " is a " + p_breed + " that is " + str(age) + " months old " + gender)
            else:
                print(name + " is a " + p_breed + ", " + s_breed + " that is " + str(age) + " months old " + gender)
