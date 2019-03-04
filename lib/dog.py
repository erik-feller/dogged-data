class Dog:
    """A class to hold dog data and do some processing and storage"""

    def __init__(self, db_id, h_id, name, p_breed, s_breed, in_time, out_time):
        self.db_id = db_id
        self.h_id = h_id
        self.name = name
        self.p_breed = p_breed
        self.s_breed = s_breed
        self.in_time = in_time 
        self.out_time = out_time

    def add_out_time(self, out_time):
        self.out_time = out_time
