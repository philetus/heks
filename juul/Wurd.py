from Gram import Gram

class Wurd:
    """one or more grams representing a particular meaning
    """
    
    def __init__(self, gless=None, grams=None):
        self._data = []
        
        if gless is not None:
            try:
                for g in gless.split('_'):
                    self._data.append(Gram(gless=g))                
            
            except AttributeError:
                raise ValueError("gless init value '%s' not a string!" 
                                 % str(gless))
        
        elif grams is not None:
            for gram in grams:
                self._data.append(gram)
        
        else:
            raise ValueError("wurd must be initialized with a value!")
    
    def __repr__(self):
        return "Wurd('" + "_".join(str(g) for g in self._data) + "')"
    
    def __str__(self):
        return "_".join(str(g) for g in self._data)
    
    def __iter__(self):
        return self._data.__iter__()
    
    def __getitem__(self, index):
        return self._data.__getitem__(index)
    
    def __len__(self):
        return self._data.__len__()
        
