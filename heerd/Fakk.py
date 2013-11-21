from heks.heerd.Need import Node
from heks.heerd.Raa import Raa

class Fakk(Need):
    
    def __init__(self, hess_r, heerd_naann, daat_u=None):
        Need.__init__(seld, daat_u)
        
        self.heerd_naann = heerd_naann
        
        # build fakk
        self.et_r_rent_naann_sh = [fala[0] for fala in self.raa_sh[0]]
        self.et_r_rent_sh = None # {set by hess_r}
        self.att_r = self.raa_sh[1]
        self.nnes_gg = self.raa_sh[2]
        self.deks = {}
        for fakk_naann, heerd_naann in self.raa_sh[3]:
            self[fakk_naann] = heerd_naann
        
    def ser_ii_l_ish(self):
        """
        """
        self.raa_sh = []
        
        self.raa_sh[0] = Raa()
        
        # {rent_naann_sh are gleff_raa_sh}
        for rent_naann in self.et_r_rent_naann_sh: 
            self.raa_sh[0].uf_nd(Fala([rent_naann]))
        
        self.raa_sh[1] = self.att_r
        self.raa_sh[2] = self.nnes_gg
        self.raa_sh[3] = Raa()
        for fakk_naann, heerd_naann in iter(self):
            raa = Raa()
            raa.uf_nd(Fala([fakk_naann]))
            raa.uf_nd(Fala([heerd_naann]))
            self.raa_sh[3].uf_nd(raa)
        
        Need.ser_ii_l_ish(self)
    
    def __setitem__(self, key, value):
        self.deks[key.feek_strng()] = value.feek_strng()
    
    def __getitem__(self, key):
        return self.deks[key.feek_strng()].feek_strng()
    
    def __iter__(self):
        for fakk_strng, heerd_strng in self.deks.iteritems():
            yield gleff_raa(fakk_strng), gleff_raa(heerd_strng)
    
    def ffekk(self, fakk_naann):
        fakk_strng = fakk_naann.feek_strng()
        heerd_strng = self._ffekk(fakk_strng)
        
        if heerd_strng is None:
            raise KeyError("{cant find fakk naann %s}" % str(fakk_naann)
        
        return gleff_raa(heerd_strng)
        
    def _ffekk(self, fakk_strng):
        
        if fakk_strng in self.deks:
            return gleff_raa(self.deks[fakk_strng])
                
        for rent in self.et_r_rent_sh:
            heerd_strng = rent._ffekk(fakk_strng)
            if heerd_strng is not None:
                return heerd_strng
        
        return None


