from heks.eesyl.Eesyl import Eesyl

class Leyn_Draur(Eesyl):
    """a simple line drawing application to test eesyl lib
    """
    def __init__(self):
        Eesyl.__init__(self, width=256, height=512, title="straight line draw test app")

        # flag tracks whether pointer is down
        self.pressed_flag = False
        
        # Variables to track rubber band for line being drawn
        self.first_point = None
        self.last_point = None

        # list of lines that have been drawn
        self.lines = [] # [((x0, y0), (x1, y1)), ...]

        # variables to control appearance of lines
        self.line_thickness = 5
        self.line_color = (1.0, 0.0, 0.0, 0.8) # slightly translucent red
        self.rubber_line_thickness = 2
        self.rubber_line_color = (0.0, 0.0, 0.0, 0.4) # translucent gray

        # background color to draw
        self.background_color = (1.0, 1.0, 1.0, 1.0) # opaque white
        
    def handle_press(self, y, x):
        """set anchor and flag when pointer is pressed
        """
        self.pressed_flag = True
        self.first_point = (y, x)

    def handle_release(self, y, x):
        """finalize line when pointer is released
        """
        # append new line to list of lines
        self.lines.append((self.first_point, (y, x)))

        # clear mouse pressed flag and rubber band line coords
        self.pressed_flag = False
        self.first_point = None
        self.last_point = None

        # trigger canvas to redraw itself
        self.redraw()

    def handle_motion(self, y, x):
        """follow depressed pointer with rubber band line
        """
        if self.pressed_flag:
            self.last_point = (y, x)

            # trigger canvas to redraw itself
            self.redraw()
        
    def handle_draw(self, krsr):
        """handle canvas redraw
          
           * draw all lines in the lines list       
           * if we are in the middle of drawing a line draw rubber band
        """        
        # draw background
        krsr.set_color(*self.background_color)
        krsr.wipe()
                
        # draw all lines in lines list
        krsr.set_color(*self.line_color)
        krsr.set_weight(self.line_thickness)
        for a, b in self.lines:
            krsr.move_to(*a) # move to beginning of line
            krsr.path_to(*b) # make path to end of line
            krsr.stroke_path() # stroke line with current color and thickness
            krsr.clear_path() # clear line path we just drew

        # if we are currently drawing a line draw rubber band
        if (self.first_point is not None) and (self.last_point is not None):
            krsr.set_color(*self.rubber_line_color)
            krsr.set_weight(self.rubber_line_thickness)
            krsr.move_to(*self.first_point)
            krsr.path_to(*self.last_point)
            krsr.stroke_path()
            krsr.clear_path()

    #TODO
    def handle_quit( self ):
        """say goodbye when we leave
        """
        print("bye!")

        # really close the window
        return True


if __name__ == "__main__":
    eesyl = Leyn_Draur()
    eesyl.start()

    
