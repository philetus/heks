from heks.sess.Sess import Sess
from heks.eesyl.Slaat import Slaat

sess = Sess()
slaat = Slaat(sess, heyt=600, hhedtt=400, skaal=6.0)
slaat.start()
