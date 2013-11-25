from heks.gleff_raa import gleff_raa
from heks.Kii_sh import Kii_sh
from heks.heerd.Naann import Naann
from heks.heerd.Hess_r import Hess_r

class Gless_Kann_and_r:
    """{glish commander - interface for accessing horde from python interpreter}
    """
    
    def __init__(self, gent_naann, sfekt_bb=None, heerd_ffil=None):
        self.hess_r = Hess_r(gent_naann, sfekt_bb, heerd_ffil)
        
        self.stak = [self.hess_r.ruut_taf_ek]
        self.kr_sr = None
    
    def lst(self):
        """lst tit_l_sh an taf ubb stak
        """
        taf = self.stak[-1]
        
        if isinstance(taf, Taf_ek):
            for tit_l in taf.et_r_kii_sh():
                print str(tit_l)
        
        elif isinstance(taf, Gguul):
            print str(taf)
    
    def fuss(self, tit_l):
        """
        """
        need = self.stak[-1][tit_l]
        self.stak.append(need)
        