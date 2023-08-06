# -*- coding: utf-8 -*-
"""
Handy Functions and variables/constants for use at iPython prompt
   call mine() for full list of functions and variables.

Created on Sat Feb  1 15:05:51 2020
     ------ Time-stamp: <2020-11-24T18:06:53.308934-05:00 hedfp> ------
     
@author: Carl Schmiedekamp

2020-04-14 /CS/ adding 'mine()' to list what has been setup by handies.py
                adding atan2P(y,x) to return positive angle.
2020-04-17 /CS/ adding astropy.units as 'u'
2020-07-13 /CS/ removing cdpy1d(), and cdWD()
2020-07-22 /CS/ making astropy and func_timeout optional.
2020-07-25 /CS/ added timeStampStr()
                changed from file date/time to timestamp file as mod. time
                for this module, also added the version from __init__.py.
                Added variable "__version__" which holds the version.
2020-07-29 /CS/ added isInstalled()
2020-08-13 /CS/ added condaEnvName() as a helper function.
2020-08-25 /CS/ added 'line magic' cls to fill screen with 23 blank lines.
                the 'Loading' message is not output if not in IPython or the
                interactive interpreter.
2020-09-02 /CS/ Now sets ipython number precision to 5 digits.
                  (Note: only for expression evaluation output.)
2020-09-13 /CS/ made the height parameter to figsize optional, with the default
                  being 0.75 % of width.
2020-09-22 /CS/ added VURound and round_sig functions,
                VURound needs work if uncertainty can have more than 1 sig.fig.
2020-10-16 /CS/ Add is_ipython(), is_interactive(), and is_commandline() to test
                running environment.
2020-10-30 /CS/ adding astropy.constants as c
2020-11-02 /CS/ added clsall() which clears terminal screen of all characters.

"""


## Shortcuts etc. functions.
import math
import codecs
from math import pi, sqrt, cos, sin, tan, floor
from math import acos, asin, atan, atan2, degrees, radians
from math import log, log10, exp

from random import randint
import time

### Current rule of thumb: only handies imports from other modules.
from classroom_gizmos.BestByMinBefore import getCCode
from classroom_gizmos.import_install import importInstall as II


def clsall():
    '''Outputs the ASCII clear screen character.
    This usually deletes all the previoous text in the terminal.'''
    print( '\033[2J', end=None)

def is_ipython():
    '''Return True if running in IPython.
    Ref: https://stackoverflow.com/questions/23883394/detect-if-python-script-is-run-from-an-ipython-shell-or-run-from-the-command-li
    '''
    try:
        __IPYTHON__
    except NameError:
        result = False
    else:
        result = True
    return result

# def is_interactive():
#     '''Return True if running interactive interpreter but not IPython.
#     Ref: https://stackoverflow.com/questions/23883394/detect-if-python-script-is-run-from-an-ipython-shell-or-run-from-the-command-li
#     '''
#     import inspect
    
#     if len( inspect.stack()) > 1 and not is_ipython():
#         result = True
#     else:
#         result = False
#     return result

def is_interactive():
    '''Return true if interactive python, False if running from command line.
    Ref: https://stackoverflow.com/questions/2356399/tell-if-python-is-in-interactive-mode
    '''
    import sys
    try:
        if sys.ps1: inter = True
    except AttributeError:
        inter = False
        if sys.flags.interactive: inter = True
    return inter


def is_commandline():
    '''Returns True if running from command line (not ipython, and not interactive
    interpreter.).
    Ref: https://stackoverflow.com/questions/23883394/detect-if-python-script-is-run-from-an-ipython-shell-or-run-from-the-command-li
    '''
    import inspect
    
    if len( inspect.stack()) == 1 :
        result = True
    else:
        result = False
    return result

