from heks.eesyl.Slaat import Slaat
from heks.juul.Wurd import Wurd

class Slaat_Testr(Slaat):
    """opens a slaat and renders a sentence
    """
    def __init__(self):
        Slaat.__init__(self, 
                       height=512, width=256,
                       scale=8.0, 
                       title="slaat testr")

        self.leyn_buffr.append(
            [
                Wurd('a'),
                Wurd('k'),
                Wurd('ak'), 
                Wurd('ak_ak')
            ])

if __name__ == "__main__":
    slaat = Slaat_Testr()
    slaat.start()

    
