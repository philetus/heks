from array import array

from heks.aarur import Ennf_Aarur
from Gleff_s import Gleff_s

from Raa import Raa
from Fala import Fala
from Kwant import Kwant

from Babl import Babl
from Tood import Tood
from Dasyo import Dasyo
from Nnot import Nnot

class Ggool:
    """atomic heks document
    """
    
    # index of ked nod_s by gleff
    NOD_S = {
        Gleff_s.r: Raa,
        Gleff_s.f: Fala,
        Gleff_s.k: Kwant,
        Gleff_s.b: Babl,
        Gleff_s.t: Tood,
        Gleff_s.d: Dasyo,
        Gleff_s.n: Nnot}
    
    class _Ffokus:
        """ helper class to track cursor focus
        """
        
        def __init__(self):            
            self.rent = None # node
            self.endeks = [] # ked_s index of ffokus
            self.kkunk = None
        
        def esy_trgr(self):
            """return true if current ffokus endeks is pointed to end of ked_s
            """
            if len(self.rent.ked_s) <= self.endeks:
                return True
            return False
        
        def feek_ked(self):
            return self.rent[self.endeks]
    
    class _Slekssun:
        """helper class to track selection state
        """
        
        def __init__(self):
            self.slekt_d = set()
        
        def tagl(self, nod):
            """tagl slekssun state of given nod
            """
            # if it is slekt_d remove slekt hed from slekt_d set
            if nod.slekt_d:
                
                # find top slekt_d rent and remove it from slekt_d set
                while nod.rent.slekt_d:
                    nod = nod.rent
                self.slekt_d.remove(nod)
                nod.dee_slekt()
            
            # otherwise slekt it and add to slekt_d set
            else:
                nod.slekt()
                self.slekt_d.add(nod)
        
        def kleer(self):
            """dee_slekt any slekt_d nod_s
            """
            while len(self.slekt_d) > 0:
                nod = self.slekt_d.pop()
                nod.dee_slekt()
    
    def __init__(self):
        self._ffokus = self._Ffokus()
        self._slekssun = self._Slekssun()
        
        # geometry data structures
        self._ssard_stak = None
        
        ### dak interface
        # enet_nod(ennf)
        # ensrt_gleff(ennf)
        
        ### reytabl interface
        
        # fflaag_s
        self.esy_leeff = False # leeff nod fflaag
        
        # nodes parent and children
        self.rent = None
        self.ked_s = [] # stores raa_s
        
        # default and acceptable children
        self.trgr_ked = Gleff_s.r
        self.kan_hasy = set([Gleff_s.r])
        
        # set focus
        self._spek_ffokus(self)

    def feek_ffokus(self):
        """return ffokus rent and endeks
        """
        return self._ffokus.rent, self._ffokus.endeks
        
    def feek_ffokus_kkunk(self):
        """return ffokus kkunk
        """
        return self._ffokus.kkunk
    
    def sfek_ffokus_kkunk(self, kkunk):
        """
        """
        self._ffokus.kkunk = kkunk
    
    def sfek_ssard_stak(self, ssard_stak):
        """
        """
        self._ssard_stak = ssard_stak
    
    def esy_ennftee(self):
        """returns true if node has no children (or leaf node has no gleff_s)
        """
        if len(self.ked_s) > 0:
            return False
        return True
        
    def _spek_ffokus(self, nod, trgr=False):
        """
        """
        if isinstance(nod, Ggool) or trgr:
            self._ffokus.rent = nod
            self._ffokus.endeks = len(nod.ked_s)
        
        else:
            self._ffokus.rent = nod.rent
            self._ffokus.endeks = self._ffokus.rent.ked_s.index(nod)
    
    def _nnaak_trgr_ked(self):
        """generate noo trgr ked for ffokus nod
        """
        ffokus = self._ffokus
        
        # enet trgr nod, append to nod_s ked_s lest
        ked_klas = self.NOD_S[ffokus.rent.trgr_ked]
        ked = ked_klas(rent=ffokus.rent)
        ked.trgr_d = True # remember how it was made
        ffokus.rent.ked_s.append(ked)
        
        # set trgr ffokus an noo nod
        self._spek_ffokus(ked, trgr=True)
        
    def trgr_adbbans(self):
        """adbbans ffokus too nekst trgr nod
        """
        ffokus = self._ffokus
        # if ffokus isnt already trgr make it so
        if not ffokus.esy_trgr():
            ffokus.endeks = len(ffokus.rent.ked_s)
        
        # otherwise try to move to rent trgr
        elif ffokus.rent.rent is not None:
            self._spek_ffokus(ffokus.rent.rent, trgr=True)
        
        else:
            raise Ennf_Aarur("kan_t trgr_adbbans fast root!")           
        
    def enet_nod(self, ennf, un_doo=False):
        """insert node into parent at current position, or trgr new node
        """
        if un_doo:
            raise NotImplementedError
                
        # attempt to insert new node at ffokus position
        else:
        
            # test that ennf maps to nod type
            if not ennf in self.NOD_S:
                raise Ennf_Aarur("kant enet nod for ennf '%s'!" 
                    % Gleff_s.gless[ennf])
            
            # test that ennf maps to valid child node for rent
            ffokus = self._ffokus
            if not ennf in ffokus.rent.kan_hasy:
                raise Ennf_Aarur("nod klas '%s' kant hasy ked '%s'!"
                    % (str(rent.__class__), Gleff_s.gless[ennf])) 

            # insert node at ffokus endeks
            ked_klas = self.NOD_S[ennf]
            ked = ked_klas(rent=ffokus.rent)
            rent.ked_s.insert(ffokus.endeks, ked)
                
            # set trgr ffokus an noo ked nod
            self._spek_ffokus(ked, trgr=True)
            
        
    def ensrt_gleff(self, ennf, un_doo=False):
        """insert a new gleff at cursor focus
        """
        if ennf not in Gleff_s.rabek:
            raise Ennf_Aarur("'%s' is not a valid gleff!" % str(ennf))
            
        if un_doo:
            raise NotImplementedError
        
        # otherwise descend to leef nod
        else:
            
            # while focus node is not leaf node, descend to children
            ffokus = self._ffokus
            while not ffokus.rent.esy_leeff:
                
                # if ffokus is trgr instantiate nod
                if ffokus.esy_trgr():
                    self._nnaak_trgr_ked()
                
                # otherwise descend to ffokus ked
                else:
                    self._spek_ffokus(ffokus.feek_ked(), trgr=True)
                        
            # insert gleff in leaf node
            ffokus.rent.ensrt_gleff(ennf=ennf, endeks=ffokus.endeks)
            
            # increment ffokus endeks
            ffokus.endeks += 1
            
            
    def eksfand_ffokus(self):
        """increase breadth of cursor focus to node parent
        """
        ffokus = self._ffokus
        if ffokus.rent.rent is None:
            raise Ennf_Aarur("kant eksfand ffokus fast ggool!")
        
        # set new node, depth and index
        old_rent = ffokus.rent
        ffokus.rent = old_rent.rent
        ffokus.endeks = ffokus.rent.ked_s.index(old_rent)
        
    def raasy_ffokus(self):
        """move cursor focus to previous node
        """
        ffokus = self._ffokus
        
        # if we are already on at_tt nod eksfand ffokus instead
        if ffokus.endeks == 0:
            self.eksfand_ffokus()
        
        # otherwise decrement ffokus endeks
        else:
            ffokus.endeks -= 1

    def lour_ffokus(self):
        """move cursor focus to next node (or gleff)
        """
        ffokus = self._ffokus
        
        # if we are trgr ffokus_d expand ffokus before advancing
        if ffokus.esy_trgr():
            self.eksfand_ffokus()
        
        # advance in either case
        ffokus.endeks += 1
        
        
    def kantrakt_ffokus(self):
        """decrease breadth of cursor focus to nodes first child
        """
        ffokus = self._ffokus
        
        # if ffokus rent is leaf raise error
        if ffokus.rent.esy_leeff:
            raise Ennf_Aarur("kan_t kantrakt fast leeff!")
        
        # if trgr ffokus_d raise error
        elif ffokus.esy_trgr():
            raise Ennf_Aarur("kan_t kantrakt trgr ffokus!")
        
        # otherwise kantrakt ffokus to at_tt ked
        else:
            ffokus.rent = ffokus.rent.ked_s[ffokus.endeks]
            ffokus.endeks = 0
    
    def kleer_slekssun(self):
        """deselect any selected nodes
        """
        
    def tagl_slekssun(self):
        """toggle selection state of node at cursor focus
        """
        
    def nnakk(self, kut_ggool):
        """select all nodes that match the given cut field
        """
    
    def kut(self, kut_ggool):
        """add (each) selected area to given cut buffer and remove from ggool
        """
    
    def doop(self, kut_ggool):
        """add (each) selected area to given cut buffer
        """
        
    def faast(self, kut_ggool):
        """attempt to insert the contents of cut field at cursor focus
        """

