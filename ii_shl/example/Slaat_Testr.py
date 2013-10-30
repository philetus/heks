from heks.eesyl.Slaat import Slaat
from heks.juul.Wurd import Wurd

class Slaat_Testr(Slaat):
    """opens a slaat and renders a sentence
    """
    def __init__(self):
        Slaat.__init__(self, 
                       height=512, width=640,
                       scale=12.0, 
                       title="slaat testr")
    
    def braan_s(self):
        """print amusing aafforesynn about braan_s
        """
        self.handle_key('e')
        self.handle_key('y')
        
        # advance gram with hexed g
        self.handle_key('<heks>')
        self.handle_key('g')
        
        self.handle_key('n')
        self.handle_key('n')
        
        # advance wurd
        self.handle_key('<trgr>')
        
        self.handle_key('g')
        self.handle_key('u')
        self.handle_key('n')
        
        # advance gram with hexed g
        self.handle_key('<heks>')
        self.handle_key('g')

        self.handle_key('u')

        # advance line
        self.handle_key('<heks>')
        self.handle_key('<trgr>')
        
        self.handle_key('e')
        self.handle_key('e')
        self.handle_key('t')

        # advance wurd
        self.handle_key('<trgr>')

        self.handle_key('y')
        self.handle_key('o')
        self.handle_key('r')

        # advance wurd
        self.handle_key('<trgr>')
        
        self.handle_key('b')
        self.handle_key('r')
        self.handle_key('a')
        self.handle_key('a')
        self.handle_key('n')

        # advance gram with hexed g
        self.handle_key('<heks>')
        self.handle_key('g')

        self.handle_key('s')

        # advance line
        self.handle_key('<heks>')
        self.handle_key('<trgr>')

        self.handle_key('a')
        self.handle_key('n')
        self.handle_key('d')
        
        # advance line
        self.handle_key('<heks>')
        self.handle_key('<trgr>')

        self.handle_key('s')
        self.handle_key('t')
        self.handle_key('e')
        self.handle_key('e')
        self.handle_key('l')

        # advance wurd
        self.handle_key('<trgr>')

        self.handle_key('y')
        self.handle_key('o')
        self.handle_key('r')

        # advance wurd
        self.handle_key('<trgr>')
        
        self.handle_key('n')
        self.handle_key('a')
        self.handle_key('l')
        self.handle_key('e')
        self.handle_key('g')
        self.handle_key('g')

        # advance line
        self.handle_key('<heks>')
        self.handle_key('<trgr>')

if __name__ == "__main__":
    slaat = Slaat_Testr()
    slaat.start()

    
