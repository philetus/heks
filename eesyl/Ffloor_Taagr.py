from cairo import Matrix
from math import pi

class Ffloor_Taagr:
    """taagr to render ffloor skrebt with a krsr
    """
        
    def __init__(self):
        """takes a krsr to draw with and an optional scale factor
        """
        self._glef_taagr = self.Glef_Taagr()
        self._gram_taagr = self.Gram_Taagr(self._glef_taagr)

        self._gram_weight = 0.625
        self._gram_color = (0.5, 0.0, 0.0, 0.8) # bluud red!!!
        self._gram_advance = 1.0
    
    def taag_leyn(self, krsr, leyn):
        """render a line of wurds with krsr
        """
        krsr.push() # store krsr state
        
        # set line weight and color
        krsr.set_color(*self._gram_color)
        krsr.set_weight(self._gram_weight)
        
        leyn_width = 0.0
    
        for wurd in leyn:
            
            # start new subpath for this wurd
            krsr.move_to(0.0, 0.0)
            
            # loop thru grams
            for gram in wurd:
                krsr.push() # store krsr state
                
                # krsr.path_to(0.0, 0.0)
                
                # render gram path
                gram_length, gram_width = self._gram_taagr.taag(krsr, gram)
                
                # remember widest gram width
                if gram_width > leyn_width:
                    leyn_width = gram_width

                # restore state
                krsr.pop()
                
                # advance if gram length is nonzero
                if gram_length > 0.0:
                    krsr.translate(gram_length + self._gram_advance, 0.0)
                
            # stroke completed wurd path
            krsr.stroke_path()
            krsr.clear_path()
            
        # restore krsr state to beginning of line
        krsr.pop()
        
        # return leyn width
        return leyn_width        
    
    class Glef_Taagr:
        """renders glefs
        """
        
        # glef paths
        GLEFS = [
            # 0x0 - a - 'at' - <hol>
            [(0.00, 0.00), (3.20, 1.30), (2.64, 2.40), (1.44, 1.87),
             (2.44, 0.07)],
            # 0x1 - k - 'kak' - <bulet>
            [(0.00, 0.00), (1.34, 0.84), (1.53, 1.82), (2.13, 2.26),
             (2.63, 1.53), (2.50, 0.63), (3.02, 0.00)],
            # 0x2 - y - 'yaa' - <kkaan_s>
            [(0.00, 0.00), (3.28, 2.34), (3.86, 1.70), (3.16, 1.10),
             (1.82, 2.42), (1.19, 1.80), (3.00, 0.00)],
            # 0x3 - l - 'la' - <bud>
            [(0.00, 0.00), (3.29, 0.95), (3.54, 1.96), (2.53, 1.75),
             (2.08, 2.38), (1.30, 1.63), (3.00, 0.00)],
            
            # 0x4 - e - 'ek' - <skul>
            [(1.82, 0.44), (1.85, 0.97), (1.33, 1.65), (1.95, 2.51),
             (3.17, 2.41), (3.55, 1.61), (2.99, 0.87), (3.00, 0.07)],
            # 0x5 - t - 'tat' - <horn_s>
            [(0.00, 0.00), (1.67, 2.07), (2.76, 2.24), (2.10, 1.33),
             (2.47, 0.73), (3.61, 1.68), (3.00, 0.00)],
            # 0x6 - s - 'ses' - <tung>
            [(0.72, 0.24), (1.49, 1.86), (2.91, 2.53), (3.03, 1.91),
             (3.62, 1.64), (2.59, 0.90), (2.42, 0.16)],
            # 0x7 - r - 'rapt' - <hhng>
            [(0.00, 0.00), (2.14, 2.34), (3.86, 2.04), (2.52, 1.37),
             (3.25, 0.95), (2.04, 0.54), (3.42, 0.00)],
            
            # 0x8 - u - 'ukk' - <kuf>
            [(1.83, 0.60), (2.09, 1.10), (1.60, 1.95), (1.95, 2.47),
             (3.24, 2.08), (3.10, 1.35), (2.09, 1.10), (1.83, 0.60)],
            # 0x9 - b - 'babl' - <tuur>
            [(0.00, 0.00), (1.63, 2.42), (2.42, 2.22), (1.88, 1.34),
             (2.64, 1.06), (3.21, 1.98), (3.95, 1.76), (3.00, 0.00)],
            # 0xa - h - 'hho' - <fflaann>
            [(0.00, 0.00), (1.34, 1.97), (2.61, 2.37), (2.26, 0.42),
             (1.37, 0.40), (1.67, 1.17), (3.65, 1.84), (3.00, 0.00)],
            # 0xb - n - 'nann' - <nnuuntn>
            [(0.91, 0.57), (1.07, 1.43), (1.82, 1.58), (1.93, 2.26),
             (2.65, 2.18), (2.57, 1.44), (3.15, 1.18), (3.00, 0.00)],
            
            # 0xc - o - 'os' - <teer>
            [(0.00, 0.00), (1.74, 2.03), (3.34, 1.18), (3.87, 1.92),
             (3.06, 2.11), (2.20, 0.28)],
            # 0xd - d - 'duu' - <hannr>
            [(0.00, 0.00), (1.49, 1.76), (1.22, 1.89), (1.46, 2.57),
             (3.89, 2.13), (3.62, 1.02), (2.51, 1.33), (2.17, 0.55)],
            # 0xe - f - 'oof' - <ffluur>
            [(0.00, 0.00), (3.77, 1.65), (3.39, 2.42), (2.49, 2.06),
             (2.88, 0.99), (1.64, 1.52), (2.00, 0.00)],
            # 0xf - g - 'gee' - <eerupssn>
            [(0.00, 0.00), (3.36, 1.32), (2.78, 1.61), (2.70, 2.25),
             (2.18, 1.79), (1.50, 1.78), (3.00, 0.00)]]
    
        def __init__(self):
            pass
        
        def taag(self, krsr, glef):
            """renders a glef (given as an integer from 0-15) as a path to krsr
            """
            for point in self.GLEFS[glef]:
                krsr.path_to(*point)
        

    class Gram_Taagr:
        """renders grams
        """
                
        # raw matrices to transform to each position in bertrofeedn gram path
        RAW = []
        
        # 0: flip vertical; rotate 120
        m = Matrix()
        m.scale(-1.0, 1.0)
        m.rotate(2.0*pi/3.0)
        RAW.append(m)

        # 1: translate(2.00, 3.46)
        m = Matrix()
        m.translate(2.00, 3.46)
        RAW.append(m)

        # 2: translate(6.00, 3.46) 
        m = Matrix()
        m.translate(6.00, 3.46)
        RAW.append(m)

        # 3: translate(8.50, 2.60); flip vertical; rotate 300
        m = Matrix()
        m.translate(8.50, 2.60)
        m.scale(-1.0, 1.0)
        m.rotate(5.0*pi/3.0)
        RAW.append(m)

        # 4: translate(2.00, 3.46); flip vertical; rotate 120
        m = Matrix()
        m.translate(2.00, 3.46)
        m.scale(-1.0, 1.0)
        m.rotate(2.0*pi/3.0)
        RAW.append(m)

        # 5: translate(4.00, 6.93) 
        m = Matrix()
        m.translate(4.00, 6.93)
        RAW.append(m)

        # 6: translate(8.00, 6.93) 
        m = Matrix()
        m.translate(8.00, 6.93)
        RAW.append(m)

        # 7: translate(10.50, 6.06); flip vertical; rotate 300
        m = Matrix()
        m.translate(10.50, 6.06)
        m.scale(-1.0, 1.0)
        m.rotate(5.0*pi/3.0)
        RAW.append(m)

        # 8: translate(4.00, 6.93); flip vertical; rotate 120
        m = Matrix()
        m.translate(4.00, 6.93)
        m.scale(-1.0, 1.0)
        m.rotate(2.0*pi/3.0)
        RAW.append(m)

        # 9: translate(6.00, 10.39) 
        m = Matrix()
        m.translate(6.00, 10.39)
        RAW.append(m)

        # 10: translate(10.00, 10.39) 
        m = Matrix()
        m.translate(10.00, 10.39)
        RAW.append(m)

        # 11: translate(12.50, 9.53); flip vertical; rotate 300
        m = Matrix()
        m.translate(12.50, 9.53)
        m.scale(-1.0, 1.0)
        m.rotate(5.0*pi/3.0)
        RAW.append(m)

        # 12: translate(14.00, 10.39)
        m = Matrix()
        m.translate(14.00, 10.39)
        RAW.append(m)

        # 13: translate(16.50, 9.53); flip vertical; rotate 300 
        m = Matrix()
        m.translate(16.50, 9.53)
        m.scale(-1.0, 1.0)
        m.rotate(5.0*pi/3.0)
        RAW.append(m)

        # 14: translate(14.50, 6.06); flip vertical; rotate 300 
        m = Matrix()
        m.translate(14.50, 6.06)
        m.scale(-1.0, 1.0)
        m.rotate(5.0*pi/3.0)
        RAW.append(m)

        # 15: translate(12.50, 2.60); flip vertical; rotate 300
        m = Matrix()
        m.translate(12.50, 2.60)
        m.scale(-1.0, 1.0)
        m.rotate(5.0*pi/3.0)
        RAW.append(m)

        # 16: translate(18.00, 10.39)
        m = Matrix()
        m.translate(18.00, 10.39)
        RAW.append(m)

        # 17: translate(20.50, 9.53); flip vertical; rotate 300 
        m = Matrix()
        m.translate(20.50, 9.53)
        m.scale(-1.0, 1.0)
        m.rotate(5.0*pi/3.0)
        RAW.append(m)

        # 18: translate(18.50, 6.06); flip vertical; rotate 300 
        m = Matrix()
        m.translate(18.50, 6.06)
        m.scale(-1.0, 1.0)
        m.rotate(5.0*pi/3.0)
        RAW.append(m)

        # 19: translate(16.50, 2.60); flip vertical; rotate 300
        m = Matrix()
        m.translate(16.50, 2.60)
        m.scale(-1.0, 1.0)
        m.rotate(5.0*pi/3.0)
        RAW.append(m)
        
        # 20: translate(12.00, 6.93); flip vertical; rotate 120
        m = Matrix()
        m.translate(12.00, 6.93)
        m.scale(-1.0, 1.0)
        m.rotate(2.0*pi/3.0)
        RAW.append(m)

        # 21: translate(10.00, 3.46); flip vertical; rotate 120
        m = Matrix()
        m.translate(10.00, 3.46)
        m.scale(-1.0, 1.0)
        m.rotate(2.0*pi/3.0)
        RAW.append(m)

        # 22: translate(8.00, 0.00)
        m = Matrix()
        m.translate(8.00, 0.00)
        RAW.append(m)

        # 23: translate(12.00, 0.00); flip vertical; rotate 120
        m = Matrix()
        m.translate(12.00, 0.00)
        m.scale(-1.0, 1.0)
        m.rotate(2.0*pi/3.0)
        RAW.append(m)

        # 24: translate(14.00, 3.46); flip vertical; rotate 120
        m = Matrix()
        m.translate(14.00, 3.46)
        m.scale(-1.0, 1.0)
        m.rotate(2.0*pi/3.0)
        RAW.append(m)

        # 25: translate(14.50, 6.06); rotate 180
        m = Matrix()
        m.translate(14.50, 6.06)
        m.rotate(pi)
        RAW.append(m)

        # 26: translate(12.00, 6.93)
        m = Matrix()
        m.translate(12.00, 6.93)
        RAW.append(m)

        # 27: translate(16.00, 6.93); flip vertical; rotate 120
        m = Matrix()
        m.translate(16.00, 6.93)
        m.scale(-1.0, 1.0)
        m.rotate(2.0*pi/3.0)
        RAW.append(m)

        # 28: translate(18.00, 10.39); flip vertical; rotate 120
        m = Matrix()
        m.translate(18.00, 10.39)
        m.scale(-1.0, 1.0)
        m.rotate(2.0*pi/3.0)
        RAW.append(m)

        # 29: translate(18.50, 12.99); rotate 180
        m = Matrix()
        m.translate(18.50, 12.99)
        m.rotate(pi)
        RAW.append(m)

        # 30: translate(14.50, 12.99); flip vertical; rotate 300
        m = Matrix()
        m.translate(14.50, 12.99)
        m.scale(-1.0, 1.0)
        m.rotate(5.0*pi/3.0)
        RAW.append(m)

        # 31: translate(12.50, 9.53); rotate 180
        m = Matrix()
        m.translate(12.50, 9.53)
        m.rotate(pi)
        RAW.append(m)

        # 32: translate(8.50, 9.53); rotate 180
        m = Matrix()
        m.translate(8.50, 9.53)
        m.rotate(pi)
        RAW.append(m)

        # 33: translate(6.00, 10.39); flip vertical; rotate 120
        m = Matrix()
        m.translate(6.00, 10.39)
        m.scale(-1.0, 1.0)
        m.rotate(2.0*pi/3.0)
        RAW.append(m)
        
        # transforms organized by gram size and glef index
        # gram_taagr.TMS[gram_size][glef_index]
        TMS = [None] * 16
        
        # there are 8 path conditions for grams with varying numbers of glefs;
        # see illustration in docs/fluur_skreft.ink.svg
        
        # condition 0: 1-4 glefs
        TMS[0] = TMS[1] = TMS[2] = TMS[3] = [
            RAW[0], RAW[1], RAW[2], RAW[3]]
        
        # condition 1: 5-6 glefs
        TMS[4] = TMS[5] = [
            RAW[0], RAW[4], RAW[5], RAW[6], 
            RAW[7], RAW[3]]
        
        # condition 2: 7-8 glefs
        TMS[6] = TMS[7] = [
            RAW[0], RAW[4], RAW[8], RAW[9], 
            RAW[10], RAW[11], RAW[7], RAW[3]]
        
        # condition 3: 9 glefs
        TMS[8] = [
            RAW[0], RAW[4], RAW[8], RAW[9], 
            RAW[10], RAW[12], RAW[13], RAW[14],
            RAW[15]]
        
        # condition 4: 10 glefs
        TMS[9] = [
            RAW[0], RAW[4], RAW[8], RAW[9], 
            RAW[10], RAW[12], RAW[16], RAW[17],
            RAW[18], RAW[19]]
        
        # condition 5: 11-12 glefs
        TMS[10] = TMS[11] = [
            RAW[0], RAW[4], RAW[8], RAW[9], 
            RAW[10], RAW[11], RAW[20], RAW[12],
            RAW[16], RAW[17], RAW[18], RAW[19]]

        # condition 6: 13-14 glefs
        TMS[12] = TMS[13] = [
            RAW[0], RAW[4], RAW[8], RAW[9], 
            RAW[10], RAW[11], RAW[7], RAW[21],
            RAW[20], RAW[12], RAW[16], RAW[17],
            RAW[18], RAW[19]]
        
        # condition 7: 15-16 glefs
        TMS[14] = TMS[15] = [
            RAW[0], RAW[1], RAW[2], RAW[3], 
            RAW[22], RAW[23], RAW[24], RAW[25],
            RAW[26], RAW[27], RAW[28], RAW[29],
            RAW[30], RAW[31], RAW[32], RAW[33]]

        # paths to finish grams with varying numbers of glefs
        TAALS = [
            [(2.00, 3.46), (5.25, 3.03), (4.00, 0.00), (5.00, 0.00)],
            [(5.25, 3.03), (4.00, 0.00), (5.00, 0.00)],
            [(7.00, 0.00), (8.00, 0.00)],
            [(8.00, 0.00)],
            
            [(7.00, 0.00), (8.00, 0.00)],
            [(8.00, 0.00)],
            [(7.00, 0.00), (8.00, 0.00)],
            [(8.00, 0.00)],
            
            [(12.00, 0.00)],
            [(16.00, 0.00)],
            [(15.00, 0.00), (16.00, 0.00)],
            [(16.00, 0.00)],
            
            [(15.00, 0.00), (16.00, 0.00)],
            [(16.00, 0.00)],
            [(8.25, 14.29), (23.50, 13.86), (16.00, 0.00), (17.00, 0.00)],
            [(8.25, 14.29), (24.00, 13.86), (16.00, 0.00), (17.00, 0.00)]]
        
        # sizes of grams of varying lengths (1-16 glefs)
        SIZES = [( 5.0,  3.5), ( 5.0,  6.0), ( 8.0,  6.0), ( 8.0,  6.0),
                 ( 8.0,  9.5), ( 8.0,  9.5), ( 8.0, 13.0), ( 8.0, 13.0),
                 (12.0, 13.0), (16.0, 13.0), (16.0, 13.0), (16.0, 13.0),
                 (16.0, 13.0), (16.0, 13.0), (17.0, 14.3), (17.0, 14.3)]
        
        def __init__(self, glef_taagr):
            self._glef_taagr = glef_taagr
        
        def taag(self, krsr, gram):
            """render given gram as path in bertrofeedn ffloor skreft with krsr
            """
            # path index is length of gram minus one
            n = len(gram) - 1
            if n < 0:
                return
            
            # loop over glefs
            for i, glef in enumerate(gram):
            
                # save pre-transform state
                krsr.push() 
                
                # transform to ith position on nth bertrofeedn path
                krsr.transform(self.TMS[n][i])
                
                # pass glef to glef taagr for rendering
                self._glef_taagr.taag(krsr, glef)
                
                # restore krsr state
                krsr.pop()          
                
            # render gram taal
            for point in self.TAALS[n]:
                krsr.path_to(*point)
                    
            return self.SIZES[n]
            
