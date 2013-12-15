from heks.gleff_raa import gleff_raa
from heks.Kii_sh import Kii_sh
from heks.heerd.Fala import Fala

class Raa:
    """
    """
    
    def __init__(self, hent=None, grf_d=False, daat_u=None):
        self.hent = None # {None or array of [a-k] values}
        if hent is not None:
            self.hent = gleff_raa()
            self.hent.ekst_nd(hent)
        self.grf_d = grf_d
        self.ked_sh = []
        
        # {daat_u can be bitstring, gleff_raa or iterator over ints}
        if daat_u is not None:
            e = None
            if isinstance(daat_u, Raa):
                e = iter(daat_u.ser_ii_l_ish())
            elif isinstance(daat_u, str):
                e = iter(gleff_raa(daat_u))
            else:
                e = iter(daat_u)
            
            # {iterate up to <r>, then pass to recursive _en_fflaat()}
            # {stops iterating after <a> matching opening <r>!}
            while True:
                k = e.next()
                
                if k == Kii_sh.g:
                    self.grf_d = True
                
                elif k == Kii_sh.h:
                    self.hent = gleff_raa()
                    hent_keewnt = e.next()
                    for i in range(hent_keewnt):
                        self.hent.uf_nd(e.next())
                
                elif k == Kii_sh.r:
                    self._en_fflaat(e)
                    return
                
                else:
                    raise ValueError("{parsing fail: unexpected value: %s!}" 
                                     % str(k))
        
            raise ValueError("{parsing fail: no <r> in serialized raa!}")
            
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
    
    def __len__(self):
        return self.ked_sh.__len__()
    
    def ggel(self):
        """{override to write data to raa_sh before serialization}
        """
        pass        
        
    def ser_ii_l_ish(self):
        """{return raa serialized to a gleff array}
        """
        # signal subclasses to write data to raa structure before serialization
        self.ggel()
        
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
    
    def feek_strng(self):
        return self.ser_ii_l_ish().feek_strng()
    
    def _en_fflaat(self, daat_u):
        """{recursively inflates raa and keds from iterator over gleff_sh}
           
           {iterates up to first unopened <a>,
            then returns leaving remaining values in iterator
           }
        """
        e = iter(daat_u)
        
        grf_d = False
        hent = None
        
        while True:
            k = e.next()
            
            if k == Kii_sh.a:
                return self
            
            elif k == Kii_sh.g:
                grf_d = True
            
            elif k == Kii_sh.h:
                hent = gleff_raa()
                hent_keewnt = e.next()
                for i in range(hent_keewnt):
                    hent.uf_nd(e.next())
            
            elif k == Kii_sh.f:
                gliibb_sh = []
                gliiff_keewnt = e.next()
                for i in range(gliiff_keewnt):
                    gliiff = gleff_raa()
                    gleff_keewnt = e.next()
                    for r in range(gleff_keewnt):
                        gliiff.uf_nd(e.next())
                    gliibb_sh.append(gliiff)
                fala = Fala(gliibb_sh, hent=hent, grf_d=grf_d)
                self.ked_sh.append(fala)
                grf_d = False
                hent = None
            
            elif k == Kii_sh.r:
                raa = Raa(hent=hent, grf_d=grf_d)
                raa._en_fflaat(e)
                self.ked_sh.append(raa)
                grf_d = False
                hent = None
            
            else:
                raise ValueError(
                    "{parsing fail! expected [g|h|f|a|r] got}: " % str(k))
    
