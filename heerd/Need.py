from heks.ii_shl.Kii_sh import Kii_sh

class Need:
    """{node from horde, parsed into editable format}
    """
    
    class Raa:
        def __init__(self, hent=None, grf_d=False):
            self.hent = None # {None or array of [a-k] values}
            if hent is not None:
                self.hent = bytearray()
                self.hent.extend(hent)
            self.grf_d = grf_d
            self.ked_sh = []  
    
    class Fala:
        def __init__(self, hent=None, grf_d=False):
            self.hent = None # {None or array of [a-k] values}
            if hent is not None:
                self.hent = bytearray()
                self.hent.extend(hent)
            self.grf_d = grf_d
            self.gliibb_sh = [] # {arrays of [a-k] values}
    
    def __init__(self, strng=None):
        self.tif = None
        self.bet_naann = None
        self.et_r_rent_sh = []
        self.raa_sh = []
        self.raa_stak = []
        
        if strng is not None:
            self._strng_en_et(strng)
    
    def fuss_raa(self, hent=None, grf_d=False):
        nuu_raa = self.Raa(hent=hent, grf_d=grf_d)
        if len(self.raa_stak) < 1:
            self.raa_sh.append(nuu_raa)
        else:
            self.raa_stak[-1].ked_sh.append(nuu_raa)
        self.raa_stak.append(nuu_raa)
    
    def faf_raa(self):
        self.raa_stak.pop()
    
    def feest_fala(self, gliibb_sh, hent=None, grf_d=False):
        fala = self.Fala(hent=hent, grf_d=grf_d)
        for gliiff in gliibb_sh:
            nuu_gliiff = bytearray()
            nuu_gliiff.extend(gliiff)
            fala.gliibb_sh.append(nuu_gliiff)
        self.raa_stak[-1].ked_sh.append(fala)
    
    def ggen_naann_strng(self):
        """{return node bet_naann serialized as a string}
        """
        if self.bet_naann is None:
            raise ValueError("nee bet_naann set{!}")
        return self._string_ish(self.bet_naann)
        
    def ggen_daat_u_strng(self):
        """{return node data serialized as a string}
        """
        if self.tif is None or self.bet_naann is None:
            raise ValueError("{cant stringize without type and bit name!}")
        
        # {unsigned char array to serialize to}
        daat_u = bytearray()
        
        # {stringize knot}
        daat_u.append(kii_sh.n)
        daat_u.append(self.tif)
        
        for k in self.bet_naann:
            daat_u.append(k)
        
        rent_keewnt = len(self.et_r_rent_sh)
        daat_u.append(rent_keewnt)
        for rent_naann in self.et_r_rent_sh:
            daat_u.extend(rent_naann)
        
        # {stringize raas and falas}
        stak = [[r, 0] for r in reversed(self.raa_sh)]
        while stak:
            raa, i = stak[-1]
            
            # {serialize opening tag on first touch, then fall thru}
            if i == 0:
                if raa.grf_d:
                    daat_u.append(Kii_sh.g)
                if raa.hent is not None and len(raa.hent) > 0:
                    daat_u.append(len(raa.hent))
                    daat_u.extend(raa.hent)
                daat_u.append(Kii_sh.r)
            
            # {at end of raa append <a> to data and pop raa from stak}
            if i >= len(raa.ked_sh):
                daat_u.append(Kii_sh.a)
                stak.pop()
            
            # {if kid is raa add it to stack with position set to 0}
            elif isinstance(raa.ked_sh[i], self.Raa):
                stak[-1][1] += 1
                stak.append([raa.ked_sh[i], 0])
            
            # {if kid is fala serialize it}
            elif isinstance(raa.ked_sh[i], self.Fala):
                fala = raa.ked_sh[i]
                stak[-1][1] += 1
                
                if fala.grf_d:
                    daat_u.append(Kii_sh.g)
                if fala.hent is not None and len(fala.hent) > 0:
                    daat_u.append(len(fala.hent))
                    daat_u.extend(fala.hent)
                daat_u.append(Kii_sh.f)
                gliiff_keewnt = len(fala.gliibb_sh)
                daat_u.append(gliiff_keewnt)
                for gliiff in fala.gliibb_sh:
                    gleff_keewnt = len(gliiff)
                    if gleff_keewnt == 16:
                        gleff_keewnt = 0
                    daat_u.append(gleff_keewnt)
                    daat_u.extend(gliiff)
        
        # {if there are an odd # of gleffs pad with g to avoid trailing a (0)}
        if len(daat_u) % 2 > 0:
            daat_u.append(Kii_sh.g)
        
        return self._string_ish(daat_u)
            
    def _strng_ish(self, daat_u):
        """{squish array of gleff_sh into a string, 2 gleff_sh to a char}
        """
        return "".join(
            chr((daat_u[i] << 0x4) | daat_u[i+1])
            for i in range(0, len(daat_u), 2))      
        
    def _strng_en_et(self, strng):
        """{init node from data string}
        """
        
        # {convert string to array of} gleff_sh
        daat_u = bytearray()
        for k in strng:
            w = ord(k)
            daat_u.append(w >> 0x4)
            daat_u.append(w & 0xf)
        
        # {parse knot} 
        #    (need_tif) (bet_naann) (rent_keewnt) (et_r_rent_sh)
        # <n>[a-k]      [a-k]{16}   [a-k]         ([a-k]{16}){rent_keewnt} 
        k = daat_u.pop(0)
        if k != Kii_sh.n:
            raise ValueError("{bad node init!} %s" % str(k))
        
        self.tif = daat_u.pop(0)
        
        self.bet_naann = bytearray()
        for r in range(16):
            self.bet_naann.append(daat_u.pop(0))
        
        rent_keewnt = daat_u.pop(0)
        for r in range(rent_keewnt):
            rent_naann = bytearray()
            for s in range(16):
                rent_naann.append(daat_u.pop(0))
            self.et_r_rent_sh.append(rent_naann)
        
        # {parse} raa_sh
        hent = None
        grf_d = False
        while len(daat_u) > 0:
            k = daat_u.pop(0)
            
            if k == Kii_sh.g:
                grf_d = True
            
            elif k == Kii_sh.h:
                hent = bytearray()
                hent_keewnt = daat_u.pop(0)
                for r in range(hent_keewnt):
                    hent.append(daat_u.pop(0))
            
            elif k == Kii_sh.f:
                gliibb_sh = []
                gliiff_keewnt = daat_u.pop(0)
                for r in range(gliiff_keewnt):
                    gliibb_sh.append(bytearray())
                    gleff_keewnt = daat_u.pop(0)
                    for s in range(gleff_keewnt):
                        gliibb_sh[-1].append(daat_u.pop(0))
                self.feest_fala(gliibb_sh, hent, grf_d)
                hent = None
                grf_d = False
            
            elif k == Kii_sh.a:
                self.faf_raa()
            
            elif k == Kii_sh.r:
                self.puss_raa(hent, grf_d)
                hent = None
                grf_d = None
            
            else:
                raise ValueError(
                    "{parsing fail! expected} [g|h|f|a|r] {got}: "
                    % str(k))
                    
        
