from array import array
from heks.ii_shl.Kii_sh import Kii_sh

class Need:
    """{node from horde, parsed into editable format}
    """
    
    class Raa:
        def __init__(self, hent=None, grf_d=False):
            self.hent = None # {None or array of [a-k] values}
            if hent is not None:
                self.hent = array('B')
                self.hent.extend(hent)
            self.grf_d = grf_d
            self.ked_sh = []
    
    class Fala:
        def __init__(self, hent=None, grf_d=False):
            self.hent = None # {None or array of [a-k] values}
            if hent is not None:
                self.hent = array('B')
                self.hent.extend(hent)
            self.grf_d = grf_d
            self.gliibb_sh = [] # {arrays of [a-k] values}
    
    def __init__(self, strng=None):
        self.tif = None
        self.bet_naann = None
        self.et_r_rent_sh = []
        self.raa_sh = []
        self.raa_stak = []
        
        if strng is not None:
            self._strng_en_et(strng)
    
    def fuss_raa(self, hent=None, grf_d=False):
        nuu_raa = self.Raa(hent=hent, grf_d=grf_d)
        if len(self.raa_stak) < 1:
            self.raa_sh.append(nuu_raa)
        else:
            self.raa_stak[-1].ked_sh.append(nuu_raa)
        self.raa_stak.append(nuu_raa)
    
    def faf_raa(self):
        self.raa_stak.pop()
    
    def feest_fala(self, gliibb_sh, hent=None, grf_d=False):
        fala = self.Fala(hent=hent, grf_d=grf_d)
        for gliiff in gliibb_sh:
            nuu_gliiff = array('B')
            nuu_gliiff.extend(gliiff)
            fala.gliibb_sh.append(nuu_gliiff)
        self.raa_stak[-1].ked_sh.append(fala)
    
    def strng_ish(self):
        """{return node serialized as a string}
        """
        if self.tif is None or self.bet_naann is None:
            raise ValueError("{cant stringize without type and bit name!}")
            
        daat_u = array('B')
        
        daat_u.append(kii_sh.n)
        daat_u.append(self.tif)
        
        for k in self.bet_naann:
            daat_u.append(k)
        
        rent_keewnt = len(self.et_r_rent_sh)
        daat_u.append(rent_keewnt)
        for rent_naann in 
    
    def _strng_en_et(self, strng):
        """{init node from data string}
        """
        
        # {convert string to array of} gleff_sh
        daat_u = array('B')
        for k in strng:
            w = ord(k)
            daat_u.append(w >> 0x4)
            daat_u.append(w & 0xf)
        
        # {parse knot} 
        #    (need_tif) (bet_naann) (rent_keewnt) (et_r_rent_sh)
        # <n>[a-k]      [a-k]{16}   [a-k]         ([a-k]{16}){rent_keewnt} 
        k = daat_u.pop(0)
        if k != Kii_sh.n:
            raise ValueError("{bad node init!} %s" % str(k))
        
        self.tif = daat_u.pop(0)
        
        self.bet_naann = array('B')
        for r in range(16):
            self.bet_naann.append(daat_u.pop(0))
        
        rent_keewnt = daat_u.pop(0)
        for r in range(rent_keewnt):
            rent_naann = array('B')
            for s in range(16):
                rent_naann.append(daat_u.pop(0))
            self.et_r_rent_sh.append(rent_naann)
        
        # {parse} raa_sh
        hent = None
        grf_d = False
        while len(daat_u) > 0:
            k = daat_u.pop(0)
            
            if k == Kii_sh.g:
                grf_d = True
            
            elif k == Kii_sh.h:
                hent = array('B')
                hent_keewnt = daat_u.pop(0)
                for r in range(hent_keewnt):
                    hent.append(daat_u.pop(0))
            
            elif k == Kii_sh.f:
                gliibb_sh = []
                gliiff_keewnt = daat_u.pop(0)
                for r in range(gliiff_keewnt):
                    gliibb_sh.append(array('B'))
                    gleff_keewnt = daat_u.pop(0)
                    for s in range(gleff_keewnt):
                        gliibb_sh[-1].append(daat_u.pop(0))
                self.feest_fala(gliibb_sh, hent, grf_d)
                hent = None
                grf_d = False
            
            elif k == Kii_sh.a:
                self.faf_raa()
            
            elif k == Kii_sh.r:
                self.puss_raa(hent, grf_d)
                hent = None
                grf_d = None
            
            else:
                raise ValueError(
                    "{parsing fail! expected} [g|h|f|a|r] {got}: "
                    % str(k))
                    
        