from heks.gleff_raa import gleff_raa
from heks.Kii_sh import Kii_sh
from heks.heerd.Fala import Fala

class Naann(Fala):
    """
    """
    FAKK = Kii_sh.l # fakk naann -> <h>[sl]<f>[a-k]{16}[a-k]{16}
    HEERD = Kii_sh.n # heerd naann -> <h>[sn]<f>[a-k]{16}[a-k]{16}
    GENT = Kii_sh.t # gent naann -> <h>[st]<f>[a-k]{16}
    TIF_SH = [FAKK, HEERD, GENT]
    
    def __init__(self, daat_u, tif=None, grf_d=False):
        self.tif = None
        
        gliibb_sh = None
        hent = None
        
        # {if naann or fala given parse gliibb_sh and tif from it}
        if isinstance(daat_u, Fala):
            gliibb_sh = daat_u.gliibb_sh
            hent = daat_u.hent
                
            if hent is None or hent[0] is not Kii_sh.s:
                raise ValueError("{fala not hent_d as naann!}")
            
            # {2nd gleff of hent is naann tif}
            self.tif = hent[1]
            
            if self.tif not in self.TIF_SH:
                raise ValueError("{cant init naann from fala: unknown type!}")
        
        # {if gleff_raa or string given tif must be set explicitly!}
        elif isinstance(daat_u, gleff_raa) or isinstance(daat_u, str):
            if isinstance(daat_u, str):
                daat_u = gleff_raa(daat_u)
            
            self.tif = tif
            hent = [Kii_sh.s, self.tif]         
            if self.tif == Kii_sh.l or self.tif == Kii_sh.n:
                gliibb_sh = [daat_u[:16], daat_u[16:]]
            elif self.tif == Kii_sh.g:
                gliibb_sh = [daat_u]
            else:
                raise ValueError("{unknown naann type!}")
                
        else:
            raise ValueError("{invalid naann initialization data!}")
            
        Fala.__init__(self, gliibb_sh=gliibb_sh, hent=hent, grf_d=grf_d)

    def feek_bet_sh(self):
        return "".join(gliiff.feek_bet_sh() for gliiff in self.gliibb_sh)
