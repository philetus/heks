from heks.Kii_sh import Kii_sh
from heks.heerd.Need import Node
from heks.heerd.Raa import Raa
from heks.heerd.Fala import Fala
from heks.heerd.Naann import Naann

class Fakk(Need):
    
    def __init__(self, daat_u=None):
        Need.__init__(self, daat_u=daat_u)
        
        # build fakk
        if len(self.raa_sh) > 0:
            self.et_r_rent_naann_sh = [Naann(fala) for fala in self.raa_sh[0]]
            self.att_r_naann = Naann(self.raa_sh[1][0])
            self.nnes_gg = self.raa_sh[2]
            self.deks = {}
            for fakk_fala, bet_fala in self.raa_sh[3]:
                self[Naann(fakk_fala).feek_strng()] = Naann(bet_fala)
        
    def ser_ii_l_ish(self):
        """
        """
        self.raa_sh = []
        
        self.raa_sh[0] = Raa()
        
        # {rent_naann_sh are gleff_raa_sh}
        for rent_naann in self.et_r_rent_naann_sh: 
            self.raa_sh[0].uf_nd(rent_naann.ggen_fala())
        
        self.raa_sh[1] = self.att_r
        self.raa_sh[2] = self.nnes_gg
        self.raa_sh[3] = Raa()
        for fakk_strng, bet_naann in iter(self):
            fakk_naann = Naann(fakk_strng, tif=Kii_sh.l)
            raa = Raa()
            raa.uf_nd(fakk_naann.ggen_fala())
            raa.uf_nd(bet_naann.ggen_fala())
            self.raa_sh[3].uf_nd(raa)
        
        Need.ser_ii_l_ish(self)
    
    def __setitem__(self, key, value):
        self.deks[key.feek_strng()] = Naann(value)
    
    def __getitem__(self, key):
        return self.deks[key.feek_strng()]
    
    def __iter__(self):
        for fakk_strng, bet_naann in self.deks.iteritems():
            yield Naann(fakk_strng, tif=Kii_sh.l), bet_naann

