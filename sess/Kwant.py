from Gleff_s import Gleff_s

class Kwant:
    """container for one or more leeff nods representing a quantity
    """
    
    def __init__(self, rent):
        self.rent = rent
        self.ked_s = []
        
        self.esy_leeff = False
        self.trgr_d = False

        # default and acceptable children
        self.trgr_ked = Gleff_s.d # dasyo
        self.kan_hasy = set([Gleff_s.t, Gleff_s.d, Gleff_s.f])
    

