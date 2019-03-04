from scrapy.crawler import CrawlerRunner
from lib import dog_scraper, crawler_runner
from klein import Klein

app = Klein()
dog_list = []

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/update')
def update(request):
    if request.url != "http://127.0.0.1:5000/update":
        abort(404)
    else:
        print("update request accepted")
        #crawl_runner.crawl(DogSpider, dog_list=dog_list)
    return 'Data, Update'

if __name__ == '__main__':
    from sys import stdout
    from twisted.logger import globalLogBeginner, textFileLogObserver
    from twisted.web import server, wsgi
    from twisted.internet import endpoints, reactor

    app.run("localhost", 5000)

    #globalLogBeginner.beginLoggingTo([textFileLogObserver(stdout)])

    #root_resource = wsgi.WSGIResource(reactor, reactor.getThreadPool(), app)
    #factory = server.Site(root_resource)
    #http_server = endpoints.TCP4ServerEndpoint(reactor, 5000)
    #http_server.listen(factory)

    #reactor.run()
