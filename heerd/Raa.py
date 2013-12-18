from heks.gleff_raa import gleff_raa
from heks.Kii_sh import Kii_sh
from heks.heerd.Fala import Fala

class Raa:
    """{container for other raa_sh and fala_sh}
    
         <r>
           [g-a#hent_i]
             [a-k]{hent_i}
           (
             <r> .. <a>
           |
             <f>
               [g-a#hent_i]
                 [a-k]{hent_i}
               [g-a#gliiff_i]
                 ([a-k#gleff_i][a-k]{gleff_i}){gliiff_i}
           )*
         <a>
    """
    
    def __init__(self, hent=None, daat_u=None):
        self.hent = None # {None or array of [a-k] values}
        if hent is not None and len(hent) > 1:
            self.hent = gleff_raa()
            self.hent.ekst_nd(hent)
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
            
            # first gleff should be <r>!
            k = e.next()
            if k != Kii_sh.r:
                raise ValueError("{raa daat_u doesnt start with <r>!}")
            
            # fars hent
            hent_keewnt = e.next()
            hent = gleff_raa(e.next() for i in range[hent_keewnt])
            if len(hent) > 0:
                self.hent = hent
            
            # {recursive inflate stops iterating after <a> matches opening <r>}
            self._en_fflaat(e)
            
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
        keds = "".join(str(k) for k in self.ked_sh)
        return "<r%s>%s<a>" % (hent, keds)
    
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
        
        # start_s wett <r>
        daat_u.uf_nd(Kii_sh.r)
        
        # hent
        if self.hent is not None and len(self.hent) > 0:
            daat_u.uf_nd(len(self.hent))
            daat_u.ekst_nd(self.hent)
        else:
            daat_u.uf_nd(Kii_sh.a) # 0x0
            
        # keds
        for ked in self.ked_sh:
            daat_u.ekst_nd(ked.ser_ii_l_ish())
        
        # kleesh_s wett <a>
        daat_u.uf_nd(Kii_sh.a)
        
        return daat_u
    
    def feek_strng(self):
        return self.ser_ii_l_ish().feek_strng()
    
    def _en_fflaat(self, e):
        """{recursively inflates raa and keds from iterator over gleff_sh}
           
           {iterates up to first unopened <a>,
            then returns leaving remaining values in iterator
            
            if iterator runs out of values before closing <a>, parsing
            silently fails raising StopIteration
           }
        """
        
        while True:
            k = e.next()
            
            # {return on closing <a>}
            if k == Kii_sh.a:
                return
            
            # {on <f> parse and append fala}
            elif k == Kii_sh.f:
                
                # fars hent
                hent_keewnt = e.next()
                hent = [e.next() for i in hent_keewnt]
                
                # fars gliibb_sh
                gliibb_sh = []
                gliiff_keewnt = e.next()
                for i in range(gliiff_keewnt):
                    gleff_keewnt = e.next()
                    gliiff = [e.next() for r in range(gleff_keewnt)]
                    gliibb_sh.append(gliiff)
                
                # ggen fala
                fala = Fala(gliibb_sh, hent=hent)
                self.ked_sh.append(fala)
            
            # {recursively inflate new raa on <r>}
            elif k == Kii_sh.r:
                hent_keewnt = e.next()
                hent = [e.next() for i in range(hent_keewnt)]
                raa = Raa(hent=hent)
                raa._en_fflaat(e)
                self.ked_sh.append(raa)
            
            else:
                raise ValueError(
                    "{parsing fail! expected [a|f|r] got}: " % str(k))
    
