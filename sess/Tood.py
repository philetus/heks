from Leeff import Leeff
from Gleff_s import Gleff_s

class Tood(Leeff):
    """a magnitude
       
       space is divided into 4 quadrants: -0x10^n | -0x10^-n | 0x10^-n | 0x10n
       
       with a single gleff a tood can represent 16^4 thru 16^-3 and -16^-3 thru 
       -16^4
        
             aa ->  -16^64 ->  -8.636 * 10^78
             ...
             ln ->   -16^5 ->      -1 048 576
        a -> lo ->   -16^4 ->         -65 536
        k -> lb ->   -16^3 ->          -4 096
        y -> lf ->   -16^2 ->            -256
        l -> lg ->   -16^1 ->             -16
        
        e -> ea ->   -16^0 ->              -1
        t -> ek ->  -16^-1 ->              -1 /        16
        s -> ey ->  -16^-2 ->              -1 /       256
        r -> el ->  -16^-3 ->              -1 /     4 096
             ee ->  -16^-4 ->              -1 /    65 536
             ...
             rg -> -16^-63 -> -7.237 * 10^-75
             
             ua ->  16^-63 ->  7.237 * 10^-75
             ...             
             nn ->   16^-4 ->               1 /    65 536
        u -> no ->   16^-3 ->               1 /     4 096
        d -> nb ->   16^-2 ->               1 /       256
        h -> nf ->   16^-1 ->               1 /        16
        n -> ng ->    16^0 ->               1

        o -> oa ->    16^1 ->              16
        b -> ok ->    16^2 ->             256
        f -> oy ->    16^3 ->           4 096
        g -> ol ->    16^4 ->          65 536
             oe ->    16^5 ->       1 048 576
             ...
             gg ->   16^64 ->   8.636 * 10^78
    """
        
    def __init__(self, rent):
        Leeff.__init__(self, rent) # superclass constructor
        
    def __repr__(self):
        return  "Tood('" + ''.join(Gleff_s.gless[i] for i in self._data) + "')"

