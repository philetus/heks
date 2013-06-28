class Gleff_s:
    """heks gleff input
    """
    
    # enum of gleff values
    a, k, y, l = 0x0, 0x1, 0x2, 0x3
    e, t, s, r = 0x4, 0x5, 0x6, 0x7
    u, d, h, f = 0x8, 0x9, 0xa, 0xb
    o, b, n, g = 0xc, 0xd, 0xe, 0xf
    heks = 0x10
    trgr = 0x11
    
    # gless equivalents
    gless = [
        'a', 'k', 'y', 'l',
        'e', 't', 's', 'r',
        'u', 'd', 'h', 'f',
        'o', 'b', 'n', 'g',
        '*', '!']
    
    # gleffs are ints from 0-15
    rabek = [i for i in range(16)]
    
