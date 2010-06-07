class Container:
    """contains phrases and containers
    """
    
    SPECIES = { 'paragraph' : 0,
                'verse' : 1, # numbered phrases (code block)
                'list' : 2,
                'dictionary' : 3,
                'set' : 4,
                'class' : 5,
                'method' : 6 }
    
    PAD = 4 # padding in cells
    PHRASE_SPACE = 4 # horizontal offset between phrases in cells
    
    def __init__( self, species="paragraph" ):
        self.species = self.SPECIES[species]        
        self.children = []
    
    @property
    def depth( self ):
        """horizontal size of container in cells
        """
        if len(self.children) < 1:
            return 0
            
        d = (self.PAD * 2) - self.PHRASE_SPACE # subtract out first phrase space
        for phrase in self.children:
            d += self.PHRASE_SPACE
            d += phrase.depth
        
        return d
            
    @property
    def length( self ):
        """vertical size of container in cells
        """
        if len(self.children) < 1:
            return 0
            
        l = self.PAD * 2
        l += max(phrase.length for phrase in self.children)
        
        return l
    
    def handle_draw( self, brush, style ):
        width, height = brush.mask_size
        
        # draw phrases
        h_off = self.PAD
        v_off = self.PAD
        for phrase in self.children:
            
            # calculate mask position
            x0 = width - style.pixels( h_off )
            y0 = style.pixels( v_off )
            x1 = width - style.pixels( h_off + phrase.depth )
            y1 = style.pixels( v_off + phrase.length )
            
            # increment horizontal position as we go
            h_off += phrase.depth
            
            brush.push_mask( x0, y0, x1, y1 )
            phrase.handle_draw( brush, style )
            brush.pop_mask()
        
