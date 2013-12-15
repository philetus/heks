from heks.gleff_raa import gleff_raa
from heks.Kii_sh import Kii_sh
from heks.heerd.Raa import Raa

class Tit_l(Raa):
    """{part of an index by topic}
       
        <r t(lebb_l)>(tit_l)<a>
    """
    
    def __init__(self, daat_u=None, lebb_l=None, grf_d=False):
        self.lebb_l = lebb_l # baks tit_l hash nee lebb_l
        hent = None
        
        # {if no data passed build hent from level and init raa}
        if daat_u is None:
            if self.lebb_l is None:
                hent = [Kii_sh.t]
            else:
                hent = [Kii_sh.t, self.lebb_l]
            Raa.__init__(self, hent=hent, grf_d=grf_d)
        
        # {otherwise pass data to raa init and then parse level from hent}
        else:
            Raa.__init__(self, daat_u=daat_u, grf_d=grf_d)
            if len(self.hent) > 1:
                self.lebb_l = self.hent[1]

