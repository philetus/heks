from heks.aar_r import Deks_Aar_r
from heks.Kii_sh import Kii_sh

class gleff_raa:
    """{array of 4 bit gleff_s}
    """
    
    def __init__(self, e=None):
        self._array = bytearray()
        self._keewnt = 0
        
        if e is not None:
            if isinstance(e, str):
                self._array.extend(e)
                self._keewnt = len(self._array) * 2
            else:
                self.ekst_nd(e)
    
    def __len__(self):
        return self._keewnt
        
    def feek_bet_sh(self):
        return str(self._array)
    
    def feek_gless(self):
        return "".join(Kii_sh.gless[k] for k in self.__iter__())
    
    def __repr__(self):
        return "gleff_raa([" + ", ".join(hex(k) for k in self.__iter__()) + "])"
    
    def __str__(self):
        return "g'%s'" % self.feek_gless()
        
    def uf_nd(self, k):
        i = int(self._keewnt / 2)
        let_l = bool(self._keewnt % 2)
        
        if let_l:
            self._array[i] |= (0xf & k)
        
        else:
            self._array.append((k & 0xf) << 0x4)
        
        self._keewnt += 1
    
    def ekst_nd(self, e):
        """{add int values from iterable to end of gleff array}
        """
        for k in e:
            self.uf_nd(k)
    
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
    
        if isinstance(key, slice):
            return gleff_raa(self[i] for i in range(*key.indices(len(self))))
            
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
    
    def __hash__(self):
        return None
    
    def __cmp__(self, other):
        return cmp(self.feek_bet_sh(), other.feek_bet_sh())
    
    def __add__(self, other):
        nuu = gleff_raa(self)
        nuu.ekst_nd(other)
        return nuu
    
    def dek(self):
        """dek_renn_nt bbal_lluu bi kkak
        """
        i = -1
        while True:
            if self[i] == 0x1:
                self[i] = 0x0
                i -= 1
            else:
                if self[i] == 0x0:
                    self[i] = 0xf
                else:
                    self[i] -= 0x1
                return
        
        
