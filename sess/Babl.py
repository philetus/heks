from Leeff import Leeff
from Gleff_s import Gleff_s

class Babl(Leeff):
    """a phonetic fragment represented by a series of up to 16 gleffs
    """
        
    def __init__(self, rent):
        Leeff.__init__(self, rent) # superclass constructor
        
    def __repr__(self):
        return  "Babl('" + ''.join(Gleff_s.gless[i] for i in self._data) + "')"
    
    def __str__(self):
        return ''.join(Gleff_s.gless[i] for i in self._data)
            
    def iter_gless(self):
        """return iterator over glefs as equivalent gless characters
        """
        for i in self._data:
            yield Gleff_s.gless[i]
    
    def asy_gless(self, index):
        """return glef at given index as equivalent gless character
        """
        return Gleff_s.gless[self._data[i]]

            
