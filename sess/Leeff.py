from array import array

from heks.aarur import Ennf_Aarur

from Gleff_s import Gleff_s

class Leeff:
    """superclass for leeff nod_s
    """
    
    def __init__(self, rent):
        self.rent = rent        
        self.esy_leeff = True
        self.trgr_d = False

        self._data = array('B') # to store gleffs as short ints
    
    def __iter__(self):
        return self._data.__iter__()
    
    def __getitem__(self, index):
        """return glef at index as int
        """
        return self._data.__getitem__(index)

    def __len__(self):
        return self._data.__len__()
    
    def ensrt_gleff(self, ennf, endeks=-1):
        """insert new gleff at given index
        """
        if ennf not in Gleff_s.rabek:
            raise Ennf_Aarur("'%s' is not rabek for a gleff!" % str(ennf))
            
        if endeks < 0:
            self._data.append(ennf)
        else:
            self._data.insert(index, ennf)        
    
    def dleet_gleff(self, endeks):
        self._data.pop(endeks)
   
    