def round_sig(x, sig=6, small_value=1.0e-9):
    ''' Round numbers to sig figs.
     Ref: https://stackoverflow.com/questions/3410976/how-to-round-a-number-to-significant-figures-in-python
     '''
    return round(x, sig - int(floor(log10(max(abs(x), abs(small_value))))) - 1)


def VURound( value, uncertainty, undig=1):
    '''
    Returns a string with rounded value and uncertainty.
    Round value based on uncertainty.
    Uncertainty is rounded up to "undig" sig.figs.
      'undig' is currently fixed at 1
      Based on Javascript function by Carl Schmiedekamp
    '''
    from math import copysign, log10, floor, ceil
    
    #soecial case: uncertanity is zero: return value as string.
    if uncertainty==0:
        return str( value)
    
    sign = copysign( 1,value)
    
    valin = abs( value)
    uncin = abs( uncertainty)
    
    dec = log10(uncin)
    # print('DBug uncin, dec, uncertainty', uncin, dec, uncertainty)
    dec = floor(dec+1)-1
    
    uncmant=uncin*pow(10.0,-1*dec)
    
    if uncmant > 9: ##Fix if rounding up adds another digit.
        dec = dec + 1
        uncmant=uncin*pow(10.0,-1*dec);
    
    if round( uncmant) != uncmant:  ##round larger if sigmant is not integral
        uncmant=int( uncmant+1);
    
    ## for values between .1 and 9999. use 2 part output (also equal to zero)
    if (valin >= .1 and valin <=9999.) or (valin == 0.0):
        if dec > 0:
            nd = 0
        else:
            nd = -dec
            
        fmtstr = '{'+':22.{}f'.format( nd)+'}'
#        print( 'DBug: fmtstr: {}'.format( fmtstr))
        
        if sign < 0:
#            val3p=str(int(valin*pow(10,-dec)+0.5)*pow(10,dec)*sign)
            val3p=fmtstr.format( int(valin*pow(10,-dec)+0.5)*pow(10,dec)*sign).strip()
        else:
#            val3p=str(int(valin*pow(10,-dec)+0.5)*pow(10,dec))
            val3p=fmtstr.format( int(valin*pow(10,-dec)+0.5)*pow(10,dec)).strip()
            
#        print( 'DBug: valin: {}, dec: {}, val3p: {}, nd: {}'.format( valin, dec, val3p, nd))
        
        unc3p = fmtstr.format( uncmant*pow(10,dec) ).strip()
        
        return ('{} '+u"\u00B1"+ ' {}').format( val3p, unc3p)
        
    else:  ##  otherwise use 4 part output
        
        val=int(valin*pow(10,-dec)+0.5)*pow(10,dec)*sign
        if valin >= uncin:
            exp=ceil(log10(valin))-1
        else:
            exp=ceil(log10(uncin))-1
        
        
        nd = -( dec - exp)
        
        if nd < 0:
            nd = 0
            
        fmtstr = '{'+':22.{}f'.format( nd)+'}'
#        print( 'DBug: fmtstr: {}'.format( fmtstr))

        val = fmtstr.format( val*pow(10,-exp)).strip()

        unc=str(uncmant*pow(10,dec-exp));
        unc = fmtstr.format( uncmant*pow(10,dec-exp)).strip()

#        print( 'DBug: val: {}, unc: {}, exp: {}, nd: {}'.format( val, unc, exp, nd))
        
        return ('({} '+u"\u00B1"+ ' {})' + u"\u00D7" +'10^' + '{}').format( val, unc, exp)



def randomLetter():
    '''
    Generate a single random uppercase ASCII letter

    Returns
    -------
    TYPE
        char.
    '''
    import random
    import string    
    return random.choice(string.ascii_uppercase)

def randomElement( List=(1,2,3,4,5,6,7, 'oops')):
    '''
    return random element of list

    '''
    index = randint(0, len( List)-1)
    return List[ index]


