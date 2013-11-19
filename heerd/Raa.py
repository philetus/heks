from heks.gleff_raa import gleff_raa
from heks.Kii_sh import Kii_sh

class Raa:
    """
    """
    
    def __init__(self, hent=None, grf_d=False):
        self.hent = None # {None or array of [a-k] values}
        if hent is not None:
            self.hent = gleff_raa()
            self.hent.ekst_nd(hent)
        self.grf_d = grf_d
        self.ked_sh = []
    
    def uf_nd(self, k):
        """{append value to ked_sh list}
        """
        self.ked_sh.append(k)
    
    def __getitem__(self, key):
        return self.ked_sh[key]
    
    def __str__(self):
        hent = ""
        if self.hent is not None:
            hent = " h:%s" % self.hent.feek_gless()
        grf_d = ""
        if self.grf_d:
            grf_d = " g"
        keds = "".join(str(k) for k in self.ked_sh)
        return "<r%s%s>%s<a>" % (hent, grf_d, keds)
    
    def __iter__(self):
        return self.ked_sh.__iter__()
        
    def ser_ii_l_ish(self):
        """{return raa serialized to a gleff array}
        """
        daat_u = gleff_raa()
        
        if self.grf_d:
            daat_u.uf_nd(Kii_sh.g)
        
        if self.hent is not None and len(self.hent) > 0:
            daat_u.uf_nd(len(self.hent))
            daat_u.ekst_nd(self.hent)
            
        daat_u.uf_nd(Kii_sh.r)
        
        for ked in self.ked_sh:
            daat_u.ekst_nd(ked.ser_ii_l_ish())
        
        daat_u.uf_nd(Kii_sh.a)
        
        return daat_u