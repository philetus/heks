import gtk
from Canvas import Canvas
from Cursor import Cursor
from Style import Style

class Pad( Canvas ):
    """heks text editor window         
    """
    
    BACKGROUND = (0.2, 0.2, 0.2, 1.0) # gray background
    PAD = 4 # window pad in cells
    
    def __init__( self, gui, width=600, height=400 ):
        Canvas.__init__( self, gui ) # superclass constructor
        
        # set up window
        self.title = "heksbad"
        self.size = ( width, height )
        
        # init style and cursor
        self.style = Style()
        self.cursor = Cursor( self )     
        
        # horizontal scroll position in cells
        self.scroll = 0

        # list to hold containers
        self.containers = []
    
    def handle_draw( self, brush ):
        style = self.style
        width, height = self.size
        
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
        
        # draw containers
        h_off = self.PAD
        v_off = self.PAD
        for container in self.containers:
            
            # calculate mask position
            x0 = width - style.pixels( h_off - self.scroll )
            y0 = style.pixels( v_off )
            x1 = width - style.pixels( h_off + container.depth - self.scroll )
            y1 = style.pixels( v_off + container.length )
            
            # increment horizontal position as we go
            h_off += container.depth
            
            brush.push_mask( x0, y0, x1, y1 )
            container.handle_draw( brush, style )
            brush.pop_mask()
    
    def handle_quit( self ):
        #gtk.main_quit()
        #print "stopped gtk in pad"
        return True
        