def timeStampStr():
    '''Returns a string with the current time in ISO format.'''
    import datetime
    import time
    
    dt = datetime.datetime.now()
    epoch = dt.timestamp() # Get POSIX timestamp of the specified datetime.
    st_time = time.localtime(epoch) #  Get struct_time for the timestamp. This will be created using the system's locale and it's time zone information.
    tz = datetime.timezone(datetime.timedelta(seconds = st_time.tm_gmtoff)) # Create a timezone object with the computed offset in the struct_time.
    return dt.astimezone(tz).isoformat()

# import math
## math.comb is in Python 3.8 
if hasattr( math, "comb" ):
    from math import comb
    from math import comb as nCr
else:
    def nCr(n,r):
        ''' calculate number of combinations of r from n items.'''
        f = math.factorial
        return f(n) // f(r) // f(n-r)
    comb = nCr    

from platform import python_version
import sys, os.path, time, os


def hostname():
    '''Returns 'fully qualified domain name' '''
    import socket
    return socket.getfqdn()


def getTS( rel_path):
    '''Reads first line of specified file, which is expected to be a time-date
    string.
    This is mostly for internal package use.'''
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as tsf:
        lines = tsf.read()
    linelist = lines.splitlines()
    return linelist[0]


def read(rel_path):
    '''Reads text file.'''
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    '''Reads version from specified file. The file path is relative
    to this file. It looks for line that starts with "__version__"'''
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")



## define cls and set precision if in IPython.
if is_ipython() and is_interactive():
    ### set default float precision
    ### Ref: https://stackoverflow.com/questions/10361206/how-to-run-an-ipython-magic-from-a-script-or-timing-a-python-script
    from IPython import get_ipython
    from IPython.core.magic import register_line_magic
            
    ipython = get_ipython()
    ipython.magic( 'precision %0.5g')
            
    ### define clear screen magic (%cls generates 23 blank lines)
    @register_line_magic 
    def cls(line): 
        '''Defines a 'clear screen' line magic'''
        print( 23*'\n') 
        return

    del cls ## must delete function to make magic visible.
    
    # try:
    #     from IPython.core.magic import register_line_magic
    #     ## Ref: https://stackoverflow.com/questions/2356399/tell-if-python-is-in-interactive-mode
    #     ## Ref: https://ipython.readthedocs.io/en/stable/config/custommagics.html
        
    #     try:
    #         if sys.ps1:
    #             IsInteractive = True
            
    #     except AttributeError:
    #         interpreter = False
    #         if sys.flags.interactive: IsInteractive = True
            
            
    #     if IsInteractive:
    #         ### set default float precision
    #         ### Ref: https://stackoverflow.com/questions/10361206/how-to-run-an-ipython-magic-from-a-script-or-timing-a-python-script
    #         from IPython import get_ipython
    #         ipython = get_ipython()
    #         ipython.magic( 'precision %0.5g')
            
    #         ### define clear screen magic (%cls generates 23 blank lines)
    #         @register_line_magic 
    #         def cls(line): 
    #             '''Defines a 'clear screen' line magic'''
    #             print( 23*'\n') 
    #             return
                
    # except ( ModuleNotFoundError, ImportError):
    #     IsInteractive = False
    # else:
    #     del cls ## must delete function to make magic visible.
    
    

######  'Welcome Message' on loading  ######

def condaEnvName():
    '''Gets environment name from python's path.
    Ref:
        https://stackoverflow.com/questions/36539623/how-do-i-find-the-name-of-the-conda-environment-in-which-my-code-is-running'''

    # return Path(sys.executable).as_posix().split('/')[-3]
    return sys.exec_prefix.split(os.sep)[-1]

def ipythonversion():
    '''gets IPython version or returns None.'''
    try:
        import IPython
        ipv = IPython.version_info
        version = ''
        for n in ipv:
            version += str( n) + '_'
        return version[:-1]  ## remove last '_'
    except:
        return None
 
