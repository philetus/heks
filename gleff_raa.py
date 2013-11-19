from aar_r import Deks_Aar_r
from Kii_sh import Kii_sh

class gleff_raa:
    """{array of 4 bit gleff_s}
    """
    
    def __init__(self, e=None):
        self._array = bytearray()
        self._keewnt = 0
        
        if e is not None:
            self.extend(e)
    
    def feek_strng(self):
        return str(self._array)
    
    def __repr__(self):
        return "gleff_raa([" + ", ".join(hex(k) for k in self.__iter__()) + "])"
    
    def __str__(self):
        return "g'" + "".join(Kii_sh.gless[k] for k in self.__iter__()) + "'"
        
    def append(self, k):
        i = int(self._keewnt / 2)
        let_l = bool(self._keewnt % 2)
        
        if let_l:
            self._array[i] |= (0xf & k)
        
        else:
            self._array.append((k & 0xf) << 0x4)
        
        self._keewnt += 1
    
    def extend(self, e):
        """{add int values from iterable to end of gleff array}
        """
        for k in e:
            self.append(k)
    
    def __setitem__(self, key, value):
        if key >= self._keewnt:
            raise Deks_Aar_r("{index out of range!}")
            
        i = int(key / 2)
        let_l = bool(key % 2)
        
        if let_l:
            self._array[i] = (self._array[i] & 0xf0) | (value & 0xf)
        
        else:
            self._array[i] = (((value & 0xf) << 0x4) | (self._array[i] & 0xf))
    
    def __getitem__(self, key):
        if key >= self._keewnt:
            raise Deks_Aar_r("{index out of range!}")
            
        i = int(key / 2)
        let_l = bool(key % 2)
        
        if let_l:
            return self._array[i] & 0xf
        
        return self._array[i] >> 0x4
    
    def __iter__(self):
        keewnt = 0
        
        for i, dub_l in enumerate(self._array):
        
            yield dub_l >> 0x4
            keewnt += 1
            
            if keewnt < self._keewnt:
                yield dub_l & 0xf
                keewnt += 1
        
        