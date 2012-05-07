
class Inspector:
    """interface to read and write folios from cabinet of recipes
    
       > cabinet - file on disk where data is stored
       > recipe - series of folios describing changes to a set of vittles
       > folio - record of dashes (changes) added during a cookout
       > dash - an atomic change to a vittle during a cookout
    """
    
    def __init__(self, cabinet):
        """inspector initializer takes cabinet as an argument
           
           cabinet initially implemented using builtin dbm library
        """
        pass
    
    def report(self, cookout):
        """commit agitation recorded in cookout as a folio in cabinet
        """
        pass
    
    def foia_request(self, number):
        """return folio associated with given number
        """
        
    class Folio:
        """interface to read a folio from cabinet
        """
        
        def __init__(self, cabinet, number):
            """initialized with a cabinet and number
            """
            pass
        
        def get_number(self):
            """return this folio's record number
            """
            pass
            
        def get_puppet(self):
            """return puppet number for agent reporting this folio
            """
            pass
            
        def get_recipes(self):
            """return an iterator over the names of recipes
            """  
            pass
            
        def get_dashes(self, recipe):
            """return iterator over dashes added to one recipe in folio
            """
            pass
            
