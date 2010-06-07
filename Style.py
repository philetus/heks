class Style:
    """holds info about current rendering style
    """
    
    def __init__( self, cell=2.0 ):
        self.cell = cell # pixels per cell
        
        self.glyph_stroke = 1.5 # stroke width in cells
        self.glyph_color = (1.0, 1.0, 1.0, 1.0)
        
        self.base_stroke = 1.5 # stroke width in cells
        self.base_offset = 2.0 # base horizontal offset in cells
        self.base_color = (1.0, 1.0, 1.0, 0.8)
        
        self.phrase_color = (1.0, 1.0, 1.0, 0.6)

    def pixels( self, cells ):
        """convert cell value to pixels
        """
        return cells * self.cell


