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
    @hold_times #List of timestamps seperated by commas, rep as str
    attr_accessor :out_time
    @out_time

    def load_data(id_query, db_handle)
        #Waiting to implement until I have db storing
    end

    def load_data_row(row)
        #A function that loads a dog from a DB row
        @id = row[0]
        @name = row[1]
        @breed_primary = row[2]
        @breed_second = row[3]
        @gender = row[4]
        @age = row[5]
        @status = row[6]
        @intake_time = row[7]
        @hold_times = row[8]
        @out_time = row[9]
        return self
    end

    def store_data(db_handle)
        #Store the data of the current object 
        if is_new(db_handle)
           #puts("dog " + name + " is a new dog")
           db_handle.execute("INSERT INTO dogdata(id, name, breed_primary, breed_secondary, gender, age, status, in_time, hold_times, out_time) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [id, name, breed_primary, breed_second, gender, age, status, intake_time, hold_times, out_time])
        end
    end
    
    def update_data(db_handle)
      db_handle.execute("UPDATE dogdata SET id=?, name=?, breed_primary=?, breed_secondary=?, gender=?, age=?, status=?, hold_times=?, out_time=? WHERE id=?", [id, name, breed_primary, breed_second, gender, age, status, hold_times, out_time, id])
    end

    def load_db(target, db_handle)
      db_handle.execute("SELECT * FROM dogdata where id=?)", [target])
    end

    def is_new(db_handle)
      #determine if a dog is new to the database or not
      if db_handle.execute("SELECT id FROM dogdata WHERE id LIKE " + id.to_s).length == 0
        true
      else
        false
      end
    end

    def set_out_time()
      #Set the out time to the current time
      @out_time = Time.now.utc.to_i
    end

    def status_changed(db_handle)
      #determine if the status of a dog has been changed
      if !(self.is_new)
        db_dog = Dog.new
        db_dog.load_db(id, db_handle)
        if db_dog.status != status
          return true
        else
          false
        end
      end
    end

    def hold_time_record(db_loc)
      #record the specific times a dog has been placed on hold. Stored as comma seperated timestamps
      if self.status_changed && status == "On Hold"
        if hold_times
          @hold_times = hold_times + "," + Time.now.utc.to_s
        else
          @hold_times = Time.now.uts.to_s
        end
      end
    end
        
end
