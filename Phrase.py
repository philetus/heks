from Word import Word

class Phrase:
    """collection of words and numbers
    """
    
    WORD_SPACE = 4 # space between words in cells
    PAD = 2 # padding in cells
    BASE_WIDTH = 4 # width of base in cells
    
    def __init__( self ):
        self.words = []
    
    def update_anchors( self ):
        """recalculate position of word anchors
        """
        h_off = self.PAD
        v_off = self.PAD
        for word in self.words:
            word.anchor[0] = h_off
            word.anchor[1] = v_off
            v_off += word.length + self.WORD_SPACE
    
    def append_word( self, word ):
        """add new word to this phrase
        """
        self.words.append( word )
        
    @property
    def depth( self ):
        """horizontal size of phrase in cells
        """            
        return (self.PAD * 2) + Word.GLYPH_DEPTH
            
    @property
    def length( self ):
        """vertical size of phrase in cells
        """
        if len(self.words) < 1:
            return 0
            
        l = self.PAD * 2 - self.WORD_SPACE # subtract out first word space
        for word in self.words:
            l += self.WORD_SPACE
            l += word.length
        
        return l
    
    def handle_draw( self, brush, style ):
        """
        """
        print "drawing phrase"
        
        width, height = brush.mask_size
        
        # first draw phrase baseline
        brush.color = style.phrase_color
        brush.move_to( width, 0 )
        brush.path_by( 0, height )
        brush.path_by( -style.pixels(self.BASE_WIDTH), 0 )
        brush.path_by( 0, -height )
        brush.close_path()
        brush.fill_path()
        brush.clear_path()
        
        # draw words
        for word in self.words:
            word.handle_draw( brush, style )
