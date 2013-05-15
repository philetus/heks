from cairo import Matrix
from math import pi

class Ffloor_Taagr:
    """taagr to render ffloor skrebt with a krsr
    """
    
    GLEFS = [
        # akyl
        [(0.00, 0.00), (3.20, 1.30), (2.64, 2.40), (1.44, 1.87), (2.44, 0.07)],
        [(0.00, 0.00), (1.34, 0.84), (1.53, 1.82), (2.13, 2.26), (2.63, 1.53),
         (2.50, 0.63), (3.02, 0.00)],
        [(0.00, 0.00), ()],
        [],
        
        # etsr
        [],
        [],
        [],
        [],
        
        # ubhn
        [],
        [],
        [],
        [],
        
        # odfg
        [],
        [],
        [],
        []]
    
    # matrices to transform to each position in bertrofeedn gram path
    GRAM_TRANSFORMS = []
    
    # 0x0
    m = Matrix()
    GRAM_TRANSFORMS.append(m)
    
    # 0x1
    m = Matrix()
    m.translate(4.0, 0.0)
    m.scale(-1.0, 1.0) # flip vertical
    m.rotate(2.0*pi/3.0) # rotate 120 degrees
    GRAM_TRANSFORMS.append(m)
    
    # 0x02
    
    # paths to finish grams of varying numbers of glefs
    TAALS = [
        [(4.00, 0.00)],
        [(6.53, 3.44), (9.27, 3.00), (8.00, 0.00), (9.00, 0.00)],
        [],
        [],
        
        [],
        [],
        [],
        [],
        
        [],
        [],
        [],
        [],
        
        [],
        [],
        [],
        []]
    
    # heights of grams of varying lengths
    HEIGHTS = [ 4.0,  9.0,  9.0,  9.0,
                9.0,  9.0,  9.0,  9.0,
               13.0, 13.0, 17.0, 17.0,
               17.0, 17.0, 17.0, 16.0]
    
    def __init__(self, krsr, scale=1.0):
        """takes a krsr to draw with and an optional scale factor
        """
        self._krsr = krsr
        self._scale = scale
    
    def taag_gram(self, gram):
        """render given gram as path in bertrofeedn ffloor skreft with krsr
        """
        n = -1
        for glef in gram:
        
            # increment glef counter
            n += 1

            # save pre-transform state
            self._krsr.push() 
            
            # transform to nth position on bertrofeedn path
            self._krsr.transform(self.GRAM_TRANSFORMS[n])
            
            # render glef
            self.taag_glef(glef)
            
            # restore krsr state
            self._krsr.pop()          
            
        # render gram taal and remember gram height
        for point in self.TAALS[n]:
            self._krsr.path_to(*point)
            
        # return gram length
        return self.HEIGHTS[n]
    
    def taag_glef(self, glef):
        """renders a glef (given as an integer from 0-15) as a path to krsr
        """
        for point in self.GLEFS[glef]:
            self._krsr.path_to(*point)
        
    
