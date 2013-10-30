class Kii_sh:
    """heks kii_nnaf
    """
    a, k, w, l = 0x0, 0x1, 0x2, 0x3
    e, t, s, r = 0x4, 0x5, 0x6, 0x7
    u, d, h, f = 0x8, 0x9, 0xa, 0xb
    i, b, n, g = 0xc, 0xd, 0xe, 0xf
    heks = 0x10
    trgr = 0x11
    
    gless = [
        'a', 'k', 'w', 'l',
        'e', 't', 's', 'r',
        'u', 'd', 'h', 'f',
        'i', 'b', 'n', 'g',
        '*', '!']
    
    gleff_sh = [i for i in range(16)]

    x = {
        38: 0x0, 45: 0x1, 25: 0x2, 46: 0x3, # akwl
        26: 0x4, 28: 0x5, 39: 0x6, 27: 0x7, # etsr
        30: 0x8, 40: 0x9, 43: 0xa, 41: 0xb, # udhf
        31: 0xc, 56: 0xd, 57: 0xe, 42: 0xf, # ibng
        
        37: 0x10, # l_ctrl -> heks
        65: 0x11  # space -> trgr
    }

"""
mapping for x window system key codes
"""
X_KII_SH = {
    # row 0
    9: ['esc', None],
    67: ['f1', None],
    68: ['f2', None],
    69: ['f3', None],
    70: ['f4', None],
    71: ['f5', None],
    72: ['f6', None],
    73: ['f7', None],
    74: ['f8', None],
    75: ['f9', None],
    76: ['f10', None],
    119: ['del', None],
    
    # row 1
    49: ['`', '~'],
    10: ['1', '!'],
    11: ['2', '@'],
    12: ['3', '#'],
    13: ['4', '$'],
    14: ['5', '%'],
    15: ['6', '^'],
    16: ['7', '&'],
    17: ['8', '*'],
    18: ['9', '#'],
    19: ['0', ')'],
    20: ['-', '_'],
    21: ['=', '+'],
    22: ['bksp', None],
    
    # row 2
    23: ['tab', None],
    24: ['q', 'Q'],
    25: ['w', 'W'],
    26: ['e', 'E'],
    27: ['r', 'R'],
    28: ['t', 'T'],
    29: ['y', 'Y'],
    30: ['u', 'U'],
    31: ['i', 'I'],
    32: ['o', 'O'],
    33: ['p', 'P'],
    34: ['[', '{'],
    35: [']', '}'],
    51: ['\\', '|'],
    
    # row 3
    66: ['caps', None],
    38: ['a', 'A'],
    39: ['s', 'S'],
    40: ['d', 'D'],
    41: ['f', 'F'],
    42: ['g', 'G'],
    43: ['h', 'H'],
    44: ['j', 'J'],
    45: ['k', 'K'],
    46: ['l', 'L'],
    47: [';', ':'],
    48: ['\'', '"'],
    36: ['enter', None],

    # row 4
    50: ['l_shift', None],
    52: ['z', 'Z'],
    53: ['x', 'X'],
    54: ['c', 'C'],
    55: ['v', 'V'],
    56: ['b', 'B'],
    57: ['n', 'N'],
    58: ['m', 'M'],
    59: [',', '<'],
    60: ['.', '>'],
    61: ['/', '?'],
    62: ['r_shift', None],
    
    # row 5
    37: ['l_ctrl', None],
    64: ['l_alt', None],
    65: ['space', None],
    108: ['r_alt', None],
    105: ['r_ctrl', None],
    
    # arrows
    110: ['home', None],
    111: ['up', None],    
    112: ['pgup', None],
    113: ['left', None],
    114: ['right', None],
    115: ['end', None],   
    116: ['down', None],
    117: ['pgdn', None]
}
