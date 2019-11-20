import json
import urllib.request
import time
import psycopg2
from scrapy.crawler import CrawlerRunner
from lib.crawler_runner import MyCrawlerRunner
from lib.dog_scraper import DogSpider
from lib.dog_class import Dog
from twisted.internet import defer
from klein import Klein

app = Klein()
crawl_runner = CrawlerRunner()
dog_list = {}
scrape_in_progress = False
scrape_complete = False
data_url = "https://www.boulderhumane.org/wp-content/plugins/Petpoint-Webservices-2018/pullanimals.php?type=dog"
db_conn = psycopg2.connect("dbname='dogdata' user='dogdata' host='localhost' password='mysecretpassword'");

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

def addTag(tag, text):
    return '<{0}>{1}</{0}>'.format(tag, text)

@app.route('/', methods = ['GET'])
@defer.inlineCallbacks
def hello_world(request): 
    global D 
    D = defer.Deferred()
    #text = 'This is a Hello World coroutine function'
    #result = yield heartBeat()
    result = yield addTag('i', "HELLO WORLD") #setHeader(request, 'GET', 'application/json')
    result = yield addTag('html', result)
    request.setHeader('Test-Header', 'this is a value')
    setCorsHeaders(request)
    return result

@app.route('/update', methods = ['GET'])
def update(request):
    global scrape_in_progress
    global scrape_complete
    if not scrape_in_progress:
        #scrape_in_progress = True

        #Load the list of previously available dogs
        global dog_list
        cursor = db_conn.cursor()
        cursor.execute("SELECT * FROM dogs WHERE out_time is NULL")
        rows = cursor.fetchall()
        print(len(rows))
        for row in rows: 
            dog = Dog.emptyDog()
            dog.createFromDbRow(row)
            dog_list[dog.h_id] = dog

        #Get the data from BVHS
        http = urllib.request.urlopen(data_url) #crawl_runner.crawl(DogSpider, dog_list=dog_list)
        plain = http.read().decode('utf-8') #Fixing the encoding of document to utf8
        clean_response = plain.replace("\\n", "").replace("[\"      \"]", "null")
        objects = json.loads(clean_response)
        for obj in objects:
            dog = Dog.emptyDog()
            dog.createFromAdoptableSearch(obj['adoptableSearch'])
            if dog.h_id in dog_list:
                dog_list[dog.h_id] = None
            dog.updateInDb(db_conn)

        #Add out time of now to any dogs that are no longer in the shelter
        for k, val in dog_list.items():
            if val is not None:
                print(val.name)
                val.setOutTime()
                val.updateInDb(db_conn)
        #event.addCallback(finished_scrape)
        return "updated " + str(len(objects)) + " entries"
    else:
        print("already scraping")
        return "The server is currently busy"

@app.route('/data/breeds', methods = ['GET'])
def data(request):
    #Make SQL requests for selected data here
    labels = []
    data = []
    cursor = db_conn.cursor()
    cursor.execute("SELECT breed_primary, COUNT(*) FROM dogs GROUP BY breed_primary")
    rows = cursor.fetchall()
    for row in rows:
        labels.append(row[0])
        data.append(row[1])
    setCorsHeaders(request)
    request.setHeader('Content-Type', 'application/json')
    response = json.dumps({"labels": labels, "data": data})
    return response

#Function to heartbeat
#def heartBeat():
#    return 'The dogged-data appliction is up and running\n'

#Function to establish a deferred with proper headers
def setCorsHeaders(request):
    request.setHeader('Access-Control-Allow-Origin', '*')
    request.setHeader('Access-Control-Allow-Methods', '*')
    request.setHeader('Access-Control-Allow-Headers', '*')

#Function to 

def finished_scrape(d):
    global scrape_in_progress
    global dog_list
    #global db_conn
    print(d)
    #for dog in dog_list:
    #    dog.pretty_print()

    scrape_in_progress = False

if __name__ == '__main__':
    app.run("0.0.0.0", 5000)

    #globalLogBeginner.beginLoggingTo([textFileLogObserver(stdout)])

    #root_resource = wsgi.WSGIResource(reactor, reactor.getThreadPool(), app)
    #factory = server.Site(root_resource)
    #http_server = endpoints.TCP4ServerEndpoint(reactor, 5000)
    #http_server.listen(factory)

    #reactor.run()