def in_ipynb():
    '''True if running in Jupyter notebook.
    Ref: https://exceptionshub.com/how-can-i-check-if-code-is-executed-in-the-ipython-notebook.html
    Ref: https://stackoverflow.com/questions/15411967/how-can-i-check-if-code-is-executed-in-the-ipython-notebook.
    Currently not definitive in result; returns True in Spyder IPython console.'''
#    try:
#        cfg = get_ipython().config 
#        pappname = cfg['IPKernelApp']['parent_appname']
#        traitlets = ii( 'traitlets')
#        if (traitlets != None) and ( isinstance( pappname, traitlets.config.loader.LazyConfigValue )):
#            return True
##        if pappname == 'ipython-notebook':
##            return True
#        else:
#            return False
#    except NameError:
#        return False
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter


def isInstalled( pkgname):
    ''' Imports pkgname and returns package if installed.
        pkgname is a string with name of package as used in import stmt.
        If not installed, returns None.
        Should be a duplicate of import_install.is_installed().
        Typical Usage:
            astropy = isInstalled( 'astropy') 
            if astropy == None:
                ... 
            else:
                from astropy import units as u
        '''
    try:
        pkg = __import__( pkgname)
        return pkg
    except Exception:
    	return None
ii = isInstalled ## abbreviation

## check if packages for sound are installed and load once
IPython = ii( 'IPython')
beepy = ii( 'beepy')
 # beepy = None  ## testing
playsoundPkg = ii( 'playsound')
 # playsoundPkg = None; ## testing
simpleaudio = ii( 'simpleaudio')
 # simpleaudio = None ## testing

def beepsound():
    '''Plays a 'beep' sound when called if a sound package is found, or
    tries terminal beep.'''
    ## use beep sounds from various possible packages
    if beepy != None:
        beepy.beep( 1)
    elif playsoundPkg != None and os.path.isfile( 'A-Tone-His_Self-1266414414.wav'):
        playsoundPkg.playsound( 'A-Tone-His_Self-1266414414.mp3')
    elif simpleaudio != None and os.path.isfile( 'mixkit-relaxing-bell-chime-3109.wav'):
        wave_obj = simpleaudio.WaveObject.from_wave_file( 'A-Tone-His_Self-1266414414..wav')
        play_obj = wave_obj.play()
        play_obj.wait_done()
    elif IPython != None:
        try:
            # IPython.display.Audio( 'http://www.soundjay.com/button/beep-07.wav', autoplay=True)
            IPython.display.Audio( 'audio/tone_440.wav', autoplay=True)
            # import numpy
            # sr = 22050 # sample rate
            # T = 2.0    # seconds
            # t = numpy.linspace(0, T, int(T*sr), endpoint=False) # time variable
            # x = 0.5*numpy.sin(2*numpy.pi*440*t)  
            # IPython.display.Audio(x, rate=sr) # load a NumPy array
        except ValueError:
            print( '\a')
    else:
        print( '\a')   ## probably won't work, but last attempt.


    
## Get timestamp for package, updated by setup.py.
timestamp = getTS( 'timestamp.txt') ##
date  = timestamp[0:10]
# print('DBug: date: {} TS:\n{}'.format( date, timestamp))

__version__=get_version("__init__.py")

# if is_interactive() or is_ipython():
if is_interactive():
    print( "Loading Carl's handies.py ver: {} {}; Python:{};\n   environment: {}; IPython: {}; is interactive: {}; is ipython: {}".format( 
            __version__, date, python_version(), condaEnvName(), ipythonversion(), is_interactive(), is_ipython() ) )

def call( cmd):
    import subprocess
    '''Modeled after call function in NANOGrav Sprinng 2020 workshop.
    call() just executes the command in the shell and displays output.
    
    Could have security issues. See subprocess documentation.'''
    subprocess.call( cmd, shell=True)


