#!/usr/bin/python
from gi.repository import Gtk
import cairo
import math

def OnDraw(w, cr):
    cr.set_source_rgb(1, 1, 0)
    cr.arc(320,240,100, 0, 2*math.pi)
    cr.fill_preserve()

    cr.set_source_rgb(0, 0, 0)
    cr.stroke()

    cr.arc(280,210,20, 0, 2*math.pi)
    cr.arc(360,210,20, 0, 2*math.pi)
    cr.fill()

    cr.set_line_width(10)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.arc(320, 240, 60, math.pi/4, math.pi*3/4)
    cr.stroke()

w = Gtk.Window()
w.set_default_size(640, 480)
a = Gtk.DrawingArea()
w.add(a)

w.connect('destroy', Gtk.main_quit)
a.connect('draw', OnDraw)

w.show_all()

Gtk.main()

