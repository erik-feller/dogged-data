###############################################################################
#
# dog-class.rb
#
# defines a class to hold information about dogs and store and load that
# information from an associated sql database. Current methods should be a load
# and store method. Maybe a seperate update method but probably not.
#
# February 1, 2017
# Erik Feller
#
################################################################################

class Dog
    
    #define data members of the class
    attr_accessor :id
    @id
    attr_accessor :name
    @name
    attr_accessor :breed_primary
    @breed_primary
    attr_accessor :breed_second
    @breed_second
    attr_accessor :gender
    @gender
    attr_accessor :age
    @age
    attr_accessor :status
    @status
    attr_accessor :intake_time
    @intake_time
    attr_accessor :hold_times
    @hold_times
    attr_accessor :out_time
    @out_time

    def load_data(id_query, db_handle)
        #Waiting to implement until I have db storing
    end

    def set(id, breed_primary, breed_second, gender, age, status, intake_time, out_time)
        #Change Attributes in case we need to
    end

    def store_data(db_handle)
        #Store the data of the current object 
        if is_new(db_handle)
           puts("dog " + name + " is a new dog")
           db_handle.execute("INSERT INTO dogdata(id, name, breed_primary, breed_secondary, gender, age, status) VALUES(?, ?, ?, ?, ?, ?, ?)", [id, name, breed_primary, breed_second, gender, age, status])
        end
        db_handle.execute("INSERT INTO seconddata(id, time, status) VALUES(?, ?, ?)", [id, intake_time, status])
    end

    def store_data_direct(id, breed_primary, breed_second, gender, age, status, intake_time)
        #Add data into the database
    end

    def is_new(db_handle)
      #determine if a dog is new to the database or not
      if db_handle.execute("SELECT id FROM dogdata WHERE id LIKE " + id.to_s).length == 0
        true
      else
        false
      end
    end

    def status_changed(db_loc)
      #determine if the status of a dog has been changed
    end

    def hold_time_record(db_loc)
      #record the specific times a dog has been placed on hold. Stored as comma seperated timestamps
    end
        
end