def mine():

    '''List the functions and variables defined in handies.py'''
    print('\n classroom_gizmos.handies ver: {}, modified {}'.format(
        __version__, date))
    if isInstalled( 'astropy'):
        print('Defining:\n     nowMJD(); mjd2date(), date2mjd(),')
        print('     astropy.units as "u", i.e. u.cm or u.GHz')
        print('     astropy.constants as "c", i.e. c.c or c.au')
    else:
        print( '** astropy not available; MJD functions, u (units) and c (constants) are not available.')
    print('     cdbn(), osname(), hostname(), call(),')
    if isInstalled( 'PyQt5'):
        if isInstalled( 'func_timeout'):
            print('     select_file(), select_file_timeout( timeout={}),'.format( sfTimeOut))
        else:
            print('** func_timeout not available; select_file_timeout() ignores timeout.')
            print('     select_file()')
        
    else:
        print( '** PyQt5 is not available; select_file() and select_file_timeout() are not defined.')
    print('     rad(), deg(), sinD(), cosD(), tanD(), asinD(),\n     acosD(), atanD(), atan2D(), atan2P()')
    print("       'D' and 'P' functions work with degrees.")
    print("       'P' inverse functions return only positive angles.")
    print("     Defines nCr() and comb() or imports from math if available.")
    print('     greeks  ➞ a string with greek alphabet.')
    print('     cls or %cls; ipython \'magic\' writes 23 blank lines to clear an area of the screen')
    print('     clsall() function which removes previous text on screen by outputing ascii code.')
    print('     pltsize( width) ➞ resizes plots in matplotlib, units are inches')
    print('     timeStampStr() ➞ returns a readable timestamp string.')
    print('     isInstalled( pkgNameStr) ➞ returns package or None if not installed.')
    print('     is_ipython() ➞ True if running in ipython.')
    print('     is_interactive() ➞ True if in interactive interpreter but not in ipython.')
    print('     is_commandline() ➞ True if running from commandline;not interactive nor ipython.')
    print('     VURound( value, uncertainty) ➞ Rounds value based on uncertainty.')
    print('     round_sig( value, sigfigs) ➞ Rounds value to specified sig.figs.')
    print('     count_down() ➞ Counts down the specified number of seconds.')
    print('     beepsound() ➞  trys to make sound.')

    print('     randomLetter() ➞ a random uppercase ASCII letter.')
    print('     randomElement( List) ➞ returns random element from list.')
    
    print('  Functions for portable code:')
    print('     osname(), username(), computername(), pythonversion(),')
    print('     condaversion(), ipythonversion(), in_ipynb(), isInstalled() or ii(),  II()' )
    
    print()

    print('From random imports randint( min, max)')
    print('From classroom_gizmos.BestByMinBefore imports getCCode()')
    print('From classroom_gizmos.import_install imports import_install as II')
    
    print('From math imports:\n     pi, sqrt, degrees, radians,\n     cos, sin, tan, atan2, asin, acos, atan, and\n' + 
      '     log, log10, exp')

    print( '\n     mine() ➞ lists what handies.py defines.')

    print( '\nRequires astropy, PyQt5, and func_timeout packages for full functionality.')
    print( 'beepsound() can use these audio packages if available: beepy, playsound, simpleaudio')
    
##Ref: https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-precision
    # prhints = ('Hint:\n' + 
    #       '     "%precision %g" or %.6g for better number formats.')
    # print(prhints)


def cosD( ang):
    '''Return cosine of angle in degrees.'''
    import math as m
    return m.cos( m.radians( ang))

def sinD( ang):
    '''Return sine of angle in degrees.'''
    import math as m
    return m.sin( m.radians( ang))

def tanD( ang):
    '''Return tangent of angle in degrees.'''
    import math as m
    return m.tan( m.radians( ang))

def asinD( val):
    '''Return inverse sine, in degrees, of val.'''
    import math as m
    return  m.degrees( m.asin( val))

def acosD( val):
    '''Return inverse consine, in degrees, of val.'''
    import math as m
    return m.degrees( m.acos( val))


