from __future__ import print_function

import os
import sys
import re

MODE = 0

if sys.platform == 'win32':
    import ctypes
    kernel32 = ctypes.WinDLL('kernel32')
    hStdOut = kernel32.GetStdHandle(-11)
    mode = ctypes.c_ulong()
    MODE = mode
    if not mode.value == 7:
        kernel32.GetConsoleMode(hStdOut, ctypes.byref(mode))
        mode.value |= 4
        kernel32.SetConsoleMode(hStdOut, mode)

class Win10Colors(object):
    """docstring for Win10Colors"""
    def __init__(self):
        super(Win10Colors, self).__init__()

    @classmethod
    def supports_color(cls):
        plat = sys.platform
        supported_platform = plat != 'Pocket PC' and (plat != 'win32' or 'ANSICON' in os.environ)

        # isatty is not always implemented, #6223.  
        is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
        
        global MODE
        if plat == 'win32' and int(MODE.value) == 7:
            supported_platform = True
        return supported_platform and is_a_tty
    
    def colored(self, string, foreground, background, attrs=[]):
        '''win10color

        print out coloring for windows >= 10

        Keyword Arguments:
            foreground {str} -- string fore color (default: {''})
            background {str} -- background color  (default: {''})
            attrs {list} -- attribute support: reset, bold, underline, inverse
        '''
        # attrs_bank = {}
        # reset = ''
        # bold = ''
        # underline = ''
        # inverse = ''
        # if attrs:
        #     for i in attrs:
        #         if i == 'reset':
        #             reset = '0m'
        #         elif i == 'bold':
        #             bold = '1m'
        #         elif i == 'underline':
        #             underline = '4m'
        #         elif i == 'inverse':
        #             inverse = '7m'
        #print("foreground =", foreground)
        #print("background =", background)
        fore_color_bank = {
            'black': '30m',
                'red': '31m',
                'green': '32m',
                'yellow': '33m',
                'blue': '34m',
                'magenta': '35m',
                'cyan': '36m',
                'white': '37m',

                'lightblack': '90m',
                'lightgrey': '90m',
                'lightred': '91m',
                'lightgreen': '92m',
                'lightyellow': '93m',
                'lightblue': '94m',
                'lightmagenta': '95m',
                'lightcyan': '96m',
                'lightwhite': '97m',

        }

        back_color_bank = {
            'black': '40m',
                'red': '41m',
                'green': '42m',
                'yellow': '43m',
                'blue': '44m',
                'magenta': '45m',
                'cyan': '46m',
                'white': '47m',

                'on_black': '40m',
                'on_red': '41m',
                'on_green': '42m',
                'on_yellow': '43m',
                'on_blue': '44m',
                'on_magenta': '45m',
                'on_cyan': '46m',
                'on_white': '47m',

                'lightblack': '100m',
                'lightgrey': '100m',
                'lightred': '101m',
                'lightgreen': '102m',
                'lightyellow': '103m',
                'lightblue': '104m',
                'lightmagenta': '105m',
                'lightcyan': '106m',
                'lightwhite': '107m',

                'on_lightblack': '100m',
                'on_lightgrey': '100m',
                'on_lightred': '101m',
                'on_lightgreen': '102m',
                'on_lightyellow': '103m',
                'on_lightblue': '104m',
                'on_lightmagenta': '105m',
                'on_lightcyan': '106m',
                'on_lightwhite': '107m',

        }

        background = back_color_bank.get(background)
        foreground = fore_color_bank.get(foreground)
        if not background:
            background = '40m'
        if not foreground:
            foreground = '37m'

        return "[%s;%s%s[0m" % (background[:-1], foreground, string)
        # return "\033[%s;%s%s\033[0m" % (background[:-1], foreground, string)

def getSort(data=None, foreground='', background=''):
    if data:
        if "-" in data or "_" in data:
            foreground, background = re.split("-|_", data)
        # 'black': '40m',
        #         'red': '41m',
        #         'green': '42m',
        #         'yellow': '43m',
        #         'blue': '44m',
        #         'magenta': '45m',
        #         'cyan': '46m',
        #         'white': '47m',
    if foreground or background:
        if foreground == 'b':
            foreground = 'black'
        elif foreground == 'bl':
            foreground = 'blue'
        elif foreground == 'r':
            foreground = 'red'
        elif foreground == 'g':
            foreground = 'green'
        elif foreground == 'y':
            foreground = 'yellow'
        elif foreground == 'm':
            foreground = 'magenta'
        elif foreground == 'c':
            foreground = 'cyan'
        elif foreground == 'w':
            foreground = 'white'
        elif foreground == 'lb':
            foreground = 'lightblue'
        elif foreground == 'lr':
            foreground = 'lightred'
        elif foreground == 'lg':
            foreground = 'lightgreen'
        elif foreground == 'ly':
            foreground = 'lightyellow'
        elif foreground == 'lm':
            foreground = 'lightmagenta'
        elif foreground == 'lc':
            foreground = 'lightcyan'
        elif foreground == 'lw':
            foreground = 'lightwhite'
        else:
            foreground = 'lightwhite'

        if background == 'b':
            background = 'black'
        elif background == 'bl':
            background = 'blue'
        elif background == 'r':
            background = 'red'
        elif background == 'g':
            background = 'green'
        elif background == 'y':
            background = 'yellow'
        elif background == 'm':
            background = 'magenta'
        elif background == 'c':
            background = 'cyan'
        elif background == 'w':
            background = 'white'
        elif background == 'lb':
            background = 'lightblue'
        elif background == 'lr':
            background = 'lightred'
        elif background == 'lg':
            background = 'lightgreen'
        elif background == 'ly':
            background = 'lightyellow'
        elif background == 'lm':
            background = 'lightmagenta'
        elif background == 'lc':
            background = 'lightcyan'
        elif background == 'lw':
            background = 'lightwhite'
        else:
            background = 'black'
    
    return foreground, background

def make_colors(string, foreground = 'white', background=None, attrs=[]):
    # if not Win10Colors.supports_color() or os.getenv('MAKE_COLORS') == '0':
    #     return string
    if "-" in foreground or "_" in foreground:
        foreground, background = getSort(foreground)
    elif foreground and len(foreground) < 3:
        if background and not len(background) < 3:
            foreground, background_temp = getSort(foreground=foreground, background=background)
        else:
            foreground, background = getSort(foreground=foreground, background=background)
    
    win10color = Win10Colors()
    
    if not win10color.supports_color() or os.getenv('MAKE_COLORS') == '0':
        return string
    elif os.getenv('MAKE_COLORS') == '1':
        return win10color.colored(string, foreground, background, attrs)
    else:
        return win10color.colored(string, foreground, background, attrs)

if __name__ == '__main__':
    print(Win10Colors.supports_color())
    print(make_colors("This is Red", 'lw', 'lr'))
