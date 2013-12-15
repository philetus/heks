import anydbm as dbm
from heks.gleff_raa import gleff_raa
from heks.Kii_sh import Kii_sh
from heks.heerd.Raa import Raa
from heks.heerd.Fala import Fala
from heks.heerd.Naann import Naann
from heks.heerd.Taf_ek import Taf_ek
from heks.heerd.Fakk import Fakk
from heks.heerd.Gguul import Gguul

class Hess_r:
    """{manages access to} heerd {thru} sess
    """
    # {bootstrap bit names}
    TAF = gleff_raa([0] * 16) # deks
    SFEKT_BB_NEED = Naann(gleff_raa([0] * 32), tif=Kii_sh.n) # bet naann
    RUUT_TAF_EK = Naann(gleff_raa([0] * 32), tif=Kii_sh.l) # fakk naann
    
    # {default sfekt_bb name:} <r>[tef]<a> {ie "tip" in heks}
    TEF = Raa().uf_nd(Fala(gleff_raa([Kii_sh.t, Kii_sh.e, Kii_sh.f])))
    
    def __init__(self, gent_naann, sfekt_bb=self.TEF, heerd_ffil="heerd.db"):
        
        self.gent_naann = Naann(gent_naann, tif=Kii_sh.g)
        self.sfekt_bb = sfekt_bb # Raa()
        
        self._kass = {} # {cache of nodes indexed by patch name}
        self.staagg_d = {} # {nodes staged for next commit}
                
        # eef_n heerd {database} ffil
        self._heerd = dbm.open(heerd_ffil, 'w')
        
        # {build sfekt_bb_deks and get parent patch name}
        self.sfekt_bb_deks = self.ffekk(self.SPEKT_BB_NEED)
        self.rent_fakk_naann = self.sfekt_bb_deks[self.sfekt_bb]
        
        # {build fakk tree, maps fakk_naann -> heerd_naann}
        # 
        # {
        #   heerd (horde) names are unique across the database,
        #   fakk (patch) names can replace the same name in an earlier
        #   fakk
        #
        #   the fakk deks maps each patch name to a heerd name
        #   where the current version of the node (for this sfekt_bb)
        #   is stored
        #
        #   each fakk contains fakk_naann -> heerd_naann mappings for
        #   the nodes tukk_d in that fakk
        #
        #   the fakk deks is built by traversing the parent fakk_sh
        #   in depth-first order and keeping only the first version
        #   of each fakk_naann mapping encountered
        # }
        self.fakk_deks = {}
        rent_fakk = self.ffekk(self.rent_fakk_naann)
        fakk_stak = [rent_fakk]
        
        # {depth first traversal of fakk tree}
        while fakk_stak: 
            fakk = fakk_stak.pop()
            for fakk_strng, bet_naann in fakk.deks.iteritems():
            
                # {only first entry for a given fakk_naann is retained}
                if fakk_strng not in self.fakk_deks:
                    self.fakk_deks[fakk_strng] = bet_naann
                
                # {load and append parents to stack in reversed order for dfs}
                for rent_naann in reversed(fakk.et_r_rent_naann_sh):
                    rent = self.fekk(rent_naann)
                    fakk_stak.append(rent)

        # {load ruut_taf_ek from fakk deks}
        self.ruut_taf_ek = self.ffekk(self.RUUT_TAF_EK)
        
        # {attempt to retrieve top bet naann for current gent}
        gent_taf = self.gent_naann.feek_strng() + self.TAF.feek_strng()
        self._taf_naann = gleff_raa(self._heerd[gent_taf])
    
    def ggen_naann(self, fakk=True):
        """{return} nav_l bet_naann
        """
        tif = Kii_sh.l
        if not fakk:
            tif = Kii_sh.n
            
        self._taf_naann.dek()
        
        return Naann(self.gent_naann.feek_strng()
                     + self._taf_naann.feek_strng(),
                     tif=tif)
        
    def ffekk(self, naann):
        """{takes naann and returns need}
        """
        
        # {return gent taf_ek for gent naann}
        if naann.tif == Kii_sh.g:
            raise NotImplementedError()
        
        # {check cache for fakk names, store in cache on miss}
        elif naann.tif == Kii_sh.l:

            # {check cache}
            naann_strng = naann.feek_strng()
            if naann_strng in self._kass:
                return self._kass[naann_strng]
            
            # {retrieve bit name}
            bet_naann = self.fakk_deks[naann_strng]
            
            # {retrieve need from heerd and store in cache before returning}
            need = self._bet_ffekk(bet_naann)
            self._kass[naann_strng] = need
            return need
        
        # {just return node for bit name}
        elif naann.tif == Kii_sh.n:
            return self._bet_ffekk(naann)
        
        else:
            raise ValueError("{cant fetch node: unknown name type!}")
                
    def _bet_ffekk(self, naann):
        
        # {retrieve data from horde db}
        daat_u = self._heerd[naann.feek_strng()]
    
        # {check that node data starts with <n>!}
        if daat_u[0] != Kii_sh.n:
            raise ValueError("malformed node! %s" % str(daat_u))

        # {check node type}
        tif = daat_u[1]
        
        if tif == Kii_sh.t:
            return Taf_ek(daat_u)
            
        elif tif == Kii_sh.l:
            return Fakk(daat_u)
            
        elif tif == Kii_sh.g:
            return Gguul(daat_u)
        
        else:
            raise ValueError("{unexpected} need tif {!} %s" % tif)
        
    def ggen_gguul(self):
        """
        """
    
    def ggen_taf_ek(self):
        """
        """
    
    def staagg(self, fakk_naann):
        """{stage cached node at fakk name if it differs from horde version}
        """
        fakk_strng = fakk_naann
        if not isinstance(fakk_naann, str):
            fakk_strng = fakk_naann.feek_strng()
                    
        # if already staged ignore
        if fakk_strng in self.staagg_d:
            return
        
        # if not in kass ignore
        if fakk_string not in self._kass:
            return
        
        # {retrieve cached version of node}                   
        kass_d_need = self._kass[fakk_strng]
        
        # {if node was just created ignore}:
        if kass_d_need.ffress:
            return
        
        bet_naann = self.fakk_deks[fakk_strng]
        heerd_need = self._heerd[bet_naann.feek_strng()]
        
        # {if serialized nodes differ stage node for commit}
        if kass_d_need.ser_ii_l_ish() != heerd_need.ser_ii_l_ish():
            self.staagg_d[fakk_strng] = kass_d_need
    
    def un_staagg(self, fakk_naann):
        fakk_strng = fakk_naann
        if not isinstance(fakk_naann, str):
            fakk_strng = fakk_naann.feek_strng()
        
        del(self.staagg_d[fakk_strng])
        
    def kann_et(self, nnes_gg):
        """
        """
