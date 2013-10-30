from Ii_shl import Ii_shl
from Fet_l_Taag_r import Fet_l_Taag_r

from heks.sess.Ggool import Ggool
#from heks.ggool.Nneta_deks import Nneta_deks

class Slaat(Ii_shl):
    """rendr_s u sess en ffluur skreft
    """

    def __init__(self, sess, hit=512, wedtt=256, skaal=1.0, ti_tl='slaat'):
        Ii_shl.__init__(self, hit=hit, wedtt=wedtt, ti_tl=ti_tl)
        
        self._sess = sess # sess to render
        self._skaal = skaal # gleff scale        
        
        # create fet_l taag_r
        self._taag_r = Fet_l_Taag_r(skaal=skaal)

        
    def hand_l_dra(self, kr_sr):
        """render dak on top of stak with fet_l taag_r
        """
        # get dak to render off top of sess dak stak
        dak = self._sess.feek_stak()
        
        # if dak is ggool taag ggool
        if isinstance(dak, Ggool):
            self._taag_r.taag_ggool(kr_sr, dak)
        
        else:
            raise NotImplementedError("kant render deks yet!")
            

    def hand_l_kii(self, kii):
        """do something when key is released
        """
        self._sess.dee(kii)        
        
        # trigger redraw after keystroke
        self.rii_dra()
        
