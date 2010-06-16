class Heks(object):
    """a symbol in the heks language
       
       * species are listed in GLYPHS comments
       * null ('***'ed) species should have no glyphs
       * other species should have from 1 to 16 glyphs
       * number glyphs can also be created from an unsigned long integer
    """
    __slots__ = ['species', 'glyphstring'] # suppress instance __dict__{}
    
    GLYPHS = ['a', # : 0x0 *** boolean false
              'k', # : 0x1
              'y', # : 0x2
              'l', # : 0x3
              
              'e', # : 0x4 negative number
              't', # : 0x5
              's', # : 0x6 word
              'w', # : 0x7 positive number
              
              'u', # : 0x8
              'b', # : 0x9
              'n', # : 0xa code word (similar to an abbreviation)
              'h', # : 0xb
              
              'o', # : 0xc *** null
              'd', # : 0xd
              'f', # : 0xe
              'm'] # : 0xf *** boolean true
              
    TO_HEX = {'a':'0', 'k':'1', 'y':'2', 'l':'3',
              'e':'4', 't':'5', 's':'6', 'w':'7',
              'u':'8', 'b':'9', 'n':'a', 'h':'b',
              'o':'c', 'd':'d', 'f':'e', 'm':'f'}
    
    SPECIES = set('aeswnom')
    NULL_SPECIES = set('aom')
    NUMBER_SPECIES = set('ew')
    
    def __init__(self, species, seed=None):
        # vet species
        if species not in self.SPECIES:
            raise ValueError("unknown heks species: '" + str(species) +"'!")
        self.species = species        
        
        # set blank glyphstring
        self.glyphstring = ''
        
        # if this is a null species just return
        if species in self.NULL_SPECIES:
            return
            
        # if glyphstring is given return after setting
        if type(seed) is str:
            if len(seed) < 1:
                raise ValueError("no glyph in empty seed string!")    
            if len(seed) > 16:
                raise ValueError("heks symbols limited to 16 glyphs!")

            for glyph in seed:
                if glyph not in self.GLYPHS:
                    raise ValueError("unknown glyph: '" + glyph + "'!")
                self.glyphstring += glyph
            return
            
        # if uint given translate to glyphs
        if type(seed) is int:
            if species not in self.NUMBER_SPECIES:
                raise ValueError("only number heks species take uint seed")
            if seed < 0:
                raise ValueError("uint argument has negative sign!")
            if seed >= 2**64:
                raise ValueError("unit argument longer than 8 bytes!")
            if seed == 0:
                self.glyphstring.append(self.GLYPHS[0])
                return
            
            while seed > 0:
                self.glyphstring = self.GLYPHS[seed & 0xf] + self.glyphstring
                seed = seed >> 4
            return
        
        # if no glyphstring or uint given for non-null species raise error
        raise ValueError("heks species " + species + " needs a seed value!")

    def __len__(self):
        """number of glyphs in heks symbol
        """
        return len(self.glyphs)
    
##    def __repr__(self):
##        if self.species in self.NULL_SPECIES:
##            return "Heks('%s')" % self.species
##            
##        return "Heks('%s', '%s')" % (self.species, self.glyphstring)
        
    def __repr__(self):
        if self.species == 'a':
            return "h<false>"
        elif self.species == 'm':
            return "h<true>"
        elif self.species == 'o':
            return "h<null>"
        elif self.species == 'e':
            return "h<neg|%s>" % self.glyphstring
        elif self.species == 'w':
            return "h<pos|%s>" % self.glyphstring
        elif self.species == 's':
            return "h<word|%s>" % self.glyphstring
        elif self.species == 'n':
            return "h<code|%s>" % self.glyphstring
    
    def to_hex(self):
        if self.species not in self.NUMBER_SPECIES:
            raise ValueError("only numeric species can be output as hex!")
            
        string = "0x" + ''.join(self.TO_HEX[g] for g in self.glyphstring)
        if self.species == 'e':
            string = "-" + string
        return string
        

