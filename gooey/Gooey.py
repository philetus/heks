import gtk
gtk.set_interactive(False) # allow gtk threads with interactive console
gtk.gdk.threads_init() # allow gtk threads, must protect gtk calls

import time
from threading import Thread, current_thread

class Gooey( object ):
    """root level gooey class manages windows and gtk loop in separate thread
       
       this setup allows interactive interpreter to be used
    """

    def __init__( self ):
        # holds gtk main loop thread
        self._gtk_thread = None

        # set of running windows
        self.windows = set()

        # ident of thread currently inside gtk thread or none
        self.in_thread = None
    
    class Gtk_Lock(object):
        """used in 'with' block (potentially recursively) to guard gtk calls
        """
        
        def __init__(self, gooey, mark=False):
            self.gooey = gooey
            self.mark = mark # used inside callback to mark without locking
            self.really_leave = False
        
        def __enter__(self):
            # check current thread id
            ident = current_thread().ident
            if ident is None:
                raise ValueError("current thread ident is None!!!")
            
            # if in thread is None enter gtk thread now and store info
            if self.gooey.in_thread is None:
                self.gooey.in_thread = ident
                self.really_leave = True
                if not self.mark:
                    gtk.gdk.threads_enter()
            
            # otherwise if thread we are in is already in gtk thread ignore
            elif self.gooey.in_thread == ident:
                pass
            
            else:
                raise ValueError(
                    "attempted to enter gtk thread from different threads!")
                
            return None
            
        def __exit__(self, type, value, traceback):
            if self.really_leave:
                self.gooey.in_thread = None
                if not self.mark:
                    gtk.gdk.threads_leave()
        
    @property
    def lock(self):
        """return object to guard gtk calls inside 'with' block
        """
        return self.Gtk_Lock(self)
        
    @property
    def lock_marker(self):
        """return guard for use inside gtk callbacks that are already locked
        """
        return self.Gtk_Lock(self, mark=True)
    
    def _start_gtk( self ):
        print("starting gtk main loop")
        gtk.main()
        print("gtk main loop stopped")

    def show(self, window):
        """display window with gtk
        """
        # store reference
        self.windows.add(window)
        
        # call window's gooey init
        window._gooey_init(self)
        
    def start( self ):
        """start gui rendering loop
        """
        self._gtk_thread = Thread(target=self._start_gtk)
        self._gtk_thread.start()

    def stop(self):
        """stop gtk loop
        """
        with self.lock:
            gtk.main_quit()
            

