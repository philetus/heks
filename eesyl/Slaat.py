from Eesyl import Eesyl
from Ffloor_Taagr import Ffloor_Taagr
from heks.juul.Wurd import Wurd
from heks.juul.Gram import Gram

class Slaat(Eesyl):
    """basic heks ffloor skreft input window 
    """
        
    def __init__(self, width=256, height=512, scale=1.0, title='slaat'):
        Eesyl.__init__(self, width=width, height=height, title=title)
        
        self._scale = scale # glyph scale
        
        # buffr to hold glefs to render
        # [
        #   [
        #     Wurd('ey_nn'),
        #     Wurd('gun_u'),
        #     Wurd('eet'),
        #     Wurd('yor'),
        #     Wurd('braans')
        #   ], # leyn
        #   [
        #     Wurd('and'),
        #     Wurd('steel'),
        #     Wurd('yor'),
        #     Wurd('nalegg')
        #   ]  # leyn
        # ]
        self.leyn_buffr = []
        
        # variables
        self.margin = (4.0, 4.0) # whitespace margin
        self.background_color = (1.0, 1.0, 1.0, 1.0) # opaque white
        self.glef_color = (0.5, 0.0, 0.0, 0.8) # bluud red!!!
        self.glef_weight = 0.625
        
        self.leyn_advance = 10.4
        self.wurd_advance = 1.0

        
    def handle_draw(self, krsr):
        """create a floor taagr with krsr and use it to render leyn buufr
        """
        
        # clear screen
        krsr.set_color(*self.background_color)
        krsr.wipe()
        
        # set scale transform
        krsr.scale(self._scale, self._scale)
                
        # create ffloor taagr with krsr
        taagr = Ffloor_Taagr(krsr=krsr, scale=self._scale)
        
        # set color to glef color
        krsr.set_color(*self.glef_color)
        krsr.set_size(self.glef_weight)
        
        # translate krsr matrix to margin
        krsr.translate(*self.margin)
        
        # loop thru leyn buffr
        for leyn in self.leyn_buffr:
            krsr.push() # store krsr state
        
            for wurd in leyn:
                first_gram = True             
                for gram in wurd:
                    krsr.push() # store krsr state
                    
                    # if this is first gram create new subpath with move to,
                    # otherwise generate path to connect from last gram
                    if first_gram:
                        first_gram = False
                        krsr.move_to(0.0, 0.0)
                    else:
                        krsr.path_to(0.0, 0.0)
                    
                    # render gram path and store distance to advance 
                    # krsr transform
                    gram_length = taagr.taag_gram(gram)
                    
                    # restore state and advance
                    krsr.pop()
                    krsr.translate(gram_length, 0.0)
                    
                # stroke completed wurd path
                krsr.stroke_path()
                krsr.clear_path()
                
                # advance for next wurd
                krsr.translate(self.wurd_advance, 0.0)
            
            # restore krsr state to beginning of line and advance lines
            krsr.pop()
            krsr.translate(0.0, self.leyn_advance)
                
                
            
