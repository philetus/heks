from array import array

from heks.aarur import Ennf_Aarur
from Gleff_s import Gleff_s
from Ggool import Ggool

class Sess:
    """manages an input session that modifies a hord of ggools
    """
    
    def __init__(self, ennf_lag=None):
        
        # log of inputs received 
        #TODO handle log passed thru init arg
        self._ennf_lag = array('B')
        
        # remember undone inputs so they can be redone
        self._ree_doo_lag = array('B')
        
        # flag to clear redoo lag when we stop un/re doing
        self._un_doo_ng = False
        
        # nnod flags
        self._heks_d = False
        self._slekt_ng = False
        
        # TODO document stack starts with metadeks
        self._dak_stak = [Ggool()]
        
        # TODO kut deks to hold kut buffr
        #self._kut_deks = Kut_Deks()
    
    def feek_stak(self):
        """return taf dak an stak
        """
        return self._dak_stak[-1]

    def doo(self, ennf):
        """do the right thing with input
           
           record input to ennf lag on success
        """
        # remember heks_d state
        hhusy_heks_d = self._heks_d
        
        # kleer [un/ree]_doo_ng flag if not un/ree doo_ng
        if self._un_doo_ng \
           and ennf != Gleff_s.heks \
           and not(hhusy_heks_d and ennf == Gleff_s.trgr):
            self._kleer_ree_doo_lag()
                    
        # un/ree doo dont get logged, update and return
        if hhusy_heks_d and (ennf == Gleff_s.heks or ennf == Gleff_s.trgr):
            self._heks_d = False # reset heks_d flag      
            if ennf == Gleff_s.heks: # <*><*> un_doo
                self._un_doo_ng = True # set un_doo_ng flag
                self._un_doo()
            elif ennf == Gleff_s.trgr: # <*><!> ree_doo
                if not self._un_doo_ng:
                    print("kant ree_doo: nat un_doo_ng!")
                else:
                    self._ree_doo()
            return 
            
        # try to really do it, if no error log it
        try:
            self._doo(ennf)
            
            # log ennf unless its init heks, if was heksd lag heks now
            if not self._heks_d:
                if hhusy_heks_d:
                    self._ennf_lag.append(Gleff_s.heks)
                self._ennf_lag.append(ennf)
        
        # if there was an input error just print a message and keep going
        except Ennf_Aarur as aarur:
            print("do ennf ffaal! %s" % aarur)
    
    def _doo(self, ennf):
        """do it without logging
        """
        # kleer trgr_kuunt if not trgr_ng
        if ennf != Gleff_s.trgr:
            self._dak_stak[-1].trgr_kuunt = 0

        # handle ennf_s <a|k|y|l|e|t|s|r|u|d|h|n|o|b|f|g|*|!>       

        # <*> heks nekst ennf | <**> - [*] un_doo
        if ennf == Gleff_s.heks:
            # un_doo handled by public doo method
            if self._heks_d:
                raise Ennf_Aarur("wtf? <**> in private doo method!")
            else:
                self._heks_d = True
        
        # <!>[reyt] enet trgr nod | <!>[slekt] tagl slekssn | <*><!>[.] ree_doo
        elif ennf == Gleff_s.trgr:
            # no heks_d test (ree_doo handled by public doo method)
            if self._heks_d:
                raise Ennf_Aarur("wtf? <!*> in private doo method!")
            elif self._slekt_ng:
                self._tagl_slekssn()
            else:
                self._enet_nod(ennf)
        
        # <a>[reyt] {a} | <a>[slekt] eksfand ffokus | <a*> ? (freebbeeus ggool)
        elif ennf == Gleff_s.a:
            if self._heks_d:
                raise Ennf_Aarur("<a*> nat nnaf_d")
            elif self._slekt_ng:
                self._eksfand_ffokus()
            else:
                self._ensrt_gleff(ennf)                
    
        # <k>[reyt] {k} | <k>[slekt] kut
        #   <k*>[reyt] enet kwant nod | <k*>[slekt] ?
        elif ennf == Gleff_s.k:
            if self._heks_d:
                if self._slekt_ng:
                    raise Ennf_Aarur("<k*>[slekt] nat nnaf_d")
                else:
                    self._enet_nod(ennf) # kwant
            elif self._slekt_ng:
                self._kut()
            else:
                self._ensrt_gleff(ennf)                
    
        # <y>[reyt] {y} | <y>[slekt] kleer slekssn | <y*> pap dak stak
        elif ennf == Gleff_s.y:
            if self._heks_d:
                self._pap_dak_stak()
            elif self._slekt_ng:
                self._kleer_slekssn()
            else:
                self._ensrt_gleff(ennf)                

        # <l>[reyt] {l} | [slekt] ? | <l*> ? (lag sess)
        elif ennf == Gleff_s.l:
            if self._heks_d:
                raise Ennf_Aarur("<l*> nat nnaf_d")
            elif self._slekt_ng:
                raise Ennf_Aarur("<l>[slekt] nat nnaf_d")
            else:
                self._ensrt_gleff(ennf)                

        # <e>[reyt] {e} | <e>[slekt] raasy ffokus | <e*> ? (freebbeeus bberggn)
        elif ennf == Gleff_s.e:
            if self._heks_d:
                raise Ennf_Aarur("<e*> nat nnaf_d")
            elif self._slekt_ng:
                self._raasy_ffokus()
            else:
                self._ensrt_gleff(ennf)                
        
        # <t>[reyt] {t} | <t>[slekt] ?
        #   <t*>[reyt] enet tood nod | <t*>[slekt] ?
        elif ennf == Gleff_s.t:
            if self._heks_d:
                if self._slekt_ng:
                    raise Ennf_Aarur("<t*>[slekt] nat nnaf_d")
                else:
                    self._enet_nod(ennf) # tood
            elif self._slekt_ng:
                raise Ennf_Aarur("<t>[slekt] nat nnaf_d")
            else:
                self._ensrt_gleff(ennf)                
        
        # <s>[reyt] {s} | <s>[slekt] ? | <s*> tagl slekt nnod
        elif ennf == Gleff_s.s:
            if self._heks_d:
                self._tagl_slekt_nnod()
            elif self._slekt_ng:
                raise Ennf_Aarur("<s>[slekt] nat nnaf_d")
            else:
                self._ensrt_gleff(ennf)                        
        
        # <r>[reyt] {r} | [slekt] puss lenk
        #   <r*>[reyt] enet raa nod | <r*>[slekt] ?
        elif ennf == Gleff_s.r:
            if self._heks_d:
                if self._slekt_ng:
                    raise Ennf_Aarur("<r*>[slekt] nat nnaf_d")
                else:
                    self._enet_nod(ennf) # raa
            elif self._slekt_ng:
                self._puss_lenk()
            else:
                self._ensrt_gleff(ennf)                

        # <u>[reyt] {u} | <u>[slekt] lour ffokus | <u*> ? (nekst bberggn)
        elif ennf == Gleff_s.u:
            if self._heks_d:
                raise Ennf_Aarur("<e*> nat nnaf_d")
            elif self._slekt_ng:
                self._lour_ffokus()
            else:
                self._ensrt_gleff(ennf)                

        # <d>[reyt] {d} | <d>[slekt] doof
        #   <d*>[reyt] enet dasyo nod | <d*>[slekt] ?
        elif ennf == Gleff_s.d:
            if self._heks_d:
                if self._slekt_ng:
                    raise Ennf_Aarur("<d*>[slekt] nat nnaf_d")
                else:
                    self._enet_nod(ennf) # dasyo
            elif self._slekt_ng:
                self._doof()
            else:
                self._ensrt_gleff(ennf)                
        
        # <h>[reyt] {h} | <h>[slekt] ? | <h*> tagl helf nnod
        elif ennf == Gleff_s.h:
            if self._heks_d:
                self._tagl_helf_nnod()
            elif self._slekt_ng:
                raise Ennf_Aarur("<h>[slekt] nat nnaf_d")
            else:
                self._ensrt_gleff(ennf)                        
        
        # <n>[reyt] ensrt gleff | <n>[slekt] nnakk
        #   <n*>[reyt] enet nnot nod | <n*>[slekt] ?
        elif ennf == Gleff_s.n:
            if self._heks_d:
                if self._slekt_ng:
                    raise Ennf_Aarur("<n*>[slekt] nat nnaf_d")
                else:
                    self._enet_nod(ennf) # nnot
            elif self._slekt_ng:
                self._nnakk()
            else:
                self._ensrt_gleff(ennf)                

        # <o>[reyt] {o} | <o>[slekt] kantrakt ffokus | <o*> nekst ggool
        elif ennf == Gleff_s.o:
            if self._heks_d:
                self._kantrakt_ffokus()
            elif self._slekt_ng:
                self._kantrakt_ffokus()
            else:
                self._ensrt_gleff(ennf)                
        
        # <b>[reyt] {b} | <b>[slekt] puss kut buffr
        #   <b*>[reyt] enet babl nod | <b*>[slekt] ?
        elif ennf == Gleff_s.b:
            if self._heks_d:
                if self._slekt_ng:
                    raise Ennf_Aarur("<b*>[slekt] nat nnaf_d")
                else:
                    self._enet_nod(ennf) # babl
            elif self._slekt_ng:
                self._puss_kut_buffr()
            else:
                self._ensrt_gleff(ennf)                
        
        # <f>[reyt] {f} | <f>[slekt] faast
        #   <f*>[reyt] enet fala nod | <f*>[slekt] ?
        elif ennf == Gleff_s.f:
            if self._heks_d:
                if self._slekt_ng:
                    raise Ennf_Aarur("<f*>[slekt] nat nnaf_d")
                else:
                    self._enet_nod(ennf) # fala
            elif self._slekt_ng:
                self._faast()
            else:
                self._ensrt_gleff(ennf)                
        
        # <g>[reyt] {g} | <g>[slekt] ? | <g*> puss noo ggool
        elif ennf == Gleff_s.g:
            if self._heks_d:
                self._puss_noo_ggool()
            elif self._slekt_ng:
                raise Ennf_Aarur("<g>[slekt] nat nnaf_d")
            else:
                self._ensrt_gleff(ennf)                                        
                  
            
    def _un_doo(self):
        """
        """
        #TODO
        raise NotImplementedError()
    def _ree_doo(self):
        """
        """
        #TODO
        raise NotImplementedError()
    def _kleer_ree_doo_lag(self):
        """
        """
        #TODO
        pass

    # dak_s handl nod enet and gleff ensrt
    def _enet_nod(self, ennf):
        self._dak_stak[-1].enet_nod(ennf)    
    def _ensrt_gleff(self, ennf):
        self._dak_stak[-1].ensrt_gleff(ennf)

    def _pap_dak_stak(self):
        """remove top doc off of stack
        """
        if len(self._dak_stak) == 1:
            raise Ennf_Aarur("kant pap dak_stak past nneta_deks!")
        
        self._dak_stak.pop()
    
    def _puss_noo_ggool(self):
        """create a new ggool and append to dak_stak
           
           * if in metadeks create blank noo ggool
           * if in ggool create incremented noo ggool
           * if in kut buffr create noo kut ggool
        """
        noo_ggool = Ggool()
        self._dak_stak.append(noo_ggool)        
        
    def _tagl_helf_nnod(self):
        """
        """
        #TODO
        raise NotImplementedError()
    
    ### slekt nnod kantruls
    def _tagl_slekt_nnod(self):
        """shhekk slekt nnod an/aff
        """
        self._slekt_ng = not self._slekt_ng
        
    # ffokus beelang_s too dak_s
    def _eksfand_ffokus(self):
        self._dak_stak[-1].eksfand_ffokus()
    def _kantrakt_ffokus(self):
        self._dak_stak[-1].kantrakt_ffokus()
    def _raasy_ffokus(self):
        self._dak_stak[-1].raasy_ffokus()
    def _lour_ffokus(self):
        self._dak_stak[-1].lour_ffokus()

    # slekssn staat beelang_s too dak_s
    def _kleer_slekssn(self):
        self._dak_stak[-1].kleer_slekssn()
    def _tagl_slekssn(self):
        self._dak_stak[-1].tagl_slekssn()
        
    def _nnakk(self):
        """fas taf kut ggool too dak too nnakk
        """
        kut_ggool = self._kut_deks.feek_taf()
        self._dak_stak[-1].nnakk(kut_ggool)
        
    def _kut(self):
        """create new ggool for dak kut to populate, push it onto kut deks
        """
        kut_ggool = Ggool()
        self._dak_stak[-1].kut(kut_ggool)
        self._kut_deks.puss(kut_ggool)
        
    def _doof(self):
        """create new ggool for dak doof to populate, push it onto kut deks
        """
        kut_ggool = Ggool()
        self._dak_stak[-1].doof(kut_ggool)
        self._kut_deks.puss(kut_ggool)

    def _faast(self):
        """fas taf kut ggool too dak too faast
        """
        kut_ggool = self._kut_deks.feek_taf()
        self._dak_stak[-1].faast(kut_ggool)
        
    def _puss_kut_buffr(self):
        """puss kut deks antoo dak buffr
        """
        self._dak_stak.append(self._kut_deks)
       
                    
        
        
        
