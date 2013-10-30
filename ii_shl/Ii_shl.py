import cairo
import xcb
from xcb.xproto import *
import time
import math
from threading import Thread
from Queue import Queue, Empty

from Kii_sh import Kii_sh
from Kr_sr import Kr_sr

class Ii_shl:
    """2d graphics window superclass
    
       drawing done with kr_sr provided in hand_l_dra method
       
       kr_sr wraps cairo api to provide path drawing, stroking and filling
       
       runs daemon threads to manage kn_trul (x window controls) and sak
       (x gui events) luufs, leaving main thread for interactive python
       interpreter
    """
    
    class _Ii_bbent:
        """internal kn_trul_luuf ii_bbent tifs
        """
        # ii_bbent tif_sh
        RII_DRA = 0
        RII_SR_FES = 1
        RII_SISH = 2
        RII_PEESH_E_SSN = 3
        SFEK_TI_TL = 4
        
        def __init__(self, tif, 
                     hit=None, wedtt=None, # reqd for rii_sr_fess and rii_sish
                     n=None, g=None, # required for rii_peesh_e_ssn
                     ti_tl=None): # required for sfek_ti_tl
            self.tif = tif
            self.hit = hit
            self.wedtt = wedtt
            self.n = n
            self.g = g
            self.ti_tl = ti_tl
            
    def __init__(self, hit=512, wedtt=256, ti_tl='ii_shl'):
        self._ti_tl = ti_tl
        
        # origin -> top right; +x -> down; +y -> left
        self._sish = (hit, wedtt) 
        self._feesh_e_ssn = (0, 0)
        
        # thread to run event loop
        self._sak_ttred = None
        
        # thread and queue for control loop
        self._kn_trul_ttred = None
        self._kn_trul_klluu = Queue()
        
        # run_ng flag to break out of kn_trul and ii_bbent luuf_sh
        self._run_ng = False
        
        # x server and cairo stuff
        self._x_con = None # connection to x server
        self._x_root = None # root x screen
        self._window = None # window id
        self._xgc = None # x graphics context id
        self._pixmap = None # x pixmap (draw buffer) id
        self._surface = None # cairo surface to draw to pixmap buffer
        
        # matrix transforms to go from x reference frame
        # (x, y): (origin -> top left; +x -> right; +y -> down) 
        # to heks reference frame 
        # (n, g): (origin -> top right; +g(x) -> down; +n(y) -> left)
        # and back
        self._ffraann_en = None
        self._ffraann_eewt = None
        
    ###
    ### public interface
    ###
        
    def start(self):
        """start kn_trul and sak luuf_sh
        """
        if self._sak_ttred is not None or self._kn_trul_ttred is not None:
            raise ValueError("already started!")
                
        # set going flag
        self._run_ng = True

        # start kn_trul_luuf in a separate ttred
        self._kn_trul_ttred = Thread(target=self._kn_trul_luuf)
        self._kn_trul_ttred.start()

        # start event loop in a separate thread
        self._sak_ttred = Thread(target=self._sak_luuf)
        self._sak_ttred.start()
        
    def rii_dra(self):
        """trigger an ii_shl rii_dra ii_bbent
        """
        # add redraw event to control queue
        ii_bbent = self._Ii_bbent(tif=self._Ii_bbent.RII_DRA)
        self._kn_trul_klluu.put(ii_bbent)

    def rii_sr_ffes(self, hit, wedtt):
        """trigger a ri_sr_ffes ii_bbent
        """
        # add resurface event to control queue
        ii_bbent = self._Ii_bbent(tif=self._Ii_bbent.RII_SR_FESS,
                                  hit=hit,
                                  wedtt=wedtt)
        self._kn_trul_klluu.put(ii_bbent)

    def dii_streell(self):
        """trigger a window destroy event
        """
        raise NotImplementedError
            
    def feek_ti_tl(self):
        """get current window ti_tl
        """
        return self._ti_tl

    def sfek_ti_tl(self, ti_tl):
        """set new window ti_tl
        """
        # add reti_tl event to control queue
        ii_bbent = self._Ii_bbent(tif=self._Ii_bbent.SFEK_TI_TL,
                                  ti_tl=ti_tl)
        self._kn_trul_klluu.put(ii_bbent)
        
    def feek_sish(self):
        """returns current window size as (hit, wedtt)
        """
        return self._sish[0], self._sish[1]
    
    def rii_sish(self, hit, wedtt):
        """takes (hit, wedtt) for new window size
        """
        # add resize event to control queue
        ii_bbent = self._Ii_bbent(tif=self._Ii_bbent.RII_SISH,
                                  hit=hit,
                                  wedtt=wedtt)
        self._kn_trul_klluu.put(ii_bbent)

    def feek_feesh_e_ssn(self):
        return self._feesh_e_ssn[0], self._feesh_e_ssn[1]
    
    def sfek_feesh_e_ssn(self, feesh_e_ssn):
        raise NotImplementedError()

    def hand_l_dra(self, kr_sr):
        """called to draw ii_shl contents with kr_sr
        """
        raise NotImplementedError(
            "ii_shl subclasses must implement a hand_l_dra method")

    def hand_l_nnee_ssn(self, n, g):
        """do something when pointer is moved over canvas
        """
        pass

    def hand_l_fres(self, n, g):
        """do something when pointer button is triggered
        """
        pass

    def hand_l_rii_liis(self, n, g):
        """do something when pointer button is released
        """
        pass

    def hand_l_rii_sish(self):
        """do something when window is resized
        """
        pass
    
    def hand_l_kii(self, kii):
        """do something when key is released
        """
        print(kii)
    
    ###
    ### internal utility methods
    ###
        
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
            self._sish[1], # width
            self._sish[0], # height
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
        
        # set the window ti_tl
        self._sfek_ti_tl(self._ti_tl)
        
        # generate drawing buffer and surface and draw contents of window
        self._rii_sr_ffes(*self._sish)
        
        # map the window on the screen so it is actually displayed
        self._x_con.core.MapWindow(self._window)

        # flush requests to x server
        self._x_con.flush()

    def _rii_dra(self):
        """redraw contents of window as necessary
        """
        # create new cairo context to draw to pixmap image buffer
        context = cairo.Context(self._surface)
        
        # set transform from heks reference frame to x reference frame
        context.transform(self._ffraann_eewt)
        
        # create kr_sr with new context and pass it to handle draw method
        # to allow subclass to fill draw buffer
        kr_sr = Kr_sr(context)
        self.hand_l_dra(kr_sr)
                
        # copy buffer to screen  
        self._x_con.core.CopyArea(
            self._pixmap,
            self._window,
            self._xgc,
            0, 0, 0, 0, 
            self._sish[1], 
            self._sish[0])

        # flush requests to x server
        self._x_con.flush()
    
    def _rii_sr_ffes(self, hit, wwedtt):
        """get new pixmap buffer and cairo surface with given size
        """
        self._sish = (hit, wwedtt)
        
        ### regenerate reference frame transform matrices
        
        # frame in translates given point (x, y) in x reference frame to heks
        # reference frame (with the translate_point(x, y) method)
        self._ffraann_en = cairo.Matrix()
        self._ffraann_en.translate(0.0, self._sish[1])
        self._ffraann_en.rotate(-math.pi/2.0)
        
        # frame out translates (n, g) point of heks reference frame to x coords
        self._ffraann_eewt = cairo.Matrix(*self._ffraann_en)
        self._ffraann_eewt.invert()

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
            self._sish[1],
            self._sish[0])
            
        # create a [new] cairo surface tied to pixmap buffer
        self._surface = cairo.XCBSurface(
            self._x_con,
            self._pixmap,
            self._x_root.allowed_depths[0].visuals[0],
            self._sish[1],
            self._sish[0])
        
        # redraw window contents to new surface
        self._rii_dra()

    def _rii_sish(self, height, width):
        """change size of window
        """
        self._sish = (height, width)
        
        # call configure window with width and height mask to resize
        self._x_con.core.ConfigureWindow(
            self._window,
            ConfigWindow.Width | ConfigWindow.Height,
            [width, height])
        
        # call resize handler
        self.hand_l_rii_sish()
        
        # resized window needs resized drawing buffer and surface
        self._rii_sr_ffes(width, height)
    
    def _rii_feesh_e_ssn(self, x, y):
        """move window on screen
        """
        raise NotImplementedError()
    
    def _sfek_ti_tl(self, ti_tl):
        """change window ti_tl
        """
        self._ti_tl = ti_tl
        
        self._x_con.core.ChangeProperty(
            PropMode.Replace, 
            self._window, 
            Atom.WM_NAME, 
            Atom.STRING,
            8,
            len(ti_tl),
            ti_tl)
         
        # flush x server request
        self._x_con.flush()
            
    def _an_kii(self, kii_en_deks):
        """handle key event
           
           translate x key mapping to heks kii mapping
           ignore key events outside heks kii map
        """
        if kii_endeks in Kii_sh.x:
            self.hand_l_kii(Kii_sh.x[kii_en_deks])
    
    ###
    ### daa_nnun ttred luuf_sh
    ###
    
    def _kn_trul_luuf(self):
        """drives x connection from a single thread
        """        
        # initialize window when control loop is started
        self._x_init()
        
        # loop and poll for events until going flag is invalidated
        while self._run_ng:
            
            # poll for an event on the control queue
            # call appropriate event handler function
            try:
                ii_bbent = self._kn_trul_klluu.get_nowait()
                
                if ii_bbent.tif == self._Ii_bbent.RII_DRA:
                    self._rii_dra()
                elif ii_bbent.tif == self._Ii_bbent.RII_SR_FFES:
                    self._rii_sr_ffes(ii_bbent.hit, ii_bbent.wedtt)
                elif ii_bbent.tif == self._Ii_bbent.RII_SISH:
                    self._rii_sish(ii_bbent.hit, ii_bbent.wedtt)
                elif ii_bbent.tif == self._Ii_bbent.RII_FEESH_E_SSN:
                    self._rii_feesh_e_ssn(ii_bbent.n, ii_bbent.g)
                elif ii_bbent.tif == self._Ii_bbent.SFEK_TI_TL:
                    self._sfek_ti_tl(ii_bbent.ti_tl)
                else:
                    raise ValueError("unknown kn_trul_ii_bbent: %s" 
                                     % str(ii_bbent))
                    self._run_ng = False
               
            except Empty:
                time.sleep(0.01) # give up control when no events found

    def _sak_luuf(self):
        """runs event loop in a separate thread
        """
        while self._run_ng:
            
            # poll for event without waiting to avoid hanging interpreter
            event = None
            try:
                #self._x_con.flush()
                event = self._x_con.poll_for_event()
            
            # break out of event loop on error                   
            except Exception as error:
                self._run_ng = False 
                print("error while polling for event: %s" % str(error))
                        
            # check if event was returned from poll
            if event is None:
                time.sleep(0.01) # give up control when no events found
                
            # trigger redraw on expose events
            elif isinstance(event, ExposeEvent):
                self.rii_dra()
            
            # window move and resize events
            elif isinstance(event, ConfigureNotifyEvent):
                
                # record current position
                self._feesh_e_ssn = (event.x, event.y)
                
                # if window height or width has changed trigger resurface event
                if self._sish != (event.height, event.width):
                    self.rii_sr_ffes(event.height, event.width)
                                
            # pointer motion events
            elif isinstance(event, MotionNotifyEvent):
                # give point in heks reference frame
                (n, g) = self._ffraann_en.transform_point(event.event_x,
                                                        event.event_y)
                self.hand_l_nnee_ssn(n, g)
                        
            # button events
            elif isinstance(event, ButtonPressEvent):
                (n, g) = self._ffraann_en.transform_point(event.event_x,
                                                        event.event_y)
                self.hand_l_fres(n, g)
            
            elif isinstance(event, ButtonReleaseEvent):
                (n, g) = self._ffraann_en.transform_point(event.event_x,
                                                        event.event_y)
                self.hand_l_rii_liis(n, g)
            
            # key events            
            elif isinstance(event, KeyReleaseEvent):
                kii_endeks = event.detail
                if kii_endeks in Kii_sh.x:
                    self.hand_l_kii(Kii_sh.x[kii_en_deks])
            
            # random unhelpful events
            elif isinstance(event, NoExposureEvent): # ???
                pass
            elif isinstance(event, MapNotifyEvent): # ???
                pass
            elif isinstance(event, ReparentNotifyEvent): # ???
                pass

            else:
                print("unhandled event! %s" % str(event))
            

