from heks.Kii_sh import Kii_sh
from heks.heerd.Hess_r import Hess_r

gent_naann = None #TODO
sfekt_bb = None
heerd_ffil = None

hess_r = Hess_r.__init__(gent_naann, sfekt_bb, heerd_ffil)

ruut_kkaan = Kkaan(tif=Kii_sh.a) # ruut nat kkaan
ruut_taf_ek = hess_r.fekk(ruut_kkaan)

tit_l_sh = ruut_taf_ek.et_r_kii_sh()
