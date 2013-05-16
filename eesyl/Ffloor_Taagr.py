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
        [(0.00, 0.00), (3.28, 2.34), (3.86, 1.70), (3.16, 1.10), (1.82, 2.42),
         (1.19, 1.80), (3.00, 0.00)],
        [(3.29, 0.95), (3.54, 1.96), (2.53, 1.75), (2.08, 2.38), (1.30, 1.63),
         (3.00, 0.00)],
        
        # etsr
        [(1.82, 0.44), (1.85, 0.97), (1.33, 1.65), (1.95, 2.51), (3.17, 2.41),
         (3.55, 1.61), (2.99, 0.87), (3.00, 0.07)],
        [(1.67, 2.07), (2.76, 2.24), (2.10, 1.33), (2.47, 0.73), (3.61, 1.68),
         (3.00, 0.00)],
        [(0.72, 0.24), (1.49, 1.86), (2.91, 2.53), (3.03, 1.91), (3.62, 1.64),
         (2.59, 0.90), (2.42, 0.16)],
        [(2.14, 2.34), (3.86, 2.04), (2.52, 1.37), (3.25, 0.95), (2.04, 0.54),
         (3.42, 0.00)],
        
        # ubhn
        [(1.83, 0.60), (2.09, 1.10), (1.60, 1.95), (1.95, 2.47), (3.24, 2.08),
         (3.10, 1.35), (2.09, 1.10), (1.83, 0.60)],
        [(1.63, 2.42), (2.42, 2.22), (1.88, 1.34), (2.64, 1.06), (3.21, 1.98),
         (3.95, 1.76), (3.00, 0.00)],
        [(1.34, 1.97), (2.61, 2.37), (2.26, 0.42), (1.37, 0.40), (1.67, 1.17),
         (3.65, 1.84), (3.00, 0.00)],
        [(0.91, 0.57), (1.07, 1.43), (1.82, 1.58), (1.93, 2.26), (2.65, 2.18),
         (2.57, 1.44), (3.15, 1.18), (3.00, 0.00)],
        
        # odfg
        [(1.74, 2.03), (3.34, 1.18), (3.87, 1.92), (3.06, 2.11), (2.20, 0.28),
         (3.00, 0.00)],
        [(1.49, 1.76), (1.22, 1.89), (1.46, 2.57), (3.89, 2.13), (3.62, 1.02),
         (2.51, 1.33), (2.17, 0.55)],
        [(3.77, 1.65), (3.39, 2.42), (2.49, 2.06), (2.88, 0.99), (1.64, 1.52),
         (2.00, 0.00)],
        [(3.36, 1.32), (2.78, 1.61), (2.70, 2.25), (2.18, 1.79), (1.50, 1.78),
         (3.00, 0.00)]]
    
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
    m = Matrix()
    m.translate(6.00, 3.46)
    m.scale(-1.0, 1.0) # flip vertical
    m.rotate(2.0*pi/3.0) # rotate 120 degrees
    GRAM_TRANSFORMS.append(m)
    
    # 0x03
    m = Matrix()
    m.translate(6.50, 6.06)
    m.rotate(pi) # rotate 180 degrees
    GRAM_TRANSFORMS.append(m)

    # 0x04
    m = Matrix()
    m.translate(4.00, 6.93)
    m.scale(-1.0, 1.0) # flip vertical
    m.rotate(2.0*pi/3.0) # rotate 120 degrees
    GRAM_TRANSFORMS.append(m)

    # 0x05
    m = Matrix()
    m.translate(6.00, 10.39)
    GRAM_TRANSFORMS.append(m)

    # 0x06
    m = Matrix()
    m.translate(10.00, 10.39)
    GRAM_TRANSFORMS.append(m)

    # paths to finish grams of varying numbers of glefs
    TAALS = [
        [(4.00, 0.00)],
        [(6.00, 3.44), (9.27, 3.00), (8.00, 0.00), (9.00, 0.00)],
        [(8.00, 7.21), (11.32, 6.73), (8.00, 0.00), (9.00, 0.00)],
        [(4.27, 7.35), (11.52, 6.43), (8.00, 0.00), (9.00, 0.00)],
        
        [(6.75, 10.82), (13.54, 9.50), (8.00, 0.00), (9.00, 0.00)],
        [(12.00, 6.93), (8.00, 0.00), (9.00, 0.00)],
        [(8.00, 0.00), (9.00, 0.00)],
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
        
    
