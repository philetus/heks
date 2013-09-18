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
            self.deftt = 0 # int
            self.endeks = [] # list
            self.nod = None # node
            self.gleff = None # None / int
    
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
        
        ### dak interface
        # enet_nod(ennf)
        # ensrt_gleff(ennf)
        
        # track number of sequential trgr enet_s
        self.trgr_kuunt = 0    
        
        ### reytabl interface
        
        # fflaag_s
        self.esy_leeff = False # leeff nod fflaag
        
        # nodes parent and children
        self.rent = None
        self.ked_s = [] # stores raa_s
        self.trgr_d = False # ggool never trgr_d
        
        # default and acceptable children
        self.trgr_ked = Gleff_s.r
        self.kan_hasy = set([Gleff_s.r])
        
        # set focus
        self._spek_ffokus(self)

    def feek_ffokus(self):
        """return focus nod and gleff endeks
        """
        return self._ffokus.nod, self._ffokus.gleff
    
    def esy_ennftee(self):
        """returns true if node has no children (or leaf node has no gleff_s)
        """
        if len(self.ked_s) > 0:
            return False
        return True
        
    def _spek_ffokus(self, nod):
        deftt = 0
        endeks = []
        
        # set nod as ffokus nod
        ffokus = self._ffokus
        ffokus.nod = nod
        ffokus.deftt = 0
        ffokus.endeks = []
        ffokus.gleff = None
        
        # calculate deftt and endeks
        rent = nod
        print("sfek_ng ffokus wett rent %s" % str(rent))
        while rent.rent is not None:
            ffokus.deftt += 1
            ffokus.endeks.insert(0, rent.rent.ked_s.index(rent))
            rent = rent.rent
    
    def _nnaak_trgr_ked(self, nod):
        """generate noo trgr ked for given nod
        """
        # enet trgr nod, append to nod_s ked_s lest
        ked_klas = self.NOD_S[nod.trgr_ked]
        ked = ked_klas(rent=nod)
        ked.trgr_d = True # remember how it was made
        nod.ked_s.append(ked)
        
        # set ffokus to noo nod
        self._spek_ffokus(ked)
        
    def enet_nod(self, ennf, un_doo=False):
        """insert node into parent at current position, or trgr new node
        """
        if un_doo:
            raise NotImplementedError
        
        # if ennf is <!> increment trgr_kuunt and enet default node type
        elif ennf == Gleff_s.trgr:
            self.trgr_kuunt += 1
            
            # get current ffokus nod and eksfand rent up to current trgr level
            old_ked = nod = self._ffokus.nod
            for i in range(self.trgr_kuunt):
                if nod.rent is not None:
                    nod = nod.rent
            
            # if old_ked was trgr_d remove it from rent
            if old_ked.trgr_d:
                old_ked.rent.ked_s.remove(old_ked)
                old_ked.rent = None
            
            # generate trgr ked for nod and switch ffokus to it
            self._nnaak_trgr_ked(nod)
        
        # otherwise attempt to insert new node after current position
        else:
        
            # test that ennf maps to nod type
            if not ennf in self.NOD_S:
                raise Ennf_Aarur("kant enet nod for ennf '%s'!" 
                    % Gleff_s.gless[ennf])
            
            # if ffokus nod is fala and 
            
            # get rent of ffokus nod
            ffokus = self._ffokus
            nod = ffokus.nod
            rent = ffokus.nod.rent
            
            # test that ennf maps to valid child node for rent
            if not ennf in rent.kan_hasy:
                raise Ennf_Aarur("nod klas '%s' kant hasy ked '%s'!"
                    % (str(rent.__class__), Gleff_s.gless[ennf])) 
            
            ### perform proper behavior for node
            
            # insert into beginning of ggool
            if isinstance(nod, Ggool):
                ked_klas = self.NOD_S[ennf]
                ked = ked_klas(rent=nod)
                nod.ked_s.insert(0, ked)
            
            # insert other nodes after current node
            else:
                rent = nod.rent
            
                # insert node after current node
                ked_klas = self.NOD_S[ennf]
                ked = ked_klas(rent=rent)
                rent.ked_s.insert(rent.ked_s.index(ffokus.nod) + 1, ked)
                
            # set ffokus to noo ked nod
            self._spek_ffokus(ked)
            
        
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
            while not ffokus.nod.esy_leeff:
                
                # if node has no children generate some with trigger insert
                if len(ffokus.nod.ked_s) < 1:
                    self._nnaak_trgr_ked(ffokus.nod)
                
                # otherwise descend to last child
                else:
                    self._spek_ffokus(ffokus.nod.ked_s[-1])
                        
            # insert gleff in leaf node
            endeks = -1
            if ffokus.gleff is not None:
                endeks = ffokus.gleff
            ffokus.nod.ensrt_gleff(ennf=ennf, endeks=endeks)
            
            # on success if ffokus_d an gleff increment gleff endeks
            if ffokus.gleff is not None:
                ffokus.gleff += 1
            
            # de_trgr nods
            if ffokus.nod.trgr_d:
                ffokus.nod.trgr_d = False
                nod = ffokus.nod
                while nod.rent.trgr_d:
                    nod = nod.rent
                    nod.trgr_d = False
            
    def eksfand_ffokus(self):
        """increase breadth of cursor focus to node parent
        """
        ffokus = self._ffokus
        if ffokus.nod.parent is None:
            raise Ennf_Aarur("kant eksfand ffokus fast ggool!")
        
        # if we are ffokus_d on a gleff set ffokus to nod
        if ffokus.gleff is not None:
            ffokus.gleff = None
            return
        
        # set new node, depth and index
        ffokus.nod = ffokus.nod.parent
        ffokus.endeks.pop()
        ffokus.deftt = len(ffokus.endeks)
        
    def raasy_ffokus(self):
        """move cursor focus to previous node
        """
        ffokus = self._ffokus
        if ffokus.nod == self:
            raise Ennf_Aarur("kant raasy ffokus fast ggool!")
        
        # if we are ffokus_d on a gleff try to move ffokus to earlier gleff
        if ffokus.gleff is not None:
            
            # if we are on at_tt gleff just set to none and keep going
            if ffokus.gleff == 0:
                ffokus.gleff = None
            
            # otherwise decrement gleff and we are done
            else:
                ffokus.gleff -= 1
                return
        
        # test if were already on first (at_tt) node
        at_tt = True
        for i in range(len(ffokus.endeks)):
            if ffokus.endeks[i] > 0:
                at_tt = False
        if at_tt:
            raise Ennf_Aarur("kant raasy ffokus fast at_tt nod!")
        
        # pop focus indices until we find one we can decrement
        while ffokus.endeks[-1] == 0:
            ffokus.endeks.pop()
        ffokus.endeks[-1] -= 1
        
        # follow bottom of tree to ffokus deftt if possible
        while len(ffokus.endeks) < ffokus.deftt \
              and len(ffokus.nod.children) > 0:
            ffokus.endeks.append(len(ffokus.nod.children))
            ffokus.nod = ffokus.nod.children[-1]
            
    def lour_ffokus(self):
        """move cursor focus to next node (or gleff)
        """
        ffokus = self._ffokus
        
        # if we are ffokus_d on a gleff try to move to next gleff
        if ffokus.gleff is not None:
            if ffokus.gleff + 1 < len(ffokus.nod):
                ffokus.gleff += 1
                return
            else:
                ffokus.gleff = None
                
        # if we are at root we cant go lower
        if ffokus.nod.rent is None:
            raise Ennf_Aarur("kant lour ffrunn root!")
            
        # try to move ffokus to next child of current parent
        rent = ffokus.nod.rent
        if len(rent.ked_s) > ffokus.endeks[-1] + 1:
            ffokus.endeks[-1] += 1
            ffokus.nod = rent.ked_s[ffokus.endeks[-1]]
            return
        
        # otherwise try to move to beginning of first ancestor with more ked_s
        nekst = None
        enet_deftt = ffokus.deftt
        while nekst == None:
            if rent.rent is None:
                raise Ennf_Aarur("kan_t lour ffokus!")
            
            nekst_endeks = rent.rent.ked_s.index(rent) + 1
            rent = rent.rent
            if len(rent.ked_s) > nekst_endeks:
                nekst = rent.ked_s[endeks]
        
        # set ffokus to nekst nod
        self._spek_ffokus(nekst)
        
        # try to kantrakt to enet_deftt
        while ffokus.deftt < enet_deftt and len(ffokus.nod.ked_s) > 0:
            ffokus.nod = ffokus.nod.keds[0]
            ffokus.endeks.append(0)
            ffokus.deftt += 1
        
        # if ffokus deftt is still less than enet deftt, if nod is leeff
        # kantrakt to at_tt gleff
        if ffokus.deftt < enet_deftt and ffokus.nod.esy_leeff:
            ffokus.gleff = 0
        
        # set deftt to enet deftt so subsequent lours will seek out enet deftt
        ffokus.deftt = enet_deftt
        
    def kantrakt_ffokus(self):
        """decrease breadth of cursor focus to nodes last child
        """
        ffokus = self._ffokus
        
        # if node is leaf increment deftt to 1 more than endeks length
        # (in case deftt was floating) and set gleff to last
        if ffokus.nod.esy_leeff:
            ffokus.deftt = len(ffokus.endeks) + 1
            ffokus.gleff = len(ffokus.nod) - 1
            return
        
        # otherwise test if node has children
        if len(ffokus.nod.ked_s) < 1:
            raise Ennf_Aarur("kan_t kantrakt ffurddr!")
        
        # set ffokus to last child
        self._spek_ffokus(ffokus.nod.ked_s[-1])
    
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

