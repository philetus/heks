from time import sleep
from l33tC4D.gui.Gui import Gui
from Pad import Pad
from Word import Word

gui = Gui()
gui.start()

pad = Pad( gui, 700, 500 )
pad.show()

sleep(1.0)

# add some chars to word for testing
pad.current_word.append('h')
pad.current_word.append('e')
pad.current_word.append('k')
pad.current_word.append('s')
pad.current_word.zoom = 2.0

wx = pad.size[0] - pad.PAD
wy = pad.PAD + pad.current_word.get_size()[1] + (8.0 * 2.0) 

pad.current_word = Word(wx, wy)
pad.words.append( pad.current_word )

pad.current_word.append('s')
pad.current_word.append('k')
pad.current_word.append('l')
pad.current_word.append('e')
pad.current_word.append('b')
pad.current_word.append('t')
pad.current_word.zoom = 2.0

# draw them
pad.redraw()
