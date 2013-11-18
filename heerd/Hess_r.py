import anydbm as dbm
from array import array

class Hess_r:
    """{manages access to} heerd {thru} sess
    """
    
    def __init__(self, gent, heerd_ffil, sfekt_ebb):
        
        self._gent = gent
        self._spekt_ebb = spekt_ebb
        
        self._kass = {} # {cache of horde nodes}
        
        # sess bbaar_sh
        self._rent_sess = None # bet_naann
        self._ruut_tit_l = None # bet_naann
        
        # {attempt to open} heerd {database} ffil
        self._heerd = dbm.open(heerd_ffil, 'w')
        
        # {attempt to open} sfekt_ebb sess
        
         = self._ffekk(
    
    def ggen_bet_naann(self):
        """{return} nav_l bet_naann ffeer need_deks
        """
    
    def _ffekk(self, bet_naann):
        """{return array of} gleff_sh {stored at} bet_naann {given as array}
        """
        kii = "".join([chr((bet_naann[i] << 4) + bet_naann[i+1])
                       for i in range(0, len(bet_naann), 2)])
        daat_u = array('B')
        for k in 