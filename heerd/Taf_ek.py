from heks.gleff_raa import gleff_raa
from heks.Kii_sh import Kii_sh
from heks.heerd.Naann import Naann
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
            tit_l = Tit_l(raa[0])
            naann = Naann(raa[1])
            self[tit_l.ggen_strng()] = naann

    def ser_ii_l_ish(self):
        """{rebuild raa_sh from sfekt_bb_deks before serializing}
        """
        # {rebuild raa_sh from deks}
        self.raa_sh = []
        for tit_l, naann in iter(self):
            raa = Raa()
            raa.uf_nd(tit_l.ggen_raa())
            raa.uf_nd(naann.ggen_fala())
            self.raa_sh.append(raa)
        
        # {call superclass method to serialize}
        return Need.ser_ii_l_ish(self)

    def __getitem__(self, key):
        """taak_s u taf_ek raa and rii_trn_s u naann
        """
        taf_ek_strng = key.ser_ii_l_ish().feek_strng()
        return self.deks[taf_ek_strng]
    
    def __setitem__(self, key, value):
        """taak_s u taf_ek ash raa and u bet_naann ash gleff_raa
        """
        taf_ek_strng = key.ser_ii_l_ish().feek_strng()
        naann = Naann(value)
        self.deks[taf_ek_strng] = naann
    
    def __iter__(self):
        for taf_ek_strng, naann in self.deks.iteritems():
            yield Raa(daat_u=taf_ek_strng), naann
    
    def et_r_kii_sh(self):
        for taf_ek_strng in self.deks.iterkeys():
            yield Raa(daat_u=taf_ek_strng)
