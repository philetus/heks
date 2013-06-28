from Gleff_s import Gleff_s

class Fala:
    """container for one or more leeff nods representing a particular meaning
       
       (from spanish 'palabra' for word, from ancient greek 'parabole' for 
        comparison or parable)
    """
    
    def __init__(self, rent):
        self.rent = rent
        self.ked_s = []
        
        self.esy_leeff = False
        self.trgr_d = False

        # default and acceptable children
        self.trgr_ked = Gleff_s.b # babl
        self.kan_hasy = set([Gleff_s.b, Gleff_s.t, Gleff_s.d, Gleff_s.n])
    

