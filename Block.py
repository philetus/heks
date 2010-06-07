class Container:
    """contains phrases
    """
    
    SPECIES = { 'paragraph' : 0,
                'list' : 1,
                'dictionary' : 2,
                'set' : 3 }
    
    PAD = 2 # padding in cells
    PHRASE_SPACE = 4 # horizontal offset between phrases in cells
    
    def __init__( self, species="paragraph" ):
        self.species = self.SPECIES[species]
        
        self.depth = 0 # x in cells
        self.length = 0 # y in cells
        self.phrases = []
    
    def handle_draw( self, brush, style ):
