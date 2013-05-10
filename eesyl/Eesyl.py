import cairo
import xcb
from xcb.xproto import *
import time
from threading import Thread
from Queue import Queue, Empty
from Krsr import Krsr

class Eesyl:
    """2d graphics window superclass
    
       drawing done with krsr provided in handle draw method
       
       krsr wraps cairo api to provide path drawing, stroking and filling
       
       windowing events managed with xpyb (the x [server] python binding)
       
       runs event handling loop in a separate thread to allow interaction
       with interpreter
    """
    
    # mapping from x server key codes to glish charset
    KEES = {
        38: 'a',
        45: 'k',
        29: 'y',
        46: 'l',

        26: 'e',
        28: 't',
        39: 's',
        27: 'r',
 
        30: 'u',
        56: 'b',
        43: 'h',
        57: 'n',
 
        32: 'o',
        40: 'd',
        41: 'f',
        42: 'g',

        37: '<heks>', # [l_ctrl]
        65: '<trgr>'  # [space]
    }
    
    def __init__(self, width=256, height=256, title='eesyl'):
        self._size = (width, height)
        self._position = (0, 0)
        self._title = title
        
        # thread to run event loop
        self._event_thread = None
        
        # thread and queue for control loop
        self._control_thread = None
        self._control_queue = Queue()
        
        # going flag to break out of control and event loops
        self._going = False
        
        # x server and cairo stuff
        self._x_con = None # connection to x server
        self._x_root = None # root x screen
        self._window = None # window id
        self._xgc = None # x graphics context id
        self._pixmap = None # x pixmap (draw buffer) id
        self._surface = None # cairo surface to draw to pixmap buffer
                                    
    def start(self):
        """start event handling (and rendering) loop
        """
        if self._event_thread is not None or self._control_thread is not None:
            raise ValueError("already started!")
                
        # set going flag
        self._going = True

        # start control loop in a separate thread
        self._control_thread = Thread(target=self._control_loop)
        self._control_thread.start()

        # start event loop in a separate thread
        self._event_thread = Thread(target=self._event_loop)
        self._event_thread.start()
        
    def redraw(self):
        """manually trigger an eesyl redraw event
        """
        # add redraw event to control queue
        event = {'type': 'redraw'}
        self._control_queue.put(event)

    def resurface(self, width, height):
        """trigger a resurface event
        """
        # add redraw event to control queue
        event = {'type': 'resurface',
                 'width': width,
                 'height': height}
        self._control_queue.put(event)

    def destroy( self ):
        """manually trigger a window destroy event
        """
        raise NotImplementedError
            
    def get_title(self):
        """get current window title
        """
        return self._title

    def retitle(self, title):
        """set new window title
        """
        # add retitle event to control queue
        event = {'type': 'retitle',
                 'title': title}
        self._control_queue.put(event)
        
    def get_size(self):
        """returns current window size as (width, height)
        """
        return self._size[0], self._size[1]
    
    def resize(self, width, height):
        """takes (width, height) for new window size
        """
        # add resize event to control queue
        event = {'type': 'resize',
                 'width': width,
                 'height': height}
        self._control_queue.put(event)

    def get_position(self):
        return self._position[0], self._position[1]
    
    def reposition(self, position):
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
    
    def handle_key(self, key):
        """do something when key is released
        """
        print(key)
    
    def _on_key(self, key_index):
        """handle key event
        """
        if key_index in self.KEES:
            self.handle_key(self.KEES[key_index])
    
    def _control_loop(self):
        """drives x connection from a single thread
        """        
        # initialize window when control loop is started
        self._x_init()
        
        # loop and poll for events until going flag is invalidated
        while self._going:
            
            # poll for an event on the control queue
            # call appropriate event handler function
            try:
                event = self._control_queue.get_nowait()
                
                if event['type'] == 'redraw':
                    self._redraw()
                elif event['type'] == 'resurface':
                    self._resurface(event['width'], event['height'])
                elif event['type'] == 'resize':
                    self._resize(event['width'], event['height'])
                elif event['type'] == 'reposition':
                    self._reposition(event['x'], event['y'])
                elif event['type'] == 'retitle':
                    self._retitle(event['title'])
                else:
                    raise ValueError("unknown control event: %s" % str(event))
                    self._going = False
               
            except Empty:
                time.sleep(0.01) # give up control when no events found
    
    def _x_init(self):
        """initialize window with x server
        """
        # connect to x server
        self._x_con = xcb.connect()
        
        # get the current x server root setup
        self._x_root = self._x_con.get_setup().roots[0]

        # generate x ids for our window and xcb graphics context
        self._window = self._x_con.generate_id()
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
              # request events here
              EventMask.PointerMotion       
              | EventMask.ButtonPress 
              | EventMask.ButtonRelease
              #| EventMask.KeyPress # heks key model is instant on release
              | EventMask.KeyRelease
              | EventMask.Exposure
              | EventMask.StructureNotify # get resize events?
              #| EventMask.ResizeRedirect 
              ])

        # simple xcb graphics context for copying the pixmap buffer to window
        self._x_con.core.CreateGC(
            self._xgc, 
            self._x_root.root,
            GC.Foreground | GC.Background,
            [ self._x_root.black_pixel, self._x_root.white_pixel ])
        
        # set the window title
        self._retitle(self._title)
        
        # generate drawing buffer and surface and draw contents of window
        self._resurface(*self._size)
        
        # map the window on the screen so it is actually displayed
        self._x_con.core.MapWindow(self._window)

        # flush requests to x server
        self._x_con.flush()

    def _redraw(self):
        """redraw contents of window as necessary
        """
        # create krsr with new cairo context and pass to handle draw method
        # handle draw method writes new screen image to buffer
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
    
    def _resurface(self, width, height):
        """get new pixmap buffer and cairo surface with given size
        """
        self._size = (width, height)

        # release old surface and pixmap
        if self._surface is not None:
            self._surface.finish()
            self._surface = None
        if self._pixmap is not None:
            self._x_con.core.FreePixmap(self._pixmap)
            self._pixmap = None
                
        # create a [new] pixmap for cairo drawing buffer
        self._pixmap = self._x_con.generate_id()
        self._x_con.core.CreatePixmap(
            self._x_root.root_depth,
            self._pixmap,
            self._x_root.root,
            self._size[0],
            self._size[1])
            
        # create a [new] cairo surface tied to pixmap buffer
        self._surface = cairo.XCBSurface(
            self._x_con,
            self._pixmap,
            self._x_root.allowed_depths[0].visuals[0],
            self._size[0],
            self._size[1])
        
        # redraw window contents to new surface
        self._redraw()

    def _resize(self, width, height):
        """change size of window
        """
        self._size = (width, height)
        
        # call configure window with width and height mask to resize
        self._x_con.core.ConfigureWindow(
            self._window,
            ConfigWindow.Width | ConfigWindow.Height,
            [width, height])
        
        # call resize handler
        self.handle_resize()
        
        # resized window needs resized drawing buffer and surface
        self._resurface(width, height)
    
    def _reposition(self, x, y):
        """move window on screen
        """
        raise NotImplementedError()
    
    def _retitle(self, title):
        """change window title
        """
        self._title = title
        
        self._x_con.core.ChangeProperty(
            PropMode.Replace, 
            self._window, 
            Atom.WM_NAME, 
            Atom.STRING,
            8,
            len(title),
            title)
         
        # flush x server request
        self._x_con.flush()

    def _event_loop(self):
        """runs event loop in a separate thread
        """
        while self._going:
            
            # poll for event without waiting to avoid hanging interpreter
            event = None
            try:
                #self._x_con.flush()
                event = self._x_con.poll_for_event()
            
            # break out of event loop on error                   
            except Exception as error:
                print("error while polling for event: %s" % str(error))
                self._going = False 
                raise error
                        
            # check if event was returned from poll
            if event is None:
                time.sleep(0.01) # give up control when no events found
                
            # trigger redraw on expose events
            elif isinstance(event, ExposeEvent):
                self.redraw()
            
            # window move and resize events
            elif isinstance(event, ConfigureNotifyEvent):
                
                # record current position
                self._position = (event.x, event.y)
                
                # if window height or width has changed trigger resurface event
                if self._size != (event.width, event.height):
                    self.resurface(event.width, event.height)
                                
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
            elif isinstance(event, KeyReleaseEvent):
                self._on_key(event.detail)
            
            # random unhelpful events
            elif isinstance(event, NoExposureEvent): # ???
                pass
            elif isinstance(event, MapNotifyEvent): # ???
                pass

            else:
                print("unhandled event! %s" % str(event))
            

