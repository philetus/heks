from Eesyl import Eesyl
from Ffluur_Taagr import Ffluur_Taagr

from heks.sess.Ggool import Ggool
#from heks.ggool.Nneta_deks import Nneta_deks

class Slaat(Eesyl):
    """rendr_s u sess en ffluur skreft
    """

    def __init__(self, sess, hhedtt=256, heyt=512, skaal=1.0, teytl='slaat'):
        Eesyl.__init__(self, hhedtt=hhedtt, heyt=heyt, teytl=teytl)
        
        self._sess = sess # sess to render
        
        self._skaal = skaal # glyph scale        
        
        # create ffluur taagr
        self._taagr = Ffluur_Taagr(skaal=skaal)

        
    def handl_dra(self, krsr):
        """render dak on top of stak with ffluur taagr
        """
        # get dak to render off top of sess dak stak
        dak = self._sess.feek_stak()
        
        # if dak is ggool taag ggool
        if isinstance(dak, Ggool):
            self._taagr.taag_ggool(krsr, dak)
        
        else:
            raise NotImplementedError("kant render deks yet!")
            

    def handl_kee(self, kee):
        """do something when key is released
        """
        self._sess.doo(kee)        
        
        # trigger redraw after keystroke
        self.redraw()
        
