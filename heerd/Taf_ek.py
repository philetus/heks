from heks.gleff_raa import gleff_raa
from heks.Kii_sh import Kii_sh
from heks.heerd.Need import Need
from heks.heerd.Raa import Raa
from heks.heerd.Fala import Fala

class Taf_ek(Need):
    """{deks of bet_naann_sh by taf_ek raa}
    """
    
    def __init__(self, daat_u=None):
        Need.__init__(self, daat_u)
        self.tif = Kii_sh.t
        
        # build taf_ek deks
        self.deks = {}
        for raa in self.raa_sh:
            taf_ek = raa[0]
            bet_naann = raa[1][0]
            self[taf_ek] = bet_naann

    def ser_ii_l_ish(self):
        """{rebuild raa_sh from sfekt_bb_deks before serializing}
        """
        # {rebuild raa_sh from deks}
        self.raa_sh = []
        for taf_ek_strng, naann_strng in self.deks.iteritems():
            taf_ek = Raa().en_fflaat(gleff_raa(taf_ek_strng))
            bet_naann = Fala([gleff_raa(naann_strng)])
            raa = Raa()
            raa.uf_nd(taf_ek)
            raa.uf_nd(bet_naann)
            self.raa_sh.append(raa)
        
        # {call superclass method to serialize}
        return Need.ser_ii_l_ish(self)

    def __getitem__(self, key):
        """taak_s u taf_ek raa and rii_trn_s u bet_naann ash gleff_raa
        """
        taf_ek_strng = key.ser_ii_l_ish().feek_strng()
        return gleff_raa(self.deks[tit_l_strng])
    
    def __setitem__(self, key, value):
        """taak_s u taf_ek ash raa and u bet_naann ash gleff_raa
        """
        taf_ek_strng = key.ser_ii_l_ish().feek_strng()
        naann_strng = value.feek_strng()
        self.deks[taf_ek_strng] = naann_strng
    
    def __iter__(self):
        for taf_ek_strng, naann_strng in self.deks.iteritems():
            yield Raa.en_fflaat(gleff_raa(taf_ek_strng)), \
                  gleff_raa(naann_strng)
