import json
import urllib.request
import time
import psycopg2
from scrapy.crawler import CrawlerRunner
from lib.crawler_runner import MyCrawlerRunner
from lib.dog_scraper import DogSpider
from lib.dog_class import Dog
from klein import Klein

app = Klein()
crawl_runner = CrawlerRunner()
dog_list = []
scrape_in_progress = False
scrape_complete = False
data_url = "https://www.boulderhumane.org/wp-content/plugins/Petpoint-Webservices-2018/pullanimals.php?type=dog"
#db_conn = psycopg2.connect("dbname='dogdata' user='dogdata' host='localhost' password='password'");

##### DB DEBUG BLOCK #####
##try:
##    db_conn = psycopg2.connect("dbname='dogdata' user='dogdata' host='localhost' password='password'");
##    cursor = db_conn.cursor()
##    cursor.execute("INSERT INTO tutorials (name) VALUES ({0})".format("'testname'"))
##    db_conn.commit()
##    db_conn.close
##    cursor.close()
##except Exception as e:
##    print(e)

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
        http = urllib.request.urlopen(data_url) #crawl_runner.crawl(DogSpider, dog_list=dog_list)
        plain = http.read().decode('utf-8') #Fixing the encoding of document to utf8
        #clean terrible formatting from BVHS
        clean_response = plain.replace("\n", "")
        clean_response = plain.replace("\\n", "")
        objects = json.loads(clean_response)
        for obj in objects:
            dog = Dog.emptyDog()
            dog.createFromAdoptableSearch(obj['adoptableSearch'])
            dog.pretty_print()
        #event.addCallback(finished_scrape)
    else:
        print("already scraping")
    return "updated " + str(len(objects)) + " number of entries"

#@app.route('/data/breeds', methods = ['GET'])
#def data(request):
    #Make SQL requests for selected data here

def finished_scrape(d):
    global scrape_in_progress
    global dog_list
    #global db_conn
    print(d)
    #for dog in dog_list:
    #    dog.pretty_print()

    scrape_in_progress = False

#This method needs to read a dog object from a sql db line
def readDog():
    pass

if __name__ == '__main__':
    app.run("localhost", 5000)

    #globalLogBeginner.beginLoggingTo([textFileLogObserver(stdout)])

    #root_resource = wsgi.WSGIResource(reactor, reactor.getThreadPool(), app)
    #factory = server.Site(root_resource)
    #http_server = endpoints.TCP4ServerEndpoint(reactor, 5000)
    #http_server.listen(factory)

    #reactor.run()
