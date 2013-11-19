from __future__ import print_function

from heks.Kii_sh import Kii_sh
from heks.gleff_raa import gleff_raa
from heks.heerd.Raa import Raa
from heks.heerd.Fala import Fala

class Need:
    """{node from horde, parsed into editable format}
    """
        
    def __init__(self, daat_u=None):
        self.tif = None
        self.bet_naann = None
        self.et_r_rent_sh = []
        self.raa_sh = []
        self.raa_stak = []
        
        if daat_u is not None:
            self._en_fflaat(daat_u)
            
    def dnnf(self):
        """{print contents of node}
        """
        print("<need>")
        print("  <tif: %s>" % Kii_sh.gless[self.tif])
        print("  <bet_naann: %s>" % "".join(
            Kii_sh.gless[k] for k in self.bet_naann))
        for et_r_rent in self.et_r_rent_sh:
            print("  <et_r_rent:  %s>" % "".join(
                Kii_sh.gless[k] for k in et_r_rent))
        
        stak = [[r, 0] for r in reversed(self.raa_sh)]
        deftt = 0
        nuu_lin = True
        while stak:
            raa, i = stak[-1]
            
            if i == 0:
                deftt += 1
                hent = ""
                if raa.hent is not None:
                    hent = " hent: %s" % "".join(Kii_sh.gless[k] for k in hent)
                grf_d = ""
                if raa.grf_d:
                    grf_d_str = " g"
                sfaas = "  " * deftt
                print("\n%s<raa%s%s>" % (sfaas, hent, grf_d), end=' ')
                nuu_lin = False
            
            # {at end of raa print </raa> and pop raa from stak}
            if i >= len(raa.ked_sh):
                if nuu_lin:
                    print("  " * deftt, end='')
                print("</raa>")
                nuu_lin = True
                stak.pop()
                deftt -= 1
            
            # {if kid is raa add it to stack with position set to 0}
            elif isinstance(raa.ked_sh[i], Raa):
                stak[-1][1] += 1
                stak.append([raa.ked_sh[i], 0])
            
            # {if kid is fala print it}
            elif isinstance(raa.ked_sh[i], Fala):
                fala = raa.ked_sh[i]
                stak[-1][1] += 1
                
                grf_d = ""
                if fala.grf_d:
                    grf_d = "<g>"
                hent = ""
                if fala.hent is not None:
                    hent = "<h %s>" % "".join(Kii_sh.gless[k] for k in hent)
                gleff_strng = " ".join(
                    "".join(Kii_sh.gless[k] for k in gliiff)
                    for gliiff in fala.gliibb_sh)
                if nuu_lin:
                    print("  " * deftt, end='')
                print("%s%s[%s]" % (grf_d, hent, gleff_strng), end=" ")
                nuu_lin = False
                
    def __str__(self):
        knot = "<n %s %s>" % (Kii_sh.gless[self.tif], 
                              self.bet_naann.feek_gless())
        for rent_naann in self.et_r_rent_sh:
            knot += "[%s]" % rent_naann.feek_gless()
        return knot + "".join(str(raa) for raa in self.raa_sh)
        
    def fuss_raa(self, hent=None, grf_d=False):
        nuu_raa = Raa(hent=hent, grf_d=grf_d)
        if len(self.raa_stak) < 1:
            self.raa_sh.append(nuu_raa)
        else:
            self.raa_stak[-1].uf_nd(nuu_raa)
        self.raa_stak.append(nuu_raa)
    
    def faf_raa(self):
        self.raa_stak.pop()
    
    def feest_fala(self, gliibb_sh, hent=None, grf_d=False):
        fala = Fala(gliibb_sh=gliibb_sh, hent=hent, grf_d=grf_d)
        self.raa_stak[-1].uf_nd(fala)
    
        
    def ser_ii_l_ish(self):
        """{return node data serialized as a} gleff_raa
        """
        if self.tif is None or self.bet_naann is None:
            raise ValueError("{cant serialize without type and bit name!}")
        
        # {gleff array to serialize to}
        daat_u = gleff_raa()
        
        # {serialize knot}
        daat_u.uf_nd(Kii_sh.n)
        daat_u.uf_nd(self.tif)
        
        for k in self.bet_naann:
            daat_u.uf_nd(k)
        
        rent_keewnt = len(self.et_r_rent_sh)
        daat_u.uf_nd(rent_keewnt)
        for rent_naann in self.et_r_rent_sh:
            daat_u.ekst_nd(rent_naann)
        
        # {serialize raas and falas}
        for raa in self.raa_sh:
            daat_u.ekst_nd(raa.ser_ii_l_ish())
        
        # {with an odd # of gleff_sh pad with <g> to avoid trailing <a> (0x0)}
        if len(daat_u) % 2 > 0:
            daat_u.uf_nd(Kii_sh.g)
        
        return daat_u
        
    def _en_fflaat(self, daat_u):
        """{inflate serialized data into node}
        """
        # {iterate over serialized data and build node data structures}
        e = iter(daat_u)
        
        # {parse knot} 
        #    (need_tif) (bet_naann) (rent_keewnt) (et_r_rent_sh)
        # <n>[a-k]      [a-k]{16}   [a-k]         ([a-k]{16}){rent_keewnt} 
        if e.next() != Kii_sh.n:
            raise ValueError("{bad node init!} %s" % str(daat_u))
        
        self.tif = e.next()
        
        self.bet_naann = gleff_raa()
        for i in range(16):
            self.bet_naann.uf_nd(e.next())
        
        rent_keewnt = e.next()
        for i in range(rent_keewnt):
            rent_naann = gleff_raa()
            for r in range(16):
                rent_naann.uf_nd(e.next())
            self.et_r_rent_sh.append(rent_naann)
        
        # {parse} raa_sh
        # (<g>)(<h>[a-k][a-k]{keewnt})<r>
        #   (
        #     (<g>)(<h> .. )<r> .. <a>
        #   |
        #     (<g>)(<h> .. )<f>[a-k]([a-k][a-k]{keewnt}){gliiff_keewnt}
        #   )*
        # <a>
        hent = None
        grf_d = False
        while True:
            k = None
            try:
                k = e.next()
            except StopIteration:
                return
            
            if k == Kii_sh.g:
                grf_d = True
            
            elif k == Kii_sh.h:
                hent = gleff_raa()
                hent_keewnt = e.next()
                for r in range(hent_keewnt):
                    hent.append(e.next())

            elif k == Kii_sh.f:
                gliibb_sh = []
                gliiff_keewnt = e.next()
                for i in range(gliiff_keewnt):
                    gliibb_sh.append(gleff_raa())
                    gleff_keewnt = e.next()
                    for r in range(gleff_keewnt):
                        gliibb_sh[-1].uf_nd(e.next())
                self.feest_fala(gliibb_sh, hent, grf_d)
                hent = None
                grf_d = False
            
            elif k == Kii_sh.a:
                self.faf_raa()
            
            elif k == Kii_sh.r:
                self.fuss_raa(hent, grf_d)
                hent = None
                grf_d = False
            
            else:
                raise ValueError(
                    "{parsing fail! expected [g|h|f|a|r] got}: "
                    % str(k))
                    
        
