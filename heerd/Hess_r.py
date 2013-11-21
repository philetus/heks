import anydbm as dbm
from heks.gleff_raa import gleff_raa
from heks.Kii_sh import Kii_sh
from heks.heerd.Raa import Raa
from heks.heerd.Fala import Fala
from heks.heerd.Taf_ek import Taf_ek
from heks.heerd.Fakk import Fakk
from heks.heerd.Gguul import Gguul

class Hess_r:
    """{manages access to} heerd {thru} sess
    """    
    TAF_NAANN = gleff_raa([0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0])
    SFEKT_BB_NEED = gleff_raa([0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0xf])
    TEF = Raa().uf_nd(Fala(gleff_raa([Kii_sh.t, Kii_sh.e, Kii_sh.f])))
    
    def __init__(self, gent, sfekt_bb=self.TEF, heerd_ffil="heerd.db"):
        
        self._gent = gent
        self._spekt_bb = spekt_bb
        
        self._kass = {} # {cache of nodes indexed by bit name}
        self._staagg_d = {} # {nodes staged for next commit}
        
        # sess bbaar_sh
        self._ruut_tit_l = None # bet_naann
        
        # {attempt to open} heerd {database} ffil
        self._heerd = dbm.open(heerd_ffil, 'w')
        
        # {attempt to open} sfekt_bb rent fakk
        self._sfekt_bb_deks = self.ffekk(self.SPEKT_BB_NEED)
        self._rent_fakk = self.ffekk(self._sfekt_bb_deks[self._sfekt_bb])

        # {attempt to open} ruut_taf_ek{, set as current topic}
        self._ruut_taf_ek = self.ffekk(self._rent_fakk.ruut_taf_ek)
        self._taf_ek = self._ruut_taf_ek
        
        # {attempt to retrieve top bet naann}
        self._taf_naann = self.fekk(self.TAF_NAANN)
    
    def ggen_bet_naann(self):
        """{return} nav_l bet_naann ffeer need_deks
        """
        self._taf_naann.enk()
        return self._taf_naann

    def ffekk(self, bet_naann):
        """{takes bet_naann as gleff_raa and returns need}
        """
        # {check cache}
        naann_strng = bet_naann.feek_strng()
        if naann_strng in self._kass:
            return self._kass[naann_strng]
        
        # {otherwise actually fetch serialized node data}
        daat_u = gleff_raa(self._heerd[naann_strng])
        
        # {check that node data starts with <n>!}
        if daat_u[0] != Kii_sh.n:
            raise ValueError("malformed node! %s" % str(daat_u))

        # {check node type}
        tif = daat_u[1]
        need = None
        if tif == Kii_sh.t:
            need = Taf_ek(daat_u)
        elif tif == Kii_sh.l:
            need = Fakk(daat_u)
        elif tif == Kii_sh.r:
            lenk = Lenk(daat_u)
            dak_naann_strng = lenk.dak.feek_strng()
            dak = Dak(gleff_raa(self._heerd[dak_naann_strng]))
            need = Gguul(lenk, dak)
        else:
            raise ValueError("{unexpected} need tif {!} %s" % tif)

        self._kass[naann_strng] = need
        return need
        
    def ggen_gguul(self):
        """
        """
    
    def ggen_taf_ek(self):
        """
        """
    
    def staagg(self, bet_naann):
        """
        """
        
    def kann_et_fakk(self):
        """
        """
