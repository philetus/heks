import cairo
import xcb
from xcb.xproto import *
import time
from threading import Thread, Lock
from Krsr import Krsr

class Eesyl:
    """2d graphics window superclass
    
       drawing done with krsr provided in handle draw method
       
       krsr wraps cairo api to provide path drawing, stroking and filling
       
       windowing events managed with xpyb (the x [server] python binding)
       
       runs event handling loop in a separate thread to allow interaction
       with interpreter
    """

    def __init__(self, width=256, height=256):
        self._size = (width, height)
        
        # thread to run event loop
        self._event_thread = None
        
        # dirty flag to trigger window redraw
        self._dirty = True
        
        # going flag to break out of event loop
        self._going = False
        
        # connect to x server
        self._x_con = xcb.connect()
        
        # get the current x server root setup
        self._x_root = self._x_con.get_setup().roots[0]

        # generate x ids for our window, pixmap and xcb graphics context
        self._window = self._x_con.generate_id()
        self._pixmap = self._x_con.generate_id()
        self._xgc = self._x_con.generate_id()

        # create a new window
        self._x_con.core.CreateWindow(
            self._x_root.root_depth,
            self._window,
            self._x_root.root, # parent is the root window
            0,
            0,
            self._size[0], # width
            self._size[1], # height
            0,
            WindowClass.InputOutput,
            self._x_root.root_visual,
            CW.BackPixel | CW.EventMask,
            [ self._x_root.white_pixel, 
              EventMask.PointerMotion       # request events here
              | EventMask.ButtonPress 
              | EventMask.ButtonRelease
              | EventMask.KeyPress
              | EventMask.KeyRelease
              | EventMask.Exposure ])

        # create a pixmap for cairo drawing buffer
        self._x_con.core.CreatePixmap(
            self._x_root.root_depth,
            self._pixmap,
            self._x_root.root,
            self._size[0],
            self._size[1])

        # simple xcb graphics context for copying the pixmap buffer to window
        self._x_con.core.CreateGC(
            self._xgc, 
            self._x_root.root,
            GC.Foreground | GC.Background,
            [ self._x_root.black_pixel, self._x_root.white_pixel ])

        # create a cairo surface tied to pixmap buffer
        self._surface = cairo.XCBSurface(
            self._x_con,
            self._pixmap,
            self._x_root.allowed_depths[0].visuals[0],
            self._size[0],
            self._size[1])
                        
    def start(self):
        """start event handling (and rendering) loop
        """
        if self._event_thread is not None:
            raise ValueError("event loop already started!")
                
        # map the window on the screen so it is actually displayed
        self._x_con.core.MapWindow(self._window)

        # flush requests to x server
        self._x_con.flush()
        
        # set going flag
        self._going = True

        # start event loop in a separate thread
        self._event_thread = Thread(target=self._event_loop)
        self._event_thread.start()
        
    def redraw(self):
        """manually trigger a canvas redraw event
        """
        # set dirty flag to true to trigger a redraw in event thread
        self._dirty = True

    def destroy( self ):
        """manually trigger a window destroy event
        """
        raise NotImplementedError
            
    def get_title(self):
        """get current window title
        """
        raise NotImplementedError()

    def set_title(self, string):
        """set new window title
        """
        raise NotImplementedError()

    def get_size(self):
        """returns current window size as (width, height)
        """
        return self._size[0], self._size[1]
    
    def set_size(self, size):
        """takes (width, height) for new window size
        """
        raise NotImplementedError()

    def get_position(self):
        raise NotImplementedError()
    
    def set_position(self, position):
        raise NotImplementedError()

    def handle_draw(self, brush):
        """called to draw canvas contents with brush
        """
        raise NotImplementedError(
            "eesyl subclasses must implement a handle_draw method")

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
    
    def handle_keypress(self, key):
        """do something when key is pressed
        """
        pass

    def handle_keyrelease(self, key):
        """do something when key is released
        """
        pass
    
    def _on_draw(self):
        """clear window, call handle draw to generate content, send to x
        """
        # create krsr with new cairo context and pass to handle draw method
        krsr = Krsr(cairo.Context(self._surface), self._size)
        self.handle_draw(krsr)
                
        # copy buffer to screen  
        self._x_con.core.CopyArea(
            self._pixmap, 
            self._window, 
            self._xgc,
            0, 0, 0, 0, self._size[0], self._size[1])

        # flush requests to x server
        self._x_con.flush()
        
    def _event_loop(self):
        """runs event loop in a separate thread
        """
        while self._going:
            
            # check if an explicit redraw request has set the dirty flag
            # if it has redraw window from inside event loop
            if self._dirty:
                self._dirty = False
                self._on_draw()
            
            # poll for event without waiting to avoid hanging interpreter
            try:
                event = self._x_con.poll_for_event()
            
            # break out of event loop on error                   
            except Exception as error:
                print("error while polling for event: %s" % str(error))
                self._going = False 
                break
                        
            # check if event was returned from poll
            if event is None:
                pass
                
            # expose events are received when we need to refresh the content of
            # the window, so we copy the content of the pixmap (where cairo
            # drew) in the window
            elif isinstance(event, ExposeEvent):
                self._on_draw()
            
            elif isinstance(event, NoExposureEvent): # ???
                pass
            
            # pointer motion events
            elif isinstance(event, MotionNotifyEvent):
                self.handle_motion(self._size[0] - event.event_x, 
                                   event.event_y) 
                        
            # button events
            elif isinstance(event, ButtonPressEvent):
                self.handle_press(self._size[0] - event.event_x,
                                  event.event_y)
            
            elif isinstance(event, ButtonReleaseEvent):
                self.handle_release(self._size[0] - event.event_x,
                                    event.event_y)
            
            # key events
            elif isinstance(event, KeyPressEvent):
                print("key pressed!")
                print(dir(event))
                print("detail: %s" % event.detail)
            
            elif isinstance(event, KeyReleaseEvent):
                pass
            
            else:
                print("unhandled event! %s" % str(event))
            
            self._x_con.flush()        


