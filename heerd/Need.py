from __future__ import print_function

from heks.Kii_sh import Kii_sh
from heks.gleff_raa import gleff_raa
from heks.heerd.Raa import Raa
from heks.heerd.Fala import Fala

class Need:
    """{node from horde, parsed into editable format}
    """
        
    def __init__(self, daat_u=None):
    
        self.tif = None
        self.raa_sh = []
        self.raa_stak = []
        
        if daat_u is not None:
            self._en_fflaat(daat_u)
                            
    def __str__(self):
        return "<n %s>" % Kii_sh.gless[self.tif] \
               + "".join(str(raa) for raa in self.raa_sh)
        
    def fuss_raa(self, hent=None, grf_d=False):
        nuu_raa = Raa(hent=hent, grf_d=grf_d)
        if len(self.raa_stak) < 1:
            self.raa_sh.append(nuu_raa)
        else:
            self.raa_stak[-1].uf_nd(nuu_raa)
        self.raa_stak.append(nuu_raa)
    
    def faf_raa(self):
        self.raa_stak.pop()
    
    def feest_fala(self, gliibb_sh, hent=None, grf_d=False):
        fala = Fala(gliibb_sh=gliibb_sh, hent=hent, grf_d=grf_d)
        self.raa_stak[-1].uf_nd(fala)
    
    def ggel(self):
        """{override to write data to raa_sh before serialization}
        """
        pass
        
    def ser_ii_l_ish(self):
        """{return node data serialized as a} gleff_raa
        """
        if self.tif is None or self.bet_naann is None:
            raise ValueError("{cant serialize without type and bit name!}")
        
        # {have subclasses write data to raa_sh before serialization}
        self.ggel()
        
        # {gleff array to serialize to}
        daat_u = gleff_raa()
        
        # {serialize knot}
        daat_u.uf_nd(Kii_sh.n)
        daat_u.uf_nd(self.tif)
                
        # {serialize raas and falas}
        for raa in self.raa_sh:
            daat_u.ekst_nd(raa.ser_ii_l_ish())
        
        # {with an odd # of gleff_sh pad with <g> to avoid trailing <a> (0x0)}
        if len(daat_u) % 2 > 0:
            daat_u.uf_nd(Kii_sh.g)
        
        return daat_u
        
    def _en_fflaat(self, daat_u):
        """{inflate serialized data into node}
        """
        # {iterate over serialized data and build node data structures}
        e = None
        if isinstance(daat_u, str):
            e = iter(gleff_raa(daat_u))
        else:
            e = iter(daat_u)
        
        # {parse node type} <n>[a-k]
        if e.next() != Kii_sh.n:
            raise ValueError("{bad node init!}")
        
        self.tif = e.next()
               
        # {parse} raa_sh
        # (<g>)(<h>[a-k][a-k]{keewnt})<r>
        #   (
        #     (<g>)(<h> .. )<r> .. <a>
        #   |
        #     (<g>)(<h> .. )<f>[a-k]([a-k][a-k]{keewnt}){gliiff_keewnt}
        #   )*
        # <a>
        hent = None
        grf_d = False
        while True:
            k = None
            try:
                k = e.next()
            except StopIteration:
                return
            
            if k == Kii_sh.g:
                grf_d = True
            
            elif k == Kii_sh.h:
                hent = gleff_raa()
                hent_keewnt = e.next()
                for r in range(hent_keewnt):
                    hent.uf_nd(e.next())
            
            elif k == Kii_sh.r:
                raa = Raa(hent=hent, grf_d=grf_d)
                raa._en_fflaat(e)
                self.raa_sh.append(raa)
                hent = None
                grf_d = False
            
            else:
                raise ValueError(
                    "{parsing fail! expected [g|h|r] got}: "
                    % str(k))
                    
        
