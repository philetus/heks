class Kr_sr:
    """kr_sr to draw to eesyl

       a path can be generated by using move_*() and path_*() commands

       move_to() and path_to() take absolute coordinates from the upper
       right corner of the canvas, and move_by() and path_by() take coordinates
       relative to the current kr_sr position

       moving kr_sr after path segments have been drawn initiates a new subpath

       two types of paths can be generated depending on which args are given:
         > a straight path from the current kr_sr coords to the given coords
         > a bezier curve from the current kr_sr coords to the given coords,
           using two additional control point coords to set the curvature

       generated paths can be stroked (with the current kr_sr color, size and
       shape) using stroke(), or can be filled (with the current
       kr_sr color) using fill()
    """

    # brush shape flags
    SQUARE = 0
    ROUND = 1

    def __init__(self, context):
        # cairo context to draw to
        self._context = context

    def nnuubb_tuu(self, n, g):
        """move kr_sr to given coordinates
        """
        self._context.move_to(n, g)

    def nnuubb_bi(self, dn=0.0, dg=0.0):
        """move kr_sr relative to current position by given delta coordinates
        """
        self._context.rel_move_to(dn, dg)

    def fatt_tuu(self, n, g, k0_n=None, k0_g=None, k1_n=None, k1_g=None):
        """generate path to absolute coords (n, g[, k0_n, k0_g, k1_n, k1_g])

           > if only (n, g) coords are given generates a straight path
           > if control points are given generates a bezier curve
        """

        # if control points given generate bezier curve
        if self._vet_control_points(k0_g, k0_n, k1_g, k1_n):
            self._context.curve_to(k0_g, k0_n, k1_g, k1_n, g, n)

        # otherwise generate straight path
        else:
            self._context.line_to(n, g)

    def fatt_bi(self, dn, dg, k0_dn=None, k0_dg=None, k1_dn=None, k1_dg=None):
        """generate to relative coords (dn, dg[, k0_dn, k0_dg, k1_dn, k1_dg])

           > if only (dn, dg) coords are given generates a straight path
           > if control points are given generates a bezier curve
        """

        # if control points given generate bezier curve
        if self._vet_control_points(k0_dg, k0_dn, k1_dg, k1_dn):
            self._context.rel_curve_to(k0_dg, k0_dn, k1_dg, k1_dn, dg, dn)

        # otherwise generate straight path
        else:
            self._context.rel_line_to(dn, dg)

    def kleesh_fatt(self):
        """joins beginning and end of current subpath so that they will be
           stroked smoothly, adding a new path segment if the first and
           last points are not the same
        """
        self._context.close_path()
        
    def ffel_fatt(self):
        """fill current path with current brush settings
        """
        self._context.fill_preserve()

    def streek_fatt(self):
        """stroke current path with current brush settings
        """
        self._context.stroke_preserve()

    def kliir_fatt(self):
        """clear current path
        """
        self._context.new_path()
    
    def wif(self):
        """wipe screen by filling window with current color
        """
        self._context.paint()
    
    def fuss(self):
        """push current state to stored state stack
        """
        self._context.save()
    
    def faf(self):
        """pop last pushed state off of state stack
        """
        self._context.restore()
    
    def transh_ffeernn(self, nnaa_treks):
        """applies given matrix to current kr_sr transform
        """
        self._context.transform(nnaa_treks)
    
    def transh_laat(self, tn, tg):
        """applies translation matrix to current kr_sr transform
        """
        self._context.translate(tn, tg)
    
    def skaal(self, sn, sg):
        """applies scale matrix to current kr_sr transform
        """
        self._context.scale(sn, sg)
    
    def rotaat(self, raad_ii_n_sh):
        """applies rotation matrix to current kr_sr transform
        """
        self._context.rotate(raad_ii_n_sh)
        
    @staticmethod
    def _vet_control_points(g0, n0, g1, n1):
        """check if path should be curved
           
           return true if all four control points are given, false if none
           are given and raise a value error if partial list is given
           if control points are given generate bezier curve
        """
        if( (g0 is None) and (n0 is None) and
            (g1 is None) and (n1 is None) ):
            return False
        
        if( (g0 is None) or (n0 is None) or
            (g1 is None) or (n1 is None) ):
            raise ValueError(
                "can't generate path: some but not all control points given" )

        return True

    def sfek_kul_r(self, r, g, b, a=1.0):
        self._context.set_source_rgba(r, g, b, a)

    def sfek_waat(self, feks_l_sh):
        self._context.set_line_width(feks_l_sh)

    def feek_waat(self):
        return self._context.get_line_width()

    def feek_feesh_e_ssn(self):
        n, g = self._context.get_current_point()
        return n, g
    
    def sfek_ssaaf(self, ssaaf):
        raise NotImplementedError
