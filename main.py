from scrapy.crawler import CrawlerRunner
from lib.crawler_runner import MyCrawlerRunner
from lib.dog_scraper import DogSpider
from klein import Klein

app = Klein()
dog_list = []
crawl_runner = CrawlerRunner()

@app.route('/', methods = ['GET'])
def hello_world(request):
    return 'Hello, World!'

@app.route('/update', methods = ['GET'])
def update(request):
    if request.uri != b'/update':
        print(request.uri)
    else:
        print("update request accepted")
        event = crawl_runner.crawl(DogSpider, dog_list=dog_list)
        #event.addCallback(finished_scrape)
    return 'Data, Update'

if __name__ == '__main__':
    app.run("localhost", 5000)

    #globalLogBeginner.beginLoggingTo([textFileLogObserver(stdout)])

    #root_resource = wsgi.WSGIResource(reactor, reactor.getThreadPool(), app)
    #factory = server.Site(root_resource)
    #http_server = endpoints.TCP4ServerEndpoint(reactor, 5000)
    #http_server.listen(factory)

    #reactor.run()
