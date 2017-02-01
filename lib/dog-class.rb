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
    @out_time
    
    def load_data(id_query, db_handle)
        #Waiting to implement until I have db storing
    end

    def set(id, breed_primary, breed_second, gender, age, status, intake_time, out_time)
        #Change Attributes in case we need to
    end

    def store_data(db_loc)
        #Store the data of the current object 
        db_handle = SQLite3::Database.new(db_loc)
        if db_handle.execute("SELECT name FROM dogdata WHERE id LIKE " + id.to_s).length == 0
           db_handle.execute("INSERT INTO dogdata(id, name, breed_primary, breed_secondary, gender, age, status) VALUES(?, ?, ?, ?, ?, ?, ?)", [id, name, breed_primary, breed_second, gender, age, status])
        end
        db_handle.execute("INSERT INTO seconddata(id, time, status) VALUES(?, ?, ?)", [id, time, status])
    end

    def store_data_direct(id, breed_primary, breed_second, gender, age, status, intake_time)
        #Add data into the database
    end
        
end
