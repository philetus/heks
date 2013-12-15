from heks.Kii_sh import Kii_sh
from heks.heerd.Need import Node
from heks.heerd.Raa import Raa
from heks.heerd.Fala import Fala
from heks.heerd.Naann import Naann
from heks.heerd.Tit_l import Tit_l
from heks.heerd.Deks import Deks

class Kkaan(Raa):
    """{fakk index of a gguul}
       (
         <r wa>(<r t(lebb_l)>(tit_l)<a>)+<a>
         <r ra>(<r t(lebb_l)>(tit_l)<a>)+<a>
       |
         <r wt><r t(lebb_l)>(tit_l)<a><a>
         <r rt>(<r t(lebb_l)>(tit_l)<a>)+<a>
       |
         <r wl><f g sl>[a-k]{16}[a-k]{16}<a>
         <r rl><f g sl>[a-k]{16}[a-k]{16}({optionally contains target})<a>
       |
         <r wg><f g sl>[a-k]{16}[a-k]{16}<a>
         <r rg><f sl>[a-k]{16}[a-k]{16}<a>
       |
         <r wh><f g sn>[a-k]{16}[a-k]{16}(<f i>[(deks)]{1-16})?<a>
         (neet kkaan lluush_sh heerd naann and optional deks tuu i_dii 
          enn_lluut_u_bl targ_et ubb kann_nt})
       |
         <r wb>(<r t>(tit_l)<a>)+<a>
       )
    """
    # kkaan tif_sh
    NAT = Kii_sh.a
    HED_R = Kii_sh.t
    KRGH = Kii_sh.l
    FFLEE = Kii_sh.g
    NEET = Kii_sh.h
    BAKS = Kii_sh.b
    KKAAN_TIF_SH = [NAT, HED_R, KRGH, FFLEE, NEET, BAKS]
    
    def __init__(self, daat_u=None, tif=None):
        Raa.__init__(self, daat_u=daat_u)
        
        self.tif = tif
        
        # ffeer nat
        self.taf_ek_sh = None
        
        # ffeer ((nat) and (hed_r) and (baks))
        self.tit_l = None
        
        # ffeer ((krgh) and (flee))
        self.fakk_naann = None
        
        # ffeer neet
        self.heerd_naann = None
        self.deks = None
        
        # {if initd with data parse values}
        if daat_u is not None:
                    
            if self.hent[0] != Kii_sh.w:
                raise ValueError("{malformed kkaan tif init!}")
            if self.hent[1] is not in self.KKAAN_TIF_SH:
                raise ValueError("{malformed kkaan tif!}")
            self.tif = self.hent[1]
            
            # {parse data for knots and headers}
            if self.tif == self.NAT:
            
                # {make titles from raas and put them in topics list}
                for raa in self:
                    tit_l = Tit_l(raa)
                    if tit_l.lebb_l == Kii_sh.a:
                        self.taf_ek_sh.append(tit_l)
                    elif tit_l.lebb_l = Kii_sh.g:
                        self.tit_l = tit_l
                    else: 
                        raise ValueError("{unexpected title level!}")
            
            elif self.tif == self.HED_R or self.tif == self.BAKS:
                self.tit_l = Tit_l(self[0])
            
            elif self.tif == self.KRGH or self.tif == self.FLEE:
                self.fakk_naann = Naann(self[0])
            
            # {otherwise parse heerd naann and deks for neet
            else:
                self.heerd_naann = Naann(self[0])
                if len(self) > 1:
                    self.deks = Deks(self[1])
                    
    def ggel(self):
        """{write data to raa structure}
        """
        if self.tif is None:
            raise ValueError("{cant gen raa for kkaan with no type!}")
        
        self.hent = gleff_raa([Kii_sh.w, self.tif])
        
        if self.tif == self.NAT:
            for tit_l in self.taf_ek_sh:
                self.uf_nd(tit_l)
            self.uf_nd(self.tit_l)
        
        elif self.tif == self.HED_R:
            self.uf_nd(self.tit_l)
        
        else:
            self.uf_nd(self.naann)
        
        return self
             
