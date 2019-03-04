from scrapy import signals
from scrapy.crawler import CrawlerRunner

class MyCrawlerRunner(CrawlerRunner):
    #An object to run a crawler async

    def crawl(self, crawler_arg, * args, **kwargs):

        #for aggregating crawler items
        self.items = []

        #store the results of scraping
        crawler = self.create_crawler(crawler_arg)

        #aggregate results
        crawler.signals.connect(self.item_scraped)

        #create a deferred launch
        dfd = self._crawl(crawler, *args, **kwargs)

        #callback
        dfd.addCallback(self.return_items)
        return dfd

    def item_scraped(self, item, response, spider):
        self.items.append(item)

    def return_items(self, result):
        return self.items
    
