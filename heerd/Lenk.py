from heks.gleff_raa import gleff_raa
from heks.Kii_sh import Kii_sh
from heks.heerd.Need import Need
from heks.heerd.Raa import Raa
from heks.heerd.Fala import Fala

class Lenk(Need):
    """
    """
    
    def __init__(self, daat_u=None):
        Need.__init__(self, daat_u)
        self.tif = Kii_sh.r
        
        # lenk daat_u
        self.dak = None
        self.nekst = None
        self.neet_sh = []
        self.baks_sh = set()
        