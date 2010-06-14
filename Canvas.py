import gtk
from Brush import Brush

class Canvas(object):
    """superclass for cross-platform 2d graphics application windows

       the window is filled with a 2d drawing surface that can be drawn to
       using the brush interface
       
       coords u, v are measured from upper right corner of canvas

       a draw handler taking a brush as an argument must be provided by
       subclasses to allow the canvas to redraw the window in a separate thread
       
       redraw events can be manually triggered by calling the redraw() method

       a pointer motion handler, a pointer button pressed handler and a pointer
       button released handler are provided to allow mouse events to be
       captured by providing the appropriate handler in a subclass

       the canvas is displayed to the screen by calling show()

       window quit events can be captured by providing a handle_quit() method
       in a subclass, and can be suppressed by returning False from the
       quit handler
    """

    def __init__(self, size=(600, 400), title="canvas"):
        # private gtk objects set whan gooey shows window
        self._gooey = None 
        self._window = None
        self._drawing_area = None
        
        # store initial window size and title for gooey init
        self._size = size
        self._title = title
        self._position = None

    def _gooey_init(self, gooey):
        """called by gooey when window is shown
        """
        self._gooey = gooey
        
        with self._gooey.lock:
        
            # set up gtk window
            self._window = gtk.Window()
            self._window.set_resize_mode(gtk.RESIZE_IMMEDIATE)
            self._window.set_reallocate_redraws(True)
            self._window.connect("destroy", self._on_quit)

            # set up drawing area widget
            self._drawing_area = gtk.DrawingArea()

            # set up callbacks
            self._drawing_area.set_events(gtk.gdk.POINTER_MOTION_MASK |
                                          gtk.gdk.BUTTON_RELEASE_MASK |
                                          gtk.gdk.BUTTON_PRESS_MASK )
            self._drawing_area.connect("expose_event", self._on_expose )
            self._drawing_area.connect("configure_event", self._on_configure)
            self._drawing_area.connect("motion_notify_event", self._on_motion)
            self._drawing_area.connect("button_press_event", self._on_press)
            self._drawing_area.connect("button_release_event", self._on_release)
            
            # add drawing area to window
            self._window.add(self._drawing_area)
            
            # set properties from initial values
            self.size = self._size
            self.title = self._title
            if self._position is not None:
                self.position = self._position
                  
            # show window when all set up
            self._window.show_all()
    
    def stop(self):
        """stop gtk
        """
        self._gooey.stop()

    def handle_quit(self):
        """return false to block closing window or call stop to kill gtk loop
        """
        return True
        
    def redraw(self):
        """manually trigger a canvas redraw event
        """
        with self._gooey.lock:
            self._drawing_area.queue_draw()

    def handle_draw(self, brush):
        """called to draw canvas contents with brush
        """
        raise NotImplementedError(
            "classes that subclass Canvas must implement a handle_draw method" )

    def handle_motion(self, x, y):
        """do something when pointer is moved over canvas
        """
        pass

    def handle_press(self, x, y):
        """do something when pointer button is triggered
        """
        pass

    def handle_release(self, x, y):
        """do something when pointer button is released
        """
        pass

    def handle_resize(self):
        """do something when window is resized
        """
        pass

    ###
    ### private functions to map gtk events to canvas handlers
    ###

    def _on_quit(self, window):
        """handler returns true to really close or calls stop() to kill loop
        """
        # just mark lock as callbacks are already inside gtk thread
        with self._gooey.lock_marker:
            return self.handle_quit()
        
    def _on_expose(self, drawing, event):
        # just mark lock as callbacks are already inside gtk thread
        with self._gooey.lock_marker:

            # get a new cairo context from the drawing area
            context = self._drawing_area.window.cairo_create()

            # set a clip region for the expose event
            context.rectangle(event.area.x, event.area.y,
                              event.area.width, event.area.height)
            context.clip()

            # call draw handler to draw contents of canvas to cairo context
            self.handle_draw(Brush(context, self.size))

            return False

    def _on_configure(self, drawing, event):
        # just mark lock as callbacks are already inside gtk thread
        with self._gooey.lock_marker:
            # update local size
            rect = self._drawing_area.get_allocation()
            self._size = rect.width, rect.height
            self.handle_resize()

    def _on_motion(self, drawing_area, event):
        # just mark lock as callbacks are already inside gtk thread
        with self._gooey.lock_marker:
            self.handle_motion(self._size[0] - event.x, event.y)

    def _on_press(self, drawing_area, event):
        # just mark lock as callbacks are already inside gtk thread
        with self._gooey.lock_marker:
            self.handle_press(self._size[0] - event.x, event.y)

    def _on_release( self, drawing_area, event ):
        # just mark lock as callbacks are already inside gtk thread
        with self._gooey.lock_marker:
            self.handle_release(self._size[0] - event.x, event.y)

    ###
    ### properties
    ###
    
    @property
    def title(self):
        """window title text
        """
        if self._window is None:
            return self._title
            
        with self._gooey.lock:
            return self._window.get_title()
    
    @title.setter
    def title(self, value):
        string = str(value)
        self._title = string
        
        if self._window is not None:
            with self._gooey.lock:
                self._window.set_title(string)
    
    @property
    def size(self):
        """width, height of canvas drawing area
        """
        return self._size
    
    @size.setter
    def size(self, value):
        width, height = (int(v) for v in value)
        self._size = width, height
        
        if self._window is not None:
            with self._gooey.lock:
                self._window.resize(width, height)
    
    @property
    def position(self):
        """x, y position of canvas window
        """
        if self._window is None:
            return self._position
        
        with self._gooey.lock:
            return self._window.get_position()

    @position.setter
    def position(self, value):
        x, y = (int(v) for v in value)
        self._position = x, y
        
        if self._window is not None:
            with self._gooey.lock:
                self._window.move(x, y)

