class Dog:
    """A class to hold dog data and do some processing and storage"""

    def __init__(self, db_id, h_id, name, p_breed, s_breed, age, gender, in_time, out_time):
        self.db_id = db_id
        self.h_id = h_id
        self.name = name
        self.p_breed = p_breed
        self.s_breed = s_breed
        self.age = age
        self.gender = gender
        self.in_time = in_time 
        self.out_time = out_time

    def add_out_time(self, out_time):
        self.out_time = out_time

    def pretty_print(self):
        if self.s_breed == None:
            print(self.name + " is a " + self.p_breed + " that is " + str(self.age) + " months old " + self.gender)
        else:
            print(self.name + " is a " + self.p_breed + ", " + self.s_breed + " that is " + str(self.age) + " months old " + self.gender)
