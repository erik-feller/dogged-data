import datetime

class Dog:
    """A class to hold dog data and do some processing and storage"""

    def __init__(self, db_id, h_id, chip_num, name, p_breed, s_breed, age, gender, in_time, out_time):
        self.db_id = db_id
        self.h_id = h_id
        self.chip_num = chip_num
        self.name = name
        self.p_breed = p_breed
        self.s_breed = s_breed
        self.age = age
        self.gender = gender
        self.in_time = in_time 
        self.out_time = out_time
        #Add some bool values for behavior stuff
        
    def emptyDog():
        return Dog(None, None, None, None, None, None, None, None, None, None)


    def createFromAdoptableSearch(self, adoptableSearch):
        #later make a db query to see if the dog exists already
        self.h_id = int(adoptableSearch['ID'])
        if adoptableSearch['ChipNumber'] is not None:
            self.chip_num = int(adoptableSearch['ChipNumber'])
        else:
            self.chip_num = 0
        self.name = str(adoptableSearch['Name'])
        self.p_breed = str(adoptableSearch['PrimaryBreed'])
        self.s_breed = str(adoptableSearch['SecondaryBreed'])
        self.age = int(adoptableSearch['Age'])
        self.gender = str(adoptableSearch['Sex'])
        self.in_time = datetime.datetime.now()

    #TODO: Add a function that reads from database rows to Dog

    def updateInDb(self, conn):
        #Connect to database
        cursor = conn.cursor()
        #Check to see if the dog is already in the database
        cursor.execute("SELECT * FROM dogs WHERE humane_id=%s",(self.h_id,))
        rows = cursor.fetchall()
        if len(rows) > 0:
            #Dog is in database, just update
            print("{0} is already in the database, updating their entry with the most recent info".format(self.name))
            cursor.execute("UPDATE dogs SET age=%s, breed_primary=%s, breed_secondary=%s WHERE humane_id=%s", (self.age, self.p_breed, self.s_breed, self.h_id))
        else:
            #insert dog into database
            print("Adding {0} to the database".format(self.name))
            #cursor.execute(self.sql_insert_print())
            cursor.execute("INSERT INTO dogs (humane_id, name, age, breed_primary, breed_secondary, gender, in_time, out_time) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (self.h_id, self.name, self.age, self.p_breed, self.s_breed, self.gender, self.in_time, self.out_time))
        conn.commit()
        #print(cursor.fetchone())

    def add_out_time(self, out_time):
        self.out_time = out_time

    #This function primarily serves a debug purpose
    def pretty_print(self):
        if self.s_breed == None:
            print(self.name + " is a " + self.p_breed + " that is " + str(self.age) + " months old " + self.gender)
        else:
            print(self.name + " is a " + self.p_breed + ", " + self.s_breed + " that is " + str(self.age) + " months old " + self.gender)

