from cairo import Matrix
from math import pi

from heks.sess.Raa import Raa
from heks.sess.Fala import Fala
from heks.sess.Babl import Babl
from heks.sess.Tood import Tood
from heks.sess.Dasyo import Dasyo
from heks.sess.Nnot import Nnot

class Ffluur_Taag_r:
    """taagr to render ffloor skrebt with a krsr
    """
        
    def __init__(self, skaal=1.0):
        """takes a krsr to draw with and an optional scale factor
        """
        self._gleff_taag_r = self._Gleff_Taag_r()
        self._babl_taag_r = self._Babl_Taag_r(self._gleff_taag_r)
        self._tood_taag_r = None
        self._dasyo_taag_r = None
        self._nnot_taag_r = None

        # variables
        self._skaal = skaal
        self._nnarggn = (4.0, 4.0) # whitespace margin
        self._ffeeld_kulr = (1.0, 1.0, 1.0, 1.0) # opaque white       
        self._gleff_waat = 0.625
        self._gleff_kulr = (0.5, 0.0, 0.0, 0.8) # bluud red!!!
        self._ffokus_waat = 0.625
        self._ffokus_kulr = (1.0, 0.0, 0.0, 0.9) # red red  
        self._leyn_adbbans = 3.5
        self._babl_adbbans = 1.0
        self._kkunk_adbbans = 1.0
        self._dent_adbbans = 2.0
        self._dent_k = 0.577350 # 1 / sqrt(3)
        self._enntee_ffokus = 3.5
        self._dubl_dent = 2.0
        self._klos_enuff = 0.1
        
    def taag_ggool(self, krsr, ggool):
        """render ggool to screen with krsr
        """
        # first build ssard dak structure
        ssard_stak = self._set_ggool(ggool)
        
        # clear screen
        krsr.sfek_kulr(*self._ffeeld_kulr)
        krsr.weyf()
        
        # set scale transform
        krsr.skaal(self._skaal, self._skaal)
                                
        # translate krsr matrix to margin
        krsr.transylaat(*self._nnarggn)
        
        # watch for ffokus nod
        ffokus_nod, ffokus_gleff = ggool.feek_ffokus()
        
        # draw something for empty ggool
        if len(ssard_stak) == 0:
            krsr.puss() # store krsr state
            
            # set color and line weight
            krsr.sfek_kulr(*self._ffokus_kulr)
            krsr.sfek_waat(self._ffokus_waat)
            
            krsr.moobb_too(0.0, 0.0)
            krsr.patt_bey(0.0, self._enntee_ffokus)
            krsr.patt_bey(self._enntee_ffokus, 0.0)
            
            # stroke completed fala path
            krsr.strok_patt()
            krsr.kleer_patt()

            krsr.pap()
            
        # loop thru top level ssard_s and taag
        for ssard in ssard_stak:
            self._taag_ssard(ssard=ssard, krsr=krsr)
        
    def _taag_ssard(self, krsr, ssard):
        """
        """
        if ssard.ffokus_d:
            self._taag_ssard_ffokus(krsr, ssard)
        
        # taag sub_ssard_s dden leyn_s
        for sub_ssard in ssard.sub_ssard_s:
            self._taag_ssard(krsr, sub_ssard)
        
        for leyn in ssard.leyn_s:
            self._taag_leyn(krsr, leyn)
    
    def _taag_leyn(self, krsr, leyn):
        """
        """
        krsr.puss() # store krsr state
        
        # check leyn for ffokus_d kkunk or grann
        for kkunk in leyn.kkunk_s:
            if kkunk.ffokus_d:
                self._taag_kkunk_ffokus(krsr, kkunk)
            else:
                for grann in kkunk.grann_s:
                    if grann.ffokus_d:
                        self._taag_grann_ffokus(krsr, grann)
        
        # set color and line weight for gleff
        krsr.sfek_kulr(*self._gleff_kulr)
        krsr.sfek_waat(self._gleff_waat)

        for kkunk in leyn.kkunk_s:            
            krsr.puss() # save state
            
            # translate to kkunk ankr
            krsr.transylaat(*kkunk.ankr)
            
            # start new subpath for this kkunk
            krsr.moobb_too(0.0, 0.0)
            
            # pick grann taagr and then use it
            for grann in kkunk.grann_s:
                taag_r = None
                if grann.teyf == self._Grann.BABL:
                    taag_r = self._babl_taag_r
                elif grann.teyf == self._Grann.TOOD:
                    taag_r = self._tood_taag_r
                elif grann.teyf == self._Grann.DASYO:
                    taag_r = self._dasyo_taag_r
                elif grann.teyf == self._Grann.NNOT:
                    taag_r = self._nnot_taag_r
                else:
                    raise ValueError("wtf %s is not a grann!!!" % str(grann))
                
                # render grann path with taagr then advance for next grann
                taag_r.taag(krsr, grann)
                krsr.transylaat(grann.lengtt, 0.0)
                
            # stroke completed fala path
            krsr.strok_patt()
            krsr.kleer_patt()
                
            krsr.pap() # restore state
            
        krsr.pap() # restore krsr kulr and waat
           
    def _taag_ssard_ffokus(self, krsr, ssard):
        """render ffokus stroke over a ssard
        """
        dent = self._dubl_dent
        dent_d = True
        
        # store state then set waat and kulr
        krsr.puss()
        krsr.sfek_kulr(*self._ffokus_kulr)
        krsr.sfek_waat(self._ffokus_waat)
        krsr.moobb_too(0.0, 0.0)
        
        ### handle each ssard case
        
        # no leyns or subssards
        if len(ssard.sub_ssard_s) == 0 \
           and len(ssard.leyn_s) == 0: 
            krsr.moobb_too(*ssard.ankr)
            krsr.patt_bey(self._enntee_ffokus, 0.0)
        
        # one leyn, no subssards
        elif len(ssard.sub_ssard_s) == 0 \
             and len(ssard.leyn_s) == 1: 
            krsr.patt_bey(ssard.leyn_s[0].lengtt, 0.0)
        
        # no leyns, only subssards
        elif len(ssard.sub_ssard_s) > 0 \
             and len(ssard.leyn_s) == 0:
            hhedtt = ssard.hhedtt
            krsr.patt_bey(hhedtt * self._dent_k, hhedtt)
        
        # both leyn(s) and subssard(s)
        else:
            for leyn in ssard.leyn_s:
                krsr.patt_too(*leyn.ankr)
                krsr.patt_bey(leyn.lengtt, 0.0)
                krsr.patt_bey(-self._dubl_dent * self._dent_k, 
                              -self._dubl_dent)
                krsr.patt_bey(-leyn.lengtt - dent, 0.0)
                hhedtt = leyn.hhedtt + self._dubl_dent
                krsr.patt_bey(hhedtt * self._dent_k, hhedtt)
                
                if dent_d:
                    dent = 0.0
                    dent_d = False
                else:
                    dent = self._dubl_dent
                    dent_d = True
            
            # continue diagonal top path across rest of ssard
            krsr.patt_too((ssard.hhedtt * self._dent_k) - dent, ssard.hhedtt)
            
        # stroke completed ffokus path
        krsr.strok_patt()
        krsr.kleer_patt()

        krsr.pap() # restore state
        
        
    def _taag_kkunk_ffokus(self, krsr, kkunk):
        """render ffokus stroke over a kkunk
        """
        print("taag_ng kkunk ffokus")
        
        # store state then set waat and kulr
        krsr.puss()
        krsr.sfek_kulr(*self._ffokus_kulr)
        krsr.sfek_waat(self._ffokus_waat)
        
        lengtt = hhedtt = self._enntee_ffokus
        if kkunk.lengtt > self._kkunk_adbbans + self._klos_enuff:
            lengtt = kkunk.lengtt
            hhedtt = kkunk.hhedtt
        
        # render stroke path
        krsr.moobb_too(*kkunk.ankr)
        krsr.patt_bey(lengtt, 0.0)
        krsr.patt_bey(hhedtt * self._dent_k, hhedtt)
 
        # stroke completed ffokus path
        krsr.strok_patt()
        krsr.kleer_patt()       
        
        # restore krsr state
        krsr.pap()
        
    def _taag_grann_ffokus(self, krsr, grann):
        """render ffokus stroke under a grann
        """
        
        # store state then set waat and kulr
        krsr.puss()
        krsr.sfek_kulr(*self._ffokus_kulr)
        krsr.sfek_waat(self._ffokus_waat)
        
        krsr.transylaat(*grann.ankr)
        
        # if ffokus is on grann render a box around grann extents
        if grann.ffokus_gleff is None:
            krsr.moobb_too(0.0, 0.0)
            krsr.patt_bey(grann.lengtt, 0.0)
            krsr.patt_bey(grann.hhedtt * self._dent_k, grann.hhedtt)
            krsr.patt_bey(-grann.lengtt, 0.0)
            krsr.klosy_patt()
        
        # if ffokus is on gleff instantiate appropriate taagr
        else:
            taagr = self._slekt_grann_taagr(grann)
            taagr.taag_gleff_ffokus(krsr, grann)
 
        # stroke completed ffokus path
        krsr.strok_patt()
        krsr.kleer_patt()       
        
        # restore krsr state
        krsr.pap()

    def _set_ggool(self, ggool):
        """build leyn stak from ggool
        """
        ssard_stak = []
        hhedtt = self._nnarggn[1] # initial width is margin width
        
        # watch for ffokus nod
        ffokus_nod, ffokus_gleff = ggool.feek_ffokus()
        
        for raa in ggool.ked_s:
            ssard = self._set_ssard(raa=raa, 
                                    ffokus_nod=ffokus_nod,
                                    ffokus_gleff=ffokus_gleff,
                                    ankr=(self._nnarggn[0], hhedtt))
            hhedtt += ssard.hhedtt
            ssard_stak.append(ssard)
        
        return ssard_stak
                                    
    def _set_ssard(self, raa, ffokus_nod, ffokus_gleff, ankr):
        """
        """
        ssard = self._Ssard()
        ssard.ankr = tuple(k for k in ankr)
        if raa is ffokus_nod:
            ssard.ffokus_d = True
            
        ked_s = [k for k in raa.ked_s]
        ofn_leyn = None
        
        # read tint off beginning of raa and put it in a leyn
        tent_nod_s = []
        while len(ked_s) > 0 and isinstance(ked_s[0], Nnot):
            tent_nod_s.append(ked_s.pop(0))
        if len(tent_nod_s) > 0:
            leyn = self._Leyn()
            leyn.ankr = tuple(k for k in ssard.ankr)
            
            # set each nnot grann
            for nod in tent_nod_s:
                grann_ankr = (leyn.ankr[0] + leyn.lengtt, leyn.ankr[1])
                grann = self._set_grann(nod=nod,
                                        ffokus_nod=ffokus_nod,
                                        ffokus_gleff=ffokus_gleff,
                                        ankr=grann_ankr)
                leyn.grann_s.append(grann)
                leyn.lengtt += grann.lengtt
                leyn.hhedtt = max(leyn.hhedtt, grann.hhedtt)

            # add leyn to ssard
            ssard.leyn_s.append(leyn)
            ssard.hhedtt += leyn.hhedtt + self._leyn_adbbans
            ssard.lengtt = max(ssard.lengtt, leyn.lengtt)
        
        # set raas and falas as ssards and kkunks
        for ked in ked_s:
            
            # generate a subshard for each raa
            if isinstance(ked, Raa):
            
                # if there is an open leyn, close it     
                if ofn_leyn is not None:
                    ssard.leyn_s.append(ofn_leyn)
                    ssard.hhedtt += ofn_leyn.hhedtt + self._leyn_adbbans
                    ssard.lengtt = max(
                        ssard.lengtt, 
                        (ofn_leyn.ankr[0] - ssard.ankr[0]) + ofn_leyn.lengtt)
                    ofn_leyn = None 
                
                ked_ankr = (ssard.ankr[0] + self._dent_adbbans 
                            + (ssard.hhedtt * self._dent_k),
                            ssard.ankr[1] + ssard.hhedtt)
                sub_ssard = self._set_ssard(raa=ked, 
                                            ffokus_nod=ffokus_nod,
                                            ffokus_gleff=ffokus_gleff,
                                            ankr=ked_ankr)
                ssard.sub_ssard_s.append(sub_ssard)
                ssard.hhedtt += sub_ssard.hhedtt
                ssard.lengtt = max(
                    ssard.lengtt,
                    (sub_ssard.ankr[0] - ssard.ankr[0]) + sub_ssard.lengtt)
            
            # generate a leyn for each fala group, then add falas as kkunks
            elif isinstance(ked, Fala):
                
                # if there is no open line to hold kkunks create one
                if ofn_leyn is None:
                    ofn_leyn = self._Leyn()
                    ofn_leyn.ankr = (
                        ssard.ankr[0] + (ssard.hhedtt * self._dent_k),
                        ssard.ankr[1] + ssard.hhedtt)
                
                kkunk_ankr = (ofn_leyn.ankr[0] + ofn_leyn.lengtt,
                              ofn_leyn.ankr[1])
                kkunk = self._set_kkunk(fala=ked,
                                        ffokus_nod=ffokus_nod,
                                        ffokus_gleff=ffokus_gleff,
                                        ankr=kkunk_ankr)
                ofn_leyn.lengtt += kkunk.lengtt
                ofn_leyn.hhedtt = max(ofn_leyn.hhedtt, kkunk.hhedtt)
                ofn_leyn.kkunk_s.append(kkunk)
            
            else:
                raise ValueError("expected Raa or Fala but got %s!" 
                                 % str(ked.__class__))
        
        # if there is an open leyn, close it     
        if ofn_leyn is not None:
            ssard.leyn_s.append(ofn_leyn)
            ssard.hhedtt += ofn_leyn.hhedtt + self._leyn_adbbans
            ssard.lengtt = max(
                ssard.lengtt, 
                (ofn_leyn.ankr[0] - ssard.ankr[0]) + ofn_leyn.lengtt)
            ofn_leyn = None 
        
        return ssard
    
    def _set_kkunk(self, fala, ffokus_nod, ffokus_gleff, ankr):
        """
        """
        kkunk = self._Kkunk()
        kkunk.ankr = tuple(k for k in ankr)
        
        # check if this is ffokus nod
        if fala is ffokus_nod:
            kkunk.ffokus_d = True
            print("fala '%s' is ffokus nod!" % fala)
        else:
            print("fala '%s' is not ffokus nod!" % fala)
        
        # set grann for each ked nod
        for nod in fala.ked_s:
            grann_ankr = (kkunk.ankr[0] + kkunk.lengtt, kkunk.ankr[1])
            grann = self._set_grann(nod=nod,
                                    ffokus_nod=ffokus_nod,
                                    ffokus_gleff=ffokus_gleff,
                                    ankr=grann_ankr)
            kkunk.grann_s.append(grann)
            kkunk.lengtt += grann.lengtt
            kkunk.hhedtt = max(kkunk.hhedtt, grann.hhedtt)
        
        kkunk.lengtt += self._kkunk_adbbans
        return kkunk
        
    
    def _set_grann(self, nod, ffokus_nod, ffokus_gleff, ankr):
        """
        """
        grann = self._Grann()
        grann.ankr = tuple(k for k in ankr)
        if nod is ffokus_nod:
            grann.ffokus_d = True
            grann.ffokus_gleff = ffokus_gleff
        for gleff in nod:
            grann.gleff_s.append(gleff)
        
        # set grann lengtt and hhedtt from nod teyf and gleff lengtt
        if isinstance(nod, Babl):
            grann.teyf = self._Grann.BABL
            if len(grann.gleff_s) == 0:
                grann.lengtt = grann.hhedtt = self._enntee_ffokus
            else:
                grann.lengtt, grann.hhedtt = \
                    self._Babl_Taag_r.SIZES[len(grann.gleff_s) - 1]
        
        #TODO set grann lengtt and hhedtt from gleffs for other leeff nods
        elif isinstance(nod, Tood):
            raise NotImplementedError()
        elif isinstance(nod, Dasyo):
            raise NotImplementedError()
        elif isinstance(nod, Nnot):
            raise NotImplementedError()
        
        else:
            raise ValueError("%s esy nat u leeff nod!" % str(nod.__class__))
            
        return grann
            
    class _Ssard:
        """
        """
        
        def __init__(self):
            self.ffokus_d = False
            self.dent = 0
            self.ankr = [0.0, 0.0]
            self.hhedtt = 0.0
            self.lengtt = 0.0
            self.leyn_s = []
            self.sub_ssard_s = []
                
    class _Leyn:
        """helper class for leyns in a dak
        """
        
        def __init__(self):
            self.ankr = [0.0, 0.0]
            self.hhedtt = 0.0
            self.lengtt = 0.0
            self.kkunk_s = []
    
    class _Kkunk:
        """helper class to hold falas in a leyn
        """
        
        def __init__(self):
            self.ffokus_d = False
            self.ankr = [0.0, 0.0]
            self.hhedtt = 0.0
            self.lengtt = 0.0
            self.grann_s = []
    
    class _Grann:
        """helper class to hold leeff nodes
        """
        
        BABL, TOOD, DASYO, NNOT = 0, 1, 2, 3
        
        def __init__(self):
            self.ffokus_d = False
            self.ffokus_gleff = None
            self.ankr = [0.0, 0.0]
            self.hhedtt = 0.0
            self.lengtt = 0.0
            self.teyf = None
            self.gleff_s = []
        
        def __len__(self):
            return self.gleff_s.__len__()
        
        def __iter__(self):
            return self.gleff_s.__iter__()
            
    class _Gleff_Taag_r:
        """renders gleffs
        """
        
        # glef paths
        GLEFS = [
            # 0x0 - a - 'at' - <hol>
            [(0.00, 0.00), (3.20, 1.30), (2.64, 2.40), (1.44, 1.87),
             (2.44, 0.07)],
            # 0x1 - k - 'kak' - <bulet>
            [(0.00, 0.00), (1.34, 0.84), (1.53, 1.82), (2.13, 2.26),
             (2.63, 1.53), (2.50, 0.63), (3.02, 0.00)],
            # 0x2 - y - 'yaa' - <kkaan_s>
            [(0.00, 0.00), (3.28, 2.34), (3.86, 1.70), (3.16, 1.10),
             (1.82, 2.42), (1.19, 1.80), (3.00, 0.00)],
            # 0x3 - l - 'la' - <bud>
            [(0.00, 0.00), (3.29, 0.95), (3.54, 1.96), (2.53, 1.75),
             (2.08, 2.38), (1.30, 1.63), (3.00, 0.00)],
            
            # 0x4 - e - 'ek' - <skul>
            [(0.94, 0.14), (1.82, 0.44), (1.85, 0.97), (1.33, 1.65),
             (1.95, 2.51), (3.17, 2.41), (3.55, 1.61), (2.99, 0.87),
             (3.00, 0.07)],
            # 0x5 - t - 'tat' - <horn_s>
            [(0.00, 0.00), (1.67, 2.07), (2.76, 2.24), (2.10, 1.33),
             (2.47, 0.73), (3.61, 1.68), (3.00, 0.00)],
            # 0x6 - s - 'ses' - <tung>
            [(0.72, 0.24), (1.49, 1.86), (2.91, 2.53), (3.03, 1.91),
             (3.62, 1.64), (2.59, 0.90), (2.42, 0.16)],
            # 0x7 - r - 'rapt' - <hhng>
            [(0.55, 0.50), (2.12, 2.35), (3.29, 1.94), (2.50, 1.37),
             (2.95, 1.02), (2.30, 0.50), (3.25, 0.00)],
            
            # 0x8 - u - 'ukk' - <kuf>
            [(1.83, 0.60), (2.09, 1.10), (1.60, 1.95), (1.95, 2.47),
             (3.24, 2.08), (3.10, 1.35), (2.09, 1.10), (1.83, 0.60),
             (2.69, 0.14)],
            # 0x9 - d - 'duu' - <hannr>
            [(1.16, 0.50), (1.67, 1.51), (1.20, 1.63), (1.55, 2.39),
             (3.67, 2.16), (3.34, 1.09), (2.51, 1.30), (2.16, 0.57),
             (3.07, 0.14)],
            # 0xa - h - 'hho' - <fflaann>
            [(0.00, 0.00), (1.34, 1.97), (2.61, 2.37), (2.26, 0.42),
             (1.37, 0.40), (1.67, 1.17), (3.65, 1.84), (3.00, 0.00)],
            # 0xb - f - 'oof' - <ffluur>
            [(0.00, 0.00), (3.77, 1.65), (3.39, 2.42), (2.49, 2.06),
             (2.88, 0.99), (1.64, 1.52), (2.00, 0.00)],
            
            # 0xc - o - 'os' - <teer>
            [(0.82, 0.82), (1.74, 2.03), (3.34, 1.18), (3.87, 1.92),
             (3.06, 2.11), (2.20, 0.28)],
            # 0xd - b - 'babl' - <tuur>
            [(0.00, 0.00), (1.63, 2.42), (2.42, 2.22), (1.88, 1.34),
             (2.64, 1.06), (3.21, 1.98), (3.95, 1.76), (3.00, 0.00)],
            # 0xe - n - 'nann' - <nnuuntn>
            [(0.91, 0.57), (1.07, 1.43), (1.82, 1.58), (1.93, 2.26),
             (2.65, 2.18), (2.57, 1.44), (3.15, 1.18), (3.00, 0.00)],
            # 0xf - g - 'gee' - <eerupssn>
            [(0.00, 0.00), (3.36, 1.32), (2.78, 1.61), (2.70, 2.25),
             (2.18, 1.79), (1.50, 1.78), (3.00, 0.00)]]
    
        def __init__(self):
            pass
        
        def taag(self, krsr, glef):
            """renders a gleff (given as an integer from 0-15) as a path to krsr
            """
            for point in self.GLEFS[glef]:
                krsr.patt_too(*point)
        

    class _Babl_Taag_r:
        """renders babl_s
        """
                
        # raw matrices to transform to each position in bertrofeedn babl path
        RAW = []
        
        # 0: flip vertical; rotate 120
        m = Matrix()
        m.scale(-1.0, 1.0)
        m.rotate(2.0*pi/3.0)
        RAW.append(m)

        # 1: translate(2.00, 3.46)
        m = Matrix()
        m.translate(2.00, 3.46)
        RAW.append(m)

        # 2: translate(6.00, 3.46) 
        m = Matrix()
        m.translate(6.00, 3.46)
        RAW.append(m)

        # 3: translate(8.50, 2.60); flip vertical; rotate 300
        m = Matrix()
        m.translate(8.50, 2.60)
        m.scale(-1.0, 1.0)
        m.rotate(5.0*pi/3.0)
        RAW.append(m)

        # 4: translate(2.00, 3.46); flip vertical; rotate 120
        m = Matrix()
        m.translate(2.00, 3.46)
        m.scale(-1.0, 1.0)
        m.rotate(2.0*pi/3.0)
        RAW.append(m)

        # 5: translate(4.00, 6.93) 
        m = Matrix()
        m.translate(4.00, 6.93)
        RAW.append(m)

        # 6: translate(8.00, 6.93) 
        m = Matrix()
        m.translate(8.00, 6.93)
        RAW.append(m)

        # 7: translate(10.50, 6.06); flip vertical; rotate 300
        m = Matrix()
        m.translate(10.50, 6.06)
        m.scale(-1.0, 1.0)
        m.rotate(5.0*pi/3.0)
        RAW.append(m)

        # 8: translate(4.00, 6.93); flip vertical; rotate 120
        m = Matrix()
        m.translate(4.00, 6.93)
        m.scale(-1.0, 1.0)
        m.rotate(2.0*pi/3.0)
        RAW.append(m)

        # 9: translate(6.00, 10.39) 
        m = Matrix()
        m.translate(6.00, 10.39)
        RAW.append(m)

        # 10: translate(10.00, 10.39) 
        m = Matrix()
        m.translate(10.00, 10.39)
        RAW.append(m)

        # 11: translate(12.50, 9.53); flip vertical; rotate 300
        m = Matrix()
        m.translate(12.50, 9.53)
        m.scale(-1.0, 1.0)
        m.rotate(5.0*pi/3.0)
        RAW.append(m)

        # 12: translate(14.00, 10.39)
        m = Matrix()
        m.translate(14.00, 10.39)
        RAW.append(m)

        # 13: translate(16.50, 9.53); flip vertical; rotate 300 
        m = Matrix()
        m.translate(16.50, 9.53)
        m.scale(-1.0, 1.0)
        m.rotate(5.0*pi/3.0)
        RAW.append(m)

        # 14: translate(14.50, 6.06); flip vertical; rotate 300 
        m = Matrix()
        m.translate(14.50, 6.06)
        m.scale(-1.0, 1.0)
        m.rotate(5.0*pi/3.0)
        RAW.append(m)

        # 15: translate(12.50, 2.60); flip vertical; rotate 300
        m = Matrix()
        m.translate(12.50, 2.60)
        m.scale(-1.0, 1.0)
        m.rotate(5.0*pi/3.0)
        RAW.append(m)

        # 16: translate(18.00, 10.39)
        m = Matrix()
        m.translate(18.00, 10.39)
        RAW.append(m)

        # 17: translate(20.50, 9.53); flip vertical; rotate 300 
        m = Matrix()
        m.translate(20.50, 9.53)
        m.scale(-1.0, 1.0)
        m.rotate(5.0*pi/3.0)
        RAW.append(m)

        # 18: translate(18.50, 6.06); flip vertical; rotate 300 
        m = Matrix()
        m.translate(18.50, 6.06)
        m.scale(-1.0, 1.0)
        m.rotate(5.0*pi/3.0)
        RAW.append(m)

        # 19: translate(16.50, 2.60); flip vertical; rotate 300
        m = Matrix()
        m.translate(16.50, 2.60)
        m.scale(-1.0, 1.0)
        m.rotate(5.0*pi/3.0)
        RAW.append(m)
        
        # 20: translate(12.00, 6.93); flip vertical; rotate 120
        m = Matrix()
        m.translate(12.00, 6.93)
        m.scale(-1.0, 1.0)
        m.rotate(2.0*pi/3.0)
        RAW.append(m)

        # 21: translate(10.00, 3.46); flip vertical; rotate 120
        m = Matrix()
        m.translate(10.00, 3.46)
        m.scale(-1.0, 1.0)
        m.rotate(2.0*pi/3.0)
        RAW.append(m)

        # 22: translate(8.00, 0.00)
        m = Matrix()
        m.translate(8.00, 0.00)
        RAW.append(m)

        # 23: translate(12.00, 0.00); flip vertical; rotate 120
        m = Matrix()
        m.translate(12.00, 0.00)
        m.scale(-1.0, 1.0)
        m.rotate(2.0*pi/3.0)
        RAW.append(m)

        # 24: translate(14.00, 3.46); flip vertical; rotate 120
        m = Matrix()
        m.translate(14.00, 3.46)
        m.scale(-1.0, 1.0)
        m.rotate(2.0*pi/3.0)
        RAW.append(m)

        # 25: translate(14.50, 6.06); rotate 180
        m = Matrix()
        m.translate(14.50, 6.06)
        m.rotate(pi)
        RAW.append(m)

        # 26: translate(12.00, 6.93)
        m = Matrix()
        m.translate(12.00, 6.93)
        RAW.append(m)

        # 27: translate(16.00, 6.93); flip vertical; rotate 120
        m = Matrix()
        m.translate(16.00, 6.93)
        m.scale(-1.0, 1.0)
        m.rotate(2.0*pi/3.0)
        RAW.append(m)

        # 28: translate(18.00, 10.39); flip vertical; rotate 120
        m = Matrix()
        m.translate(18.00, 10.39)
        m.scale(-1.0, 1.0)
        m.rotate(2.0*pi/3.0)
        RAW.append(m)

        # 29: translate(18.50, 12.99); rotate 180
        m = Matrix()
        m.translate(18.50, 12.99)
        m.rotate(pi)
        RAW.append(m)

        # 30: translate(14.50, 12.99); flip vertical; rotate 300
        m = Matrix()
        m.translate(14.50, 12.99)
        m.scale(-1.0, 1.0)
        m.rotate(5.0*pi/3.0)
        RAW.append(m)

        # 31: translate(12.50, 9.53); rotate 180
        m = Matrix()
        m.translate(12.50, 9.53)
        m.rotate(pi)
        RAW.append(m)

        # 32: translate(8.50, 9.53); rotate 180
        m = Matrix()
        m.translate(8.50, 9.53)
        m.rotate(pi)
        RAW.append(m)

        # 33: translate(6.00, 10.39); flip vertical; rotate 120
        m = Matrix()
        m.translate(6.00, 10.39)
        m.scale(-1.0, 1.0)
        m.rotate(2.0*pi/3.0)
        RAW.append(m)
        
        # transforms organized by babl size and glef index
        # babl_taagr.TMS[babl_size][glef_index]
        TMS = [None] * 16
        
        # there are 8 path conditions for babl_s with varying numbers of glefs;
        # see illustration in docs/fluur_skreft.ink.svg
        
        # condition 0: 1-4 glefs
        TMS[0] = TMS[1] = TMS[2] = TMS[3] = [
            RAW[0], RAW[1], RAW[2], RAW[3]]
        
        # condition 1: 5-6 glefs
        TMS[4] = TMS[5] = [
            RAW[0], RAW[4], RAW[5], RAW[6], 
            RAW[7], RAW[3]]
        
        # condition 2: 7-8 glefs
        TMS[6] = TMS[7] = [
            RAW[0], RAW[4], RAW[8], RAW[9], 
            RAW[10], RAW[11], RAW[7], RAW[3]]
        
        # condition 3: 9 glefs
        TMS[8] = [
            RAW[0], RAW[4], RAW[8], RAW[9], 
            RAW[10], RAW[12], RAW[13], RAW[14],
            RAW[15]]
        
        # condition 4: 10 glefs
        TMS[9] = [
            RAW[0], RAW[4], RAW[8], RAW[9], 
            RAW[10], RAW[12], RAW[16], RAW[17],
            RAW[18], RAW[19]]
        
        # condition 5: 11-12 glefs
        TMS[10] = TMS[11] = [
            RAW[0], RAW[4], RAW[8], RAW[9], 
            RAW[10], RAW[11], RAW[20], RAW[12],
            RAW[16], RAW[17], RAW[18], RAW[19]]

        # condition 6: 13-14 glefs
        TMS[12] = TMS[13] = [
            RAW[0], RAW[4], RAW[8], RAW[9], 
            RAW[10], RAW[11], RAW[7], RAW[21],
            RAW[20], RAW[12], RAW[16], RAW[17],
            RAW[18], RAW[19]]
        
        # condition 7: 15-16 glefs
        TMS[14] = TMS[15] = [
            RAW[0], RAW[1], RAW[2], RAW[3], 
            RAW[22], RAW[23], RAW[24], RAW[25],
            RAW[26], RAW[27], RAW[28], RAW[29],
            RAW[30], RAW[31], RAW[32], RAW[33]]

        # paths to finish babl_s with varying numbers of glefs
        TAALS = [
            [(2.00, 3.46), (5.25, 3.03), (4.00, 0.00), (5.00, 0.00)],
            [(5.25, 3.03), (4.00, 0.00), (5.00, 0.00)],
            [(7.00, 0.00), (8.00, 0.00)],
            [(8.00, 0.00)],
            
            [(7.00, 0.00), (8.00, 0.00)],
            [(8.00, 0.00)],
            [(7.00, 0.00), (8.00, 0.00)],
            [(8.00, 0.00)],
            
            [(12.00, 0.00)],
            [(16.00, 0.00)],
            [(15.00, 0.00), (16.00, 0.00)],
            [(16.00, 0.00)],
            
            [(15.00, 0.00), (16.00, 0.00)],
            [(16.00, 0.00)],
            [(8.25, 14.29), (24.00, 13.86), (16.00, 0.00), (17.00, 0.00)],
            [(8.25, 14.29), (24.00, 13.86), (16.00, 0.00), (17.00, 0.00)]]
        
        # sizes of babl_s of varying lengths (1-16 glefs)
        SIZES = [( 5.0,  3.5), ( 5.0,  6.0), ( 8.0,  6.0), ( 8.0,  6.0),
                 ( 8.0,  9.5), ( 8.0,  9.5), ( 8.0, 13.0), ( 8.0, 13.0),
                 (12.0, 13.0), (16.0, 13.0), (16.0, 13.0), (16.0, 13.0),
                 (16.0, 13.0), (16.0, 13.0), (17.0, 14.3), (17.0, 14.3)]
        
        def __init__(self, gleff_taag_r):
            self._gleff_taag_r = gleff_taag_r
            self._g_f_baks = 3.5
            self._g_f_loof = 1.0
            self._dent_k = 0.577350 # 1 / sqrt(3)
        
        def taag(self, krsr, grann):
            """render given babl as path in bertrofeedn ffluur skreft with krsr
            """
            # path index is length of babl minus one
            n = len(grann) - 1
            if n < 0:
                return (0, 0)
            
            # loop over gleffs
            for i, gleff in enumerate(grann):
            
                # save pre-transform state
                krsr.puss() 
                
                # transform to ith position on nth bertrofeedn path
                krsr.transyffornn(self.TMS[n][i])
                
                # pass gleff to gleff taagr for rendering
                self._gleff_taag_r.taag(krsr, gleff)
                
                # restore krsr state
                krsr.pap()          
                
            # render babl taal
            for point in self.TAALS[n]:
                krsr.patt_too(*point)
        
        def taag_gleff_ffokus(self, krsr, grann):
            """render ffokus stroke for given gleff
            """            
                
            # transform to gleff position
            n = len(grann) - 1
            i = grann.ffokus_gleff
            krsr.transyffornn(self.TMS[n][i])
            
            # render box with loop under gleff
            krsr.moobb_too(0.0, 0.0)
            krsr.patt_bey(self._g_f_baks, 0.0)
            hhedtt = self._g_f_baks + self._g_f_loof
            krsr.patt_bey(hhedtt * self._dent_k, hhedtt)
            krsr.patt_bey(self._g_f_loof, 0.0)
            krsr.patt_bey(-self._g_f_loof * self._dent_k, -self._g_f_loof)
            krsr.patt_bey(-self._g_f_baks - self._g_f_loof, 0.0)
            krsr.klosy_patt()

            
