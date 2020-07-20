import json
import urllib.request
import time
import psycopg2
from psycopg2 import sql
from twisted.internet import defer
from klein import Klein
from lib.dog_class import Dog

app = Klein()
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

        return "updated " + str(len(objects)) + " entries"
    else:
        print("already scraping")
        return "The server is currently busy"

with app.subroute('/data') as app:

    @app.route('/breeds', methods = ['GET'])
    def breed_data(request):
        labels = []
        data = []
        condense = False
        splitage = False
        cursor = db_conn.cursor()

        #Read args and look for condensed data flag
        if len(request.args) > 0:
            for arg in request.args:
                if arg==b'condense' and b'true' in request.args[arg]:
                    condense = True
                if arg==b'split' and b'true' in request.args[arg]:
                    splitage = True

        if condense:
            if splitage:
                puppyData = []
                adolescentData = []
                adultData = []
                seniorData = []
                row = getAgeSplitData(cursor, [])
                #Counts to track the splits for the Other catagory
                puppyCount = row[0]
                adolescentCount = row[1]
                adultCount = row[2]
                seniorCount = row[3]
                cursor.execute("""
                    SELECT breed_primary, COUNT(*) 
                    FROM dogs 
                    GROUP BY breed_primary
                    ORDER BY COUNT(*) DESC
                    LIMIT 9""")
                rows = cursor.fetchall()
                for row in rows:
                    labels.append(row[0])
                    #find a join that can replace this 
                    row = getAgeSplitData(cursor, [[row[0]]])
                    puppyData.append(row[0])
                    puppyCount = puppyCount-row[0]
                    adolescentData.append(row[1])
                    adolescentCount = adolescentCount-row[1]
                    adultData.append(row[2])
                    adultCount = adultCount-row[2]
                    seniorData.append(row[3])
                    seniorCount = seniorCount-row[3]

                #Build final object with aggregated data
                labels.append("Other")
                puppyData.append(puppyCount)
                data.append(puppyData)
                adolescentData.append(adolescentCount)
                data.append(adolescentData)
                adultData.append(adultCount)
                data.append(adultData)
                seniorData.append(seniorCount)
                data.append(seniorData)
                
            else:
                cursor.execute("""
                    SELECT breed_primary, COUNT(*) 
                    FROM dogs 
                    GROUP BY breed_primary
                    ORDER BY COUNT(*) DESC
                    LIMIT 9""")
                rows = cursor.fetchall()
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM dogs""")
                total_count = cursor.fetchone()[0]
                count = 0
                for row in rows:
                    labels.append(row[0])
                    count = count+row[1]
                    data.append(row[1])
                labels.append("Other")
                print(total_count-count)
                data.append((total_count-count))

        else:
            if splitage:
                puppyData = []
                adolescentData = []
                adultData = []
                seniorData = []
                cursor.execute("""
                    SELECT breed_primary, COUNT(*) 
                    FROM dogs 
                    GROUP BY breed_primary
                    ORDER BY COUNT(*) DESC""")
                rows = cursor.fetchall()
                for row in rows:
                    labels.append(row[0])
                    print(row[0])
                    #find a join that can replace this 
                    row = getAgeSplitData(cursor, [[row[0]]])
                    print(row)
                    puppyData.append(row[0])
                    adolescentData.append(row[1])
                    adultData.append(row[2])
                    seniorData.append(row[3])
                data.append(puppyData)
                data.append(adolescentData)
                data.append(adultData)
                data.append(seniorData)
        

            else:
                cursor.execute("""
                    SELECT breed_primary, COUNT(*) 
                    FROM dogs 
                    GROUP BY breed_primary
                    ORDER BY COUNT(*) DESC""")
                rows = cursor.fetchall()
                for row in rows:
                    labels.append(row[0])
                    data.append(row[1])
        
        setCorsHeaders(request)
        request.setHeader('Content-Type', 'application/json')
        response = json.dumps({"labels": labels, "data": data})
        return response

    @app.route('/age', methods = ['GET'])
    def age_data(request):
        labels = ["Puppy", "Adolescent", "Adult", "Senior"]
        data = []
        breeds = []
        cursor = db_conn.cursor()

        if len(request.args) > 0:
            for arg in request.args:
                if arg==b'breed':
                    breeds.append(list(map(lambda x: x.decode("utf-8"),request.args[arg])))

        row = getAgeSplitData(cursor, breeds)

        for i in row:
            data.append(i)
        
        setCorsHeaders(request)
        request.setHeader('Content-Type', 'application/json')
        response = json.dumps({"labels": labels, "data": data})
        return response


    @app.route('/gender', methods = ['GET'])
    def gender_data(request):
        labels = []
        data = []
        breeds = []
        cursor = db_conn.cursor()
        if len(request.args) > 0:
            for arg in request.args:
                if arg==b'breed':
                    breeds.append(list(map(lambda x: x.decode("utf-8"),request.args[arg])))

        if breeds:
            cursor.execute("""
                SELECT gender, COUNT(*) 
                FROM dogs
                WHERE breed_primary=%(breed)s 
                GROUP BY gender
                """, {
                    'breed': breeds[0][0] #TODO Add support for a list of breeds
                })
            rows = cursor.fetchall()
        else:
            cursor.execute("""
                SELECT gender, COUNT(*) 
                FROM dogs
                GROUP BY gender
                """)
            rows = cursor.fetchall()

        for row in rows:
            labels.append(row[0])
            data.append(row[1])

        setCorsHeaders(request)
        request.setHeader('Content-Type', 'application/json')
        response = json.dumps({"labels": labels, "data": data})
        return response

#Function to make queries for age data
def getAgeSplitData(cursor, breeds):
    if breeds:
        print(breeds)
        cursor.execute("""
            SELECT 
                SUM (
                    CASE WHEN age < 5 THEN
                        1
                    ELSE
                        0
                    END
                    ) AS "Puppy",
                SUM (
                    CASE WHEN age > 4 and age < 25 THEN
                        1
                    ELSE
                        0
                    END
                    ) AS "Adolescent",
                SUM (
                    CASE WHEN age > 24 and age < 73 THEN
                        1
                    ELSE
                        0
                    END
                    ) AS "Adult",
                SUM (
                    CASE WHEN age > 72 THEN
                        1
                    ELSE
                        0
                    END
                    ) AS "Senior"
            FROM dogs
            WHERE breed_primary=%(breed)s""", {
                'breed':breeds[0][0]
            })
        rows = cursor.fetchall()
        row = rows[0]
    else:
        cursor.execute("""
            SELECT 
                SUM (
                    CASE WHEN age < 5 THEN
                        1
                    ELSE
                        0
                    END
                    ) AS "Puppy",
                SUM (
                    CASE WHEN age > 4 and age < 25 THEN
                        1
                    ELSE
                        0
                    END
                    ) AS "Adolescent",
                SUM (
                    CASE WHEN age > 24 and age < 73 THEN
                        1
                    ELSE
                        0
                    END
                    ) AS "Adult",
                SUM (
                    CASE WHEN age > 73 THEN
                        1
                    ELSE
                        0
                    END
                    ) AS "Senior"
            FROM dogs""")
        rows = cursor.fetchall()
        row = rows[0]
    return row

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
