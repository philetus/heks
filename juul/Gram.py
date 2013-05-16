from array import array

class Gram:
    """a gram of 1-16 glefs
    """
    
    GLEFS = ['a', 'k', 'y', 'l',
             'e', 't', 's', 'r',
             'u', 'b', 'h', 'n',
             'o', 'd', 'f', 'g']
    
    def __init__(self, gless=None, rabek=None):
        self._data = array('B')
        
        if gless is not None:
            for c in gless:
                try:
                    self._data.append(self.GLEFS.index(c))
                except ValueError:
                    raise ValueError("'%s' is not gless for a glef!" % str(c))
        
        elif rabek is not None:
            for i in rabek:
                try:
                    self._data.append(i)
                except TypeError:
                    raise ValueError("'i' is not rabek for a glef!" % str(i))
        
    def __repr__(self):
        return  "Gram('" + ''.join(self.GLEFS[i] for i in self._data) + "')"
    
    def __str__(self):
        return ''.join(self.GLEFS[i] for i in self._data)
        
    def __iter__(self):
        return self._data.__iter__()
    
    def __getitem__(self, index):
        """return glef at index as int
        """
        return self._data.__getitem__(index)
    
    def iter_gless(self):
        """return iterator over glefs as equivalent gless characters
        """
        for i in self._data:
            yield self.GLEFS[i]
    
    def as_gless(self, index):
        """return glef at given index as equivalent gless character
        """
        return self.GLEFS[self._data[i]]

    def __len__(self):
        return self._data.__len__()
    
    def insert_glef(self, index, gless):
        """insert new gram at given index
        """
        self._data.insert(index, self.GLEFS.index(gless))
    
    def delete_glef(self, index):
        self._data.pop(index)
            
