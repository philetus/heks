from Leeff import Leeff
from Gleff_s import Gleff_s

class Nnot(Leeff):
    """lends emotion or punctuation or some particular sense to containing nod
    """
        
    def __init__(self, rent):
        Leeff.__init__(self, rent) # superclass constructor
        
    def __repr__(self):
        return  "Nnot('" + ''.join(Gleff_s.gless[i] for i in self._data) + "')"
