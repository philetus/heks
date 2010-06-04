from l33tC4D.gui.Canvas import Canvas
from Word import Word

class Pad( Canvas ):
    """
    """
    
    BACKGROUND = (0.2, 0.2, 0.2, 1.0) # gray background
    PAD = 20.0 # window pad in pixels
    
    def __init__( self, gui, width=600, height=400 ):
        Canvas.__init__( self, gui ) # superclass constructor
        
        # set up window
        self.title = "heksbad"
        self.size = ( width, height )

        # set up words
        self.current_word = Word( self.size[0] - self.PAD, self.PAD )
        self.words = [ self.current_word ]
    
    
    def handle_draw( self, brush ):
        
        # draw background
        brush.color = self.BACKGROUND
        width, height = self.size
        brush.move_to( 0, 0 )
        brush.path_to( width, 0 )
        brush.path_to( width, height )
        brush.path_to( 0, height )
        brush.close_path()
        brush.fill_path()
        brush.clear_path()
        
        # draw words
        for word in self.words:
            word.handle_draw( brush )

