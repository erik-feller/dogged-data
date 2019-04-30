import json
import time
import psycopg2
from scrapy.crawler import CrawlerRunner
from lib.crawler_runner import MyCrawlerRunner
from lib.dog_scraper import DogSpider
from klein import Klein

app = Klein()
crawl_runner = CrawlerRunner()
dog_list = []
scrape_in_progress = False
scrape_complete = False
db_conn = psycopg2.connect("dbname='dogdata' user='dogdata' host='localhost' password='password'");

@app.route('/', methods = ['GET'])
def hello_world(request):
    return 'Hello, World!'

@app.route('/update', methods = ['GET'])
def update(request):
    global scrape_in_progress
    global scrape_complete
    if not scrape_in_progress:
        scrape_in_progress = True
        global dog_list
        event = crawl_runner.crawl(DogSpider, dog_list=dog_list)
        event.addCallback(finished_scrape)
    else:
        print("already scraping")
    return 'Data, Update'

@app.route('/data/breeds', methods = ['GET'])
def data(request):
    #Make SQL requests for selected data here

def finished_scrape(null):
    global scrape_in_progress
    global dog_list
    global db_conn

    if db_conn == None:
        cur = db_conn.cursor()
        cur.execute('SELECT version')
        db_version = cur.fetchone()
        print(db_version)
    else:
        print("DB ERROR")
    for dog in dog_list:
        dog.pretty_print()
    scrape_in_progress = False

if __name__ == '__main__':
    app.run("localhost", 5000)

    #globalLogBeginner.beginLoggingTo([textFileLogObserver(stdout)])

    #root_resource = wsgi.WSGIResource(reactor, reactor.getThreadPool(), app)
    #factory = server.Site(root_resource)
    #http_server = endpoints.TCP4ServerEndpoint(reactor, 5000)
    #http_server.listen(factory)

    #reactor.run()