def atanD( val):
    '''Return inverse tangent, in degrees, of val.'''
    import math as m
    return m.degrees( m.atan( val))


def atan2D( y, x):
    '''Return inverse tangent, in degrees, of y/x. (-180 ... 180)'''
    import math as m
    return m.degrees( m.atan2( y, x))

def atan2P( y, x):
    '''Return inverse tangent, in degrees, of y/x. (0 .. 360)'''
    ang = atan2D( y, x)
    if ang <0:
        ang = ang + 360
    return ang

rad = radians  ## alias the conversion functions
deg = degrees

greeks = ' Α Β Γ Δ Ε Ζ Η Θ Ι Κ Λ Μ Ν Ξ Ο Π Ρ Σ Τ Υ Φ Χ Ψ Ω  α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ σ τ υ φ χ ψ ω '

def cdbn( dirname, sub=None):
    '''cd to directory (or subdirectory) who's path is in Env.Var. who's name is passed as
       first argument.  2nd argument specifies a subdirectory relative to
       that named directory.'''
    import os
    """ Does cd to directory named in specified environment
        variable.
        Returns current directory (as string) if no error.
        If Error, outputs error msg. and returns False.
        --
        If sub is specified, tries to cd to that subdirectory
        after the cd to the contents of env. var.
    """
    try:
        dir = os.environ[ dirname]
    except KeyError:
        print( dirname, ': not an env. var.')
        return False
    else:
        if os.access( dir, os.R_OK):
            os.chdir( dir)
            if sub==None:
                return os.getcwd()
            else:
                if os.access( sub, os.R_OK):
                    os.chdir( sub)
                    return os.getcwd()
                else:
                    print( '{}: No access!'.format( 
                            os.path.join(dir,sub), dir))
            return False

        else:
            print('[{}] --> {} : No access!'.format( dirname, dir))
            return False


# def cdpy1d():
#     '''cd to Pythonista dir. in OneDrive'''
#     return cdbn('MYonedrivepsu', 'Pythonista')
#
# def cdWD():
#     '''cd to SinglePulse/WorkingDir.'''
# # #     ##os.chdir( r'C:\Users\hedfp\OneDrive - The Pennsylvania State University\InProgress\ACURA-Radio-Astro-class-stuff\SinglePulse-GiantPulses\WorkingDir')
#     return cdbn('MYonedrivepsu', 'InProgress\ACURA-Radio-Astro-class-stuff\SinglePulse-GiantPulses\WorkingDir' )
#

try:
    import astropy
    from astropy import units as u
    from astropy import constants as c
    
    def nowMJD():
        '''Convert current time to MJD'''
        from astropy.time import Time
        return Time.now().to_value( 'mjd')
    
    def mjd2date( mjd):
        '''Convert MJD to a civil date/time'''
        
        from astropy.time import Time
        time = Time( mjd, format='mjd')
        return time.to_datetime()
    
    def date2mjd_( civildate):
        '''Convert specified time to MJD.
        The string in civildate must be recognized by astropy.time.Time,
        and is assumed to be UCT time.
    
        Value returned is float
        
        Usage:
            date2mjd( '2020-05-16T14:10') returns 58985.59027777777778'''
        
        from astropy.time import Time
        return Time( civildate).to_value( 'mjd', 'long')
        
    def date2mjd( civildate):
        '''Convert specified time to MJD.
        The string in civildate must be recognized by astropy.time.Time,
        and is assumed to be UCT time.
        As a special case, if the date/time is followed by UTC offset
        then that is used to shift the date/time to UTC.
        Example: 2019-09-30 20:54:54-04:00 corresponds to 
        UTC of 2019-10-01 00:54:54
    
        Value returned is float
        
        Usage:
            date2mjd( '2020-05-16T14:10') returns 58985.59027777777778
            or
            date2mjd( '2020-05-16T14:10-04:00') returns 58985.756944444444446
            '''
        
        cd = civildate
        offset = 0
        ## check for special case:
        if cd[-3]==':' and ( cd[-6]=='-' or cd[-6]=='+') :
            offset = (int( cd[-5:-3]) + int( cd[-2:])/60 )/24
            if cd[-6]=='+':
                offset = -offset
            cd = cd[:-6]
        
        from astropy.time import Time
        return Time( cd).to_value( 'mjd', 'long')+offset
