class Word:
    """stores characters of a word and draws them with a brush
    """
    
    # list of x, y pairs for drawing each glyph, in cells
    GLYPHS = { 'a' : [(0, 0), (5, 0), (7, 6), (11, 6), (13, 0)],
               'k' : [(0, 0), (9, 4), (9, 6), (5, 6), (5, 0), (13, 0)],
               'y' : [],
               'l' : [(0, 2), (7, 2), (7, 0), (11, 0), (9, 4), (11, 6), (7, 6)],
               'e' : [(0, 6), (9, 6), (9, 0), (13, 0)],
               'h' : [(0, 6), (5, 6), (7, 0), (9, 4), (13, 2), (11, 6)],
               's' : [(0, 0), (13, 2), (9, 4), (13, 6)],
               'w' : [],
               'u' : [],
               'b' : [(0, 4), (9, 4), (9, 6), (13, 6), (13, 0), (9, 2)],
               'm' : [],
               'd' : [],
               'o' : [],
               't' : [(0, 2), (13, 2), (5, 6), (5, 0)],
               'f' : [],
               'g' : [] }
               
    CELL = 2.0 # base cell size in pixels
    STROKE = 1.5 # stroke width in cells
    GLYPH_SPACE = 3.0 # space between glyphs in cells
    GLYPH_LENGTH = 6.0 # vertical dimension of glyph in cells
    GLYPH_DEPTH = 13.0 # horizontal dimension of glyph in cells
    BASE_OFFSET = 2.0 # base line horizontal offset in cells
    
    def __init__(self, anchor_x, anchor_y, zoom=1.0):
        self.anchor = [float(a) for a in (anchor_x, anchor_y)] # x, y pos in px
        self.chars = []
        self.length = self.GLYPH_SPACE # length of word in cells
        self.depth = self.GLYPH_DEPTH
        self.zoom = zoom # current zoom ratio
        
        self.base_color = (1.0, 1.0, 1.0, 0.8)
        self.glyph_color = (1.0, 1.0, 1.0, 1.0)
        
    def __str__( self ):
        return "".join( self.chars )
        
    def pxls( self, cells ):
        return cells * self.CELL * self.zoom
    
    def get_size( self ):
        """returns w, h of word in pixels
        """
        return (self.pxls(self.depth), self.pxls(self.length))
            
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
        self.length += self.GLYPH_LENGTH + self.GLYPH_SPACE
        
    def handle_draw( self, brush ):
        """draw word with brush
        """
        if len(self.chars) < 1:
            return
        
        # set brush size and color
        brush.size = self.pxls(self.STROKE)
        brush.color = self.base_color
        
        # draw baseline
        brush.move_to( self.anchor[0] - self.pxls(self.BASE_OFFSET),
                       self.anchor[1] )
        brush.path_by( 0, self.pxls(self.length) )
        brush.stroke_path()
        brush.clear_path()
        
        # draw characters
        brush.color = self.glyph_color
        for i, char in enumerate(self.chars):
            v_off = (self.GLYPH_SPACE 
                     + (i * (self.GLYPH_LENGTH + self.GLYPH_SPACE)))
            
            # get points and move to first one
            points = self.GLYPHS[char]
            brush.move_to( self.anchor[0] - self.pxls(points[0][0]),
                           self.anchor[1] + self.pxls(v_off + points[0][1]) )
            
            # connect rest
            for x, y in points[1:]:
                brush.path_to( self.anchor[0] - self.pxls(x),
                               self.anchor[1] + self.pxls(v_off + y) )
            
            # stroke path and then reset
            brush.stroke_path()
            brush.clear_path()
            
        
