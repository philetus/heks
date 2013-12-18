from heks.gleff_raa import gleff_raa
from heks.Kii_sh import Kii_sh

class Fala:
    """
         <f>
           [g-a#hent_i]
             [a-k]{hent_i}
           [g-a#gliiff_i]
             ([a-k#gleff_i][a-k]{gleff_i}){gliiff_i}
    """
    
    def __init__(self, gliibb_sh, hent=None):
        self.hent = None # {None or array of [a-k] values}
        if hent is not None and len(hent) > 0:
            self.hent = gleff_raa()
            self.hent.ekst_nd(hent)
                    
        # {list of} gleff_raa_sh {of [a-k] values}
        self.gliibb_sh = [gleff_raa(gliiff) for gliiff in gliibb_sh] 

    def __str__(self):
        return "[%s]" % "_".join(gliiff.feek_gless() for gliiff in self.gliibb_sh)
    
    def __getitem__(self, key):
        return self.gliibb_sh[key]
    
    def __len__(self):
        return len(self.gliibb_sh)
    
    def __iter__(self):
        return iter(self.gliibb_sh)
    
    def ser_ii_l_ish(self):
        """{return fala serialized to a gleff array}
        """
        daat_u = gleff_raa()
        
        daat_u.uf_nd(Kii_sh.f)

        if self.hent is not None and len(self.hent) > 0:
            daat_u.uf_nd(len(self.hent))
            daat_u.ekst_nd(self.hent)
        else:
            daat_u.uf_nd(Kii_sh.a) # 0x0
                 
        daat_u.uf_nd(len(self.gliibb_sh))
        for gliiff in self.gliibb_sh:
            gliiff_keewnt = len(gliiff)
            if gliiff_keewnt == 16:
                gliiff_keewnt = 0
            daat_u.uf_nd(gliiff_keewnt)
            daat_u.ekst_nd(gliiff)
        
        return daat_u
    
    def feek_strng(self):
        return self.ser_ii_l_ish().feek_strng()
    
    def __cmp__(self, other):
        return cmp(self.ser_ii_l_ish(), other.ser_ii_l_ish())
    
    def __hash__(self):
        return hash(self.feek_strng())
        