except ImportError:
    print( 'mjd functions not defined because astropy is not available.')


def pltsize( w, h=None, dpi=150):
    '''set plot size (matplotlib), size in notebook depends on resolution and
    browser settings. However, doubling the values should double the size.
    dpi is dots-per-inch which also changes plot size in notebooks.
    Default height is .75 times the width.'''
    import matplotlib
    if h==None:
        h = 0.75*w
    matplotlib.rc('figure', figsize=[w,h], dpi=dpi)

def osname():
    '''Returns name of operating system that Python is running on.'''
    try:
        os = __import__( 'os')
        return os.name
    except ImportError:
        return None


def username():
    '''Get current username or return "None".'''
    # import getpass
    try:
        getpass = __import__( 'getpass')
        return( getpass.getuser())
    except ImportError:
        return None

def computername():
    '''Get hostname of current computer or return "None".'''
    try:
        socket = __import__( 'socket')
        return socket.getfqdn()
    except ImportError:
        return None

def pythonversion():
    '''Get version of python or return "None".'''
    try:
        platform = __import__( 'platform')
        return platform.python_version()
    except ImportError:
        return None

def condaversion():
    '''Get version of conda, or return "None".'''
    try:
        conda = __import__( 'conda')
        return conda.__version__
    except ImportError:
        return None  ## to be consistent with the others.

def count_down( t=10):
    '''Count down by seconds. 't' is the number of seconds.
    If beepy is installed, then a sound is made when countdown ends.
    Refs:  
    https://pypi.org/project/beepy/#description
    https://www.codespeedy.com/how-to-create-a-countdown-in-python/
    https://stackoverflow.com/questions/25189554/countdown-clock-0105'''
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d} '.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1
    print('\a\n\nDone!\n\n')
    beepsound()

try:
    import PyQt5  ## used in fdtest module, skip these definitions if Qt5 not available.
    
    ## default timeout (in s) for select_file():
    sfTimeOut = 95

    def select_file( ):
        ''' Uses fdtest.py to browse for file and return its path.
        WARNING: This function will 'hang' until a file is selected.'''
        
        from classroom_gizmos.fdtest import gui_fname        
        return gui_fname()

    def select_file_timeout( timeout=sfTimeOut):
        ''' Uses fdtest.py to browse for file and return its path.
        If the fdtest call takes longer than 'timeout' seconds,
        the attempt is cancelled and None is returned.
        The argument, timeout, sets the number of seconds before time out.
        Note: if func_timeout package is not available, the no timeout
        is used (select_file() is called.)
        '''
        ## trying to do auto-install of func_timeout
        try:
            from func_timeout import func_timeout, FunctionTimedOut
        except ImportError:
            from classroom_gizmos.import_install import ii
            func_timeout = ii( 'func_timeout')
            try:
                from func_timeout import func_timeout, FunctionTimedOut
            except Exception:
                print( 'Timeout is not available.')
                return select_file()
            
        from classroom_gizmos.fdtest import gui_fname
        
        try:
            filename = func_timeout( timeout, gui_fname, args=()).decode("utf-8")
        except FunctionTimedOut:
            outstr = 'select_file cound not complete within '
            outstr += '{} seconds.\n'.format( timeout)
            print( outstr)
            #raise e
            filename = None
            
        return filename
except ImportError:
    print( 'select_file functions not defined because PyQt5 is not available.')




if __name__ == "__main__":
    mine()
    
    
    
