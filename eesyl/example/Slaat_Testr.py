from heks.eesyl.Slaat import Slaat
from heks.juul.Wurd import Wurd

class Slaat_Testr(Slaat):
    """opens a slaat and renders a sentence
    """
    def __init__(self):
        Slaat.__init__(self, 
                       height=512, width=640,
                       scale=6.0, 
                       title="slaat testr")

        self.leyn_buffr.append(
            [
                Wurd('ey_nn'),
                Wurd('gun_u'),
                Wurd('eet'),
                Wurd('yor'),
                Wurd('braans')
            ])
        self.leyn_buffr.append(
            [
                Wurd('and'),
                Wurd('steel'),
                Wurd('yor'),
                Wurd('nalegg')
            ])

if __name__ == "__main__":
    slaat = Slaat_Testr()
    slaat.start()

    
