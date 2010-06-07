class Cursor:
    """
    """
    
    def __init__( self, pad ):
        self.pad = pad
        self.container = None
        self.word = None
        self.glyph_index = 0
        self.x = 0.0 # horizontal position in cells
        self.y = 0.0 # vertical position in cells
    
    
    def advance( self ):
        """advance cursor by one glyph
        """
        pass
        
        
