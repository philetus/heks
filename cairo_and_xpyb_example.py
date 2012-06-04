import cairo
import xcb
from xcb.xproto import *

WIDTH, HEIGHT = 600, 600

def draw_spiral(ctx, width, height):
    """Draw a spiral with lines!"""
    wd = .02 * width
    hd = .02 * height

    width -= 2
    height -= 2

    
    for i in range(9):
        #print( "i: " + str(i))
        ctx.move_to (width + 1 + i, 1-hd)
        ctx.rel_line_to (0, height - hd * (2 * i - 1))
        ctx.rel_line_to (- (width - wd * (2 *i)), 0)
        ctx.rel_line_to (0, - (height - hd * (2*i)))
        ctx.rel_line_to (width - wd * (2 * i + 1), 0)

        ctx.set_source_rgb (0, 0, 1)
        ctx.stroke()

# Connect to the X server
conn = xcb.connect()

# Get the X server setup
setup = conn.get_setup()

# Generate X ID for our X "objects"
window = conn.generate_id()
pixmap = conn.generate_id()
gc = conn.generate_id()

# Create a new window
conn.core.CreateWindow(setup.roots[0].root_depth, window,
                       # Parent is the root window
                       setup.roots[0].root,
                       0, 0, WIDTH, HEIGHT, 0, WindowClass.InputOutput,
                       setup.roots[0].root_visual,
                       CW.BackPixel | CW.EventMask,
                       [ setup.roots[0].white_pixel, 
                       EventMask.ButtonPress 
                       | EventMask.EnterWindow 
                       | EventMask.LeaveWindow 
                       | EventMask.Exposure ])

# Create a pixmap: it will be used to draw with cairo
conn.core.CreatePixmap(setup.roots[0].root_depth, pixmap, setup.roots[0].root,
                       WIDTH, HEIGHT)

# We just need a GC to copy later the pixmap on the window, so create one
# very simple
conn.core.CreateGC(gc, setup.roots[0].root, GC.Foreground | GC.Background,
                   [ setup.roots[0].black_pixel, setup.roots[0].white_pixel ])

# Create a cairo surface
surface = cairo.XCBSurface (conn, pixmap,
                            setup.roots[0].allowed_depths[0].visuals[0], WIDTH, HEIGHT)
                            
# Create a cairo context with that surface
ctx = cairo.Context(surface)

# Paint everything in white
ctx.set_source_rgb (1, 1, 1)
ctx.set_operator (cairo.OPERATOR_SOURCE)
ctx.paint()

# Draw our spiral
draw_spiral (ctx, WIDTH, HEIGHT)

# Map the window on the screen so it gets visible
conn.core.MapWindow(window)

# Flush all X requests to the X server
conn.flush()

while True:
    try:
        event = conn.wait_for_event()
    except xcb.ProtocolException, error:
        print "Protocol error %s received!" % error.__class__.__name__
        break
    except:
        break

    # ExposeEvent are received when we need to refresh the content of the
    # window, so we copy the content of the pixmap (where cairo drew) in the
    # window
    if isinstance(event, ExposeEvent):
        conn.core.CopyArea(pixmap, window, gc, 0, 0, 0, 0, WIDTH, HEIGHT)
    # You click, I quit.
    elif isinstance(event, ButtonPressEvent):
        break
    conn.flush()
