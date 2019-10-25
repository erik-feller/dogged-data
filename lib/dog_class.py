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

    def add_out_time(self, out_time):
        self.out_time = out_time

    def createFromAdoptableSearch(self, adoptableSearch):
        #later make a db query to see if the dog exists already
        self.h_id = int(adoptableSearch['ID'])
        self.chip_num = int(adoptableSearch['ChipNumber'])
        self.name = str(adoptableSearch['Name'])
        self.p_breed = str(adoptableSearch['PrimaryBreed'])
        self.s_breed = str(adoptableSearch['SecondaryBreed'])
        self.age = int(adoptableSearch['Age'])
        self.gender = str(adoptableSearch['Sex'])

    def pretty_print(self):
        if self.s_breed == None:
            print(self.name + " is a " + self.p_breed + " that is " + str(self.age) + " months old " + self.gender)
        else:
            print(self.name + " is a " + self.p_breed + ", " + self.s_breed + " that is " + str(self.age) + " months old " + self.gender)

    def sql_insert_print(self):
        #Handle the case where the data is new
        if self.db_id == None:
            return ("INSERT INTO dogdata (humane_id, name, age, breed_primary, breed_secondary, gender, in_time, out_time) VALUES ({0},{1},{2},{3},{4},{5},{6},{7})".format(self.h_id, self.name, self.age, self.p_breed, self.s_breed, self.gender, self.in_time, self.out_time))
        
        else:
            #If the entry alrady exists in the database, enforce only updating out time.
            return ("UPDATE dogdata SET out_time={0} WHERE id={1}".format(self.db_id, self.out_time))
            
