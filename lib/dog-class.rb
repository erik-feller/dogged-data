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
    @id
    @breed_primary
    @breed_second
    @gender
    @age
    @status
    @intake_time
    @out_time
    
    def load_data(id_query)
    end
        
end
