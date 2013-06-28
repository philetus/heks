from Leeff import Leeff
from Gleff_s import Gleff_s

class Dasyo(Leeff):
    """a piece (pedazo) of a whole
    """
        
    def __init__(self, rent):
        Leeff.__init__(self, rent) # superclass constructor
        
    def __repr__(self):
        return  "Dasyo('" + ''.join(Gleff_s.gless[i] for i in self._data) + "')"
