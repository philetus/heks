from time import sleep
from l33tC4D.gui.Gui import Gui
from Pad import Pad
from Container import Container
from Phrase import Phrase
from Word import Word

gui = Gui()
gui.start()

pad = Pad( gui, 700, 500 )
pad.show()

#sleep(1.0)

container = Container()
pad.containers.append(container)

phrase = Phrase()
container.children.append(phrase)

heks = Word('heks')
phrase.words.append(heks)

sklebt = Word('sklebt')
phrase.words.append(sklebt)

# draw them
pad.redraw()
