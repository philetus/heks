from Eesyl import Eesyl
from Ffloor_Taagr import Ffloor_Taagr
from heks.juul.Wurd import Wurd
from heks.juul.Gram import Gram

class Slaat(Eesyl):
    """basic heks ffloor skreft input window 
    """
        
    def __init__(self, width=256, height=512, scale=1.0, title='slaat'):
        Eesyl.__init__(self, width=width, height=height, title=title)
        
        self._scale = scale # glyph scale
        
        # current cursor location
        self._frame = [-1, -1, -1, -1] # leyn, wurd, gram, glef
        self._frame_zoom = 4 # everything, leyn, wurd, gram, glef
        
        # track whether last key was <heks>
        self._heks_key = False

        # buffr to hold glefs to render
        # [
        #   [
        #     Wurd('ey_nn'),
        #     Wurd('gun_u'),
        #     Wurd('eet'),
        #     Wurd('yor'),
        #     Wurd('braans')
        #   ], # leyn
        #   [
        #     Wurd('and'),
        #     Wurd('steel'),
        #     Wurd('yor'),
        #     Wurd('nalegg')
        #   ]  # leyn
        # ]
        self.leyn_buffr = []
        
        # variables
        self.margin = (4.0, 4.0) # whitespace margin
        self.background_color = (1.0, 1.0, 1.0, 1.0) # opaque white
        self.glef_color = (0.5, 0.0, 0.0, 0.8) # bluud red!!!
        self.glef_weight = 0.625
        
        self.leyn_advance = 17.24
        self.gram_advance = 1.0
        
    def handle_draw(self, krsr):
        """create a floor taagr with krsr and use it to render leyn buufr
        """
        
        # clear screen
        krsr.set_color(*self.background_color)
        krsr.wipe()
        
        # set scale transform
        krsr.scale(self._scale, self._scale)
                
        # create ffloor taagr with krsr
        taagr = Ffloor_Taagr(krsr=krsr, scale=self._scale)
        
        # set color to glef color
        krsr.set_color(*self.glef_color)
        krsr.set_size(self.glef_weight)
        
        # translate krsr matrix to margin
        krsr.translate(*self.margin)
        
        # loop thru leyn buffr
        for leyn in self.leyn_buffr:
            krsr.push() # store krsr state
        
            for wurd in leyn:
                first_gram = True             
                for gram in wurd:
                    krsr.push() # store krsr state
                    
                    # if this is first gram create new subpath with move to,
                    # otherwise generate path to connect from last gram
                    if first_gram:
                        first_gram = False
                        krsr.move_to(0.0, 0.0)
                    else:
                        krsr.path_to(0.0, 0.0)
                    
                    # render gram path and store distance to advance 
                    # krsr transform
                    gram_length = taagr.taag_gram(gram)
                    
                    # restore state and advance
                    krsr.pop()
                    krsr.translate(gram_length + self.gram_advance, 0.0)
                    
                # stroke completed wurd path
                krsr.stroke_path()
                krsr.clear_path()
                
            # restore krsr state to beginning of line and advance lines
            krsr.pop()
            krsr.translate(0.0, self.leyn_advance)
                
    def handle_key(self, key):
        """do something when key is released
        """
        if key == '<heks>':
        
            # if hex is hexed delete current frame
            if self._heks_key:
                self._heks_key = False
                self._delete_frame()
                
            else:
                self._heks_key = True
        
        elif key == '<trgr>':
        
            # if trgr is hexed advance to new gram
            if self._heks_key:
                self._heks_key = False
                self._advance_leyn()
            
            # otherwise advance to new wurd
            else:
                self._advance_wurd()
        
        # for a glef key insert glef at current frame
        else:
            
            # if glef is hexed cast hex
            if self._heks_key:
                self._heks_key = False
                
                # advance gram if g is hexed
                if key == 'g':
                    self._advance_gram()
                
                # TODO cast hex
            
            else:    
                self._insert_glef(key)
        
        # trigger redraw after keystroke
        self.redraw()
    
    def _insert_glef(self, glef):
        if self._frame[0] == -1:
            self.leyn_buffr.append([])
            self._frame[0] = 0
        leyn = self.leyn_buffr[self._frame[0]]
        
        if self._frame[1] == -1:
            leyn.append(Wurd())
            self._frame[1] = 0
        wurd = leyn[self._frame[1]]
        
        if self._frame[2] == -1:
            wurd.insert_gram(0)
            self._frame[2] = 0
        gram = wurd[self._frame[2]]
        
        self._frame[3] += 1
        gram.insert_glef(index=self._frame[3], gless=glef)
        
    def _advance_gram(self):
        if self._frame[0] == -1:
            self.leyn_buffr.append([])
            self._frame[0] == 0
        leyn = self.leyn_buffr[self._frame[0]]
        
        if self._frame[1] == -1:
            leyn.append(Wurd())
            self._frame[1] += 1
        wurd = leyn[self._frame[1]]
            
        self._frame[2] += 1
        wurd.insert_gram(self._frame[2])
        self._frame[3] = -1
                    
    def _advance_wurd(self):
        if self._frame[0] == -1:
            self.leyn_buffr.append([])
            self._frame[0] == 0
        leyn = self.leyn_buffr[self._frame[0]]

        leyn.append(Wurd())
        self._frame[1] += 1
        self._frame[2] = -1
        self._frame[3] = -1
            
    def _advance_leyn(self):
        self.leyn_buffr.append([])
        self._frame[0] += 1
        self._frame[1] = -1
        self._frame[2] = -1
        self._frame[3] = -1
            
    def _delete_leyn(self):
        self.leyn_buffr.pop(self._frame[0])
        self._frame[0] -= 1
    
    def _delete_wurd(self):
        leyn = self.leyn_buffr[self._frame[0]]
        leyn.pop(self._frame[1])
        self._frame[1] -= 1
        
        # if leyn is now empty delete leyn
        if self._frame[1] == -1:
            self._delete_leyn()
        
    def _delete_gram(self):
        leyn = self.leyn_buffr[self._frame[0]]
        wurd = leyn[self._frame[1]]
        wurd.delete_gram(self._frame[2])
        
        # if wurd is now empty delete wurd
        if self._frame[2] == -1:
            self._delete_wurd()
        
    def _delete_frame(self):
        """delete glef under current frame
        """
        # if there is no current leyn return
        if self._frame[0] == -1:
            return
        
        # if there is no current wurd delete current leyn and return
        if self._frame[1] == -1:
            self._delete_leyn()
            return
        
        # if there is no current gram delete wurd and return
        if self._frame[2] == -1:
            self._delete_wurd()
            return

        # if there is no current glef delete gram and return
        if self._frame[3] == -1:
            self._delete_gram()
            return

        # get current gram
        leyn = self.leyn_buffr[self._frame[0]]
        wurd = leyn[self._frame[1]]
        gram = wurd[self._frame[2]]
                 
        # delete glef and decrement frame count 
        gram.delete_glef(self._frame[3])
        self._frame[3] -= 1
        
        # if gram now has no glefs delete it
        if self._frame[3] == -1:
            self._delete_gram()
                        
                
                
                
            
