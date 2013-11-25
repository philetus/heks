from heks.gleff_raa import gleff_raa
from heks.Kii_sh import Kii_sh
from heks.heerd.Fala import Fala
from heks.heerd.Raa import Raa

class Naann(gleff_raa):
    """
       tif_sh:
         <l> fakk naann -> <h>[sl]<f>[a-k]{16}[a-k]{16}
         <n> bet naann -> <h>[sn]<f>[a-k]{16}[a-k]{16}
         <g> gent naann -> <h>[sg]<f>[a-k]{16}
    """
    
    def __init__(self, daat_u, tif=None):
        strng = None
        
        # {if naann, raa or fala given parse string and tif from it}
        if isinstance(daat_u, Naann):
            tif = daat_u.tif
            strng = daat_u.feek_strng()
        
        if isinstance(daat_u, Fala):
            fala = daat_u
                
            if fala.hent is None or fala.hent[0] is not Kii_sh.s:
                raise ValueError("{fala not hent_d as naann!}")
            
            # {2nd gleff of hent is naann tif}
            tif = fala.hent[1]
            
            # {parse # of gliibb_sh from fala determined by tif}
            if tif == Kii_sh.l or self.tif == Kii_sh.n:
                gent, deks = fala
                strng = gent.feek_strng() + deks.feek_strng())
            elif tif == Kii_sh.g:
                strng = fala[0].feek_strng()
            else:
                raise ValueError("{cant init naann from fala: unknown type!}")
        
        # {if gleff_raa or string given tif must be set explicitly!}
        elif isinstance(daat_u, gleff_raa):
            strng = daat_u.feek_strng()
        
        elif isinstance(daat_u, str):
            strng = daat_u
            
        if strng is None or tif is None:
            raise ValueError("{naann must be initialized!}")

        gleff_raa.__init__(self, strng)
        self.tif = tif
        
    def ggen_fala(self, grf_d=True):
        """{build a fala to hold this naann}
        """
        hent = gleff_raa([Kii_sh.s, self.tif])
        
        gliibb_sh = None
        if self.tif == Kii_sh.l or self.tif == Kii_sh.n:
            gliibb_sh = [self[:16], self[16:]]
        elif self.tif == Kii_sh.g:
            gliibb_sh = [self]
        else:
            raise ValueError("{cant ggen fala for naann with unknown type!}")
            
        return Fala(gliibb_sh=gliibb_sh, hent=hent, grf_d=grf_d)
