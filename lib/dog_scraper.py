import scrapy

class DogSpider(scrapy.Spider):

    name ='dogspider'
    start_url = ["https://www.boulderhumane.org/animals/adoption/dogs"]

    def parse(self, response):
        rows = response.css("div.views-row")

        for row in rows:
            name = row.css("div.views-field.views-field-field-pp-animalid-1").css("span.field-content").text
            print(name)
