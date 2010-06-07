class Word:
    """stores characters of a word and draws glyphs with a brush
    """
    
    # list of x, y pairs for drawing each glyph, in cells
    GLYPHS = { 'a' : [(0, 0), (5, 0), (7, 6), (11, 6), (13, 0)],
               'k' : [(0, 0), (9, 4), (9, 6), (5, 6), (5, 0), (13, 0)],
               'y' : [(0, 4), (13, 2), (13, 6), (9, 6), (9, 0), (5, 0), 
                      (5, 6)],
               'l' : [(0, 2), (7, 2), (7, 0), (11, 0), (9, 4), (11, 6), 
                      (7, 6)],
               'e' : [(0, 6), (9, 6), (9, 0), (13, 0)],
               't' : [(0, 6), (11, 6), (11, 2), (9, 0), (7, 2), (13, 4)],
               's' : [(0, 0), (13, 2), (9, 4), (13, 6)],
               'w' : [(0, 0), (9, 0), (9, 2), (11, 2), (11, 4), (13, 4),
                      (13, 6)],
               'u' : [(0, 4), (13, 0), (11, 6), (9, 4), (5, 6)],
               'b' : [(0, 4), (9, 4), (9, 6), (13, 6), (13, 0), (9, 2)],
               'h' : [(0, 6), (5, 6), (7, 0), (9, 4), (13, 2), (11, 6)],
               'n' : [(0, 6), (13, 6), (13, 0), (9, 0), (9, 4)],
               'o' : [(0, 0), (5, 0), (9, 4), (5, 6), (7, 0)],
               'd' : [(0, 2), (13, 2), (5, 6), (5, 0)],
               'f' : [(0, 4), (13, 4), (13, 0), (9, 0), (9, 6), (7, 6), (7, 2)],
               'm' : [(0, 0), (0, 9), (13, 4), (11, 6), (5, 6)] }
    
    GLYPH_SPACE = 3.0 # space between glyphs in cells
    GLYPH_LENGTH = 6.0 # vertical dimension of glyph in cells
    GLYPH_DEPTH = 13.0 # horizontal dimension of glyph in cells
    
    def __init__(self, string=""):
        self.chars = [str(c) for c in string]
        self.anchor = [0, 0] # position in cells
                
    def __str__( self ):
        return "".join( self.chars )
                    
    def append( self, char ):
        """add glyph at end of word by char
        """
        self.insert( len(self.chars), char )
        
    def insert( self, offset, char ):
        """insert glyph into word at given offset
        """
        if char not in self.GLYPHS:
            raise ValueError( "error: '" + str(char) + "' not a known glyph!" )
        
        self.chars.insert( offset, char )
        
    @property
    def depth( self ):
        """horizontal size of word in cells
        """
        return self.GLYPH_DEPTH
            
    @property
    def length( self ):
        """vertical size of word in cells
        """
        if len(self.chars) < 1:
            return 0
            
        return self.GLYPH_SPACE + ((self.GLYPH_SPACE + self.GLYPH_LENGTH)
                                   * len(self.chars))
        
    def handle_draw( self, brush, style ):
        """draw word with brush
        """
        if len(self.chars) < 1:
            return
        
        print "drawing word"
        
        # set brush size and color
        brush.size = style.pixels(style.base_stroke)
        brush.color = style.base_color
        
        # draw baseline
        brush.move_to( style.pixels(self.anchor[0] - style.base_offset),
                       style.pixels(self.anchor[1]) )
        brush.path_by( 0, style.pixels(self.length) )
        brush.stroke_path()
        brush.clear_path()
        
        # draw glyph
        brush.size = style.pixels(style.glyph_stroke)
        brush.color = style.glyph_color
        for i, char in enumerate(self.chars):
            v_off = (self.GLYPH_SPACE 
                     + (i * (self.GLYPH_LENGTH + self.GLYPH_SPACE)))
            
            # get points and move to first one
            points = self.GLYPHS[char]
            brush.move_to( style.pixels(self.anchor[0] - points[0][0]),
                           style.pixels(self.anchor[1] + v_off + points[0][1]) )
            
            # connect rest
            for x, y in points[1:]:
                brush.path_to( style.pixels(self.anchor[0] - x),
                               style.pixels(self.anchor[1] + v_off + y) )
            
            # stroke path and then reset
            brush.stroke_path()
            brush.clear_path()
            
        
