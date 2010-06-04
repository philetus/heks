class Cursor:
    """
    """
    
    def __init__( self, pad ):
        self.pad = pad
        self.word = 0
        self.glyph = 0
        self.x = 0.0
        self.y = 0.0
    
    
    def advance( self ):
        """advance cursor by one glyph
        """
        
        
