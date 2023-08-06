# Classroom Gizmos
This is a collection of functions for classroom instruction in
introductory physics. This is basically using ipython as a calculator
that displays the calculation and the results.<br>
Typical usage to make a set of useful functions available in ipython:

    from classroom_gizmos.handies import *

<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
## handies
*_classroom_gizmos.handies_* is a collection of small functions
that are
useful from an ipython prompt. <br>
__Note: Imports from astropy, PyQt5, and func_timeout__<br>
Certain functions and functionality are not available when some of the
imported packages are unavailable.<br>
The **mine()** function lists all the user functions defined
in *_handies.py_*.

### handies defines or imports:
    cdbn(), osname(), getCCode()
    hostname(), call(), rad(), deg(), sinD(), cosD(), tanD(),
    asinD(), acosD(), atanD(), atan2D(), atan2P(), nCr(), comb(),
    pltsize(), select_file(), select_file_timeout(), getTS(), timeStampStr(),
    isInstalled(), randomLetter(), randomElement(), count_down()
    mine()

### Clear screen functions:
    cls  (iPython magic %cls) outputs 23 blank lines.
    clsall() deletes previous text using ascii control character.
Trig Functions in Degrees<br>
&nbsp;&nbsp;&nbsp;&nbsp;'D' and 'P' trig functions work with degrees.<br>
&nbsp;&nbsp;&nbsp;&nbsp;'P' inverse functions return only positive angles.

greeks  &#10230; a string with greek alphabet.<br>
pltsize( w, h, dpi=150) &#10230; resizes plots in matplotlib.<br>
getTS() &#10230; returns a readable time stamp string.<br>
isInstalled( pkgNameStr) &#10230; returns package or None if pkg is not installed.<br>
timeStampStr() &#10230; returns a readable, timestamp string.<br>
From random imports randint and defines randomLetter

mine() &#10230; lists what handies.py defines.
### If PyQt5 package is available defines:
select_file and select_file_timeout
### From math imports these functions:
pi, sqrt, cos, sin, tan, acos, asin, atan, atan2,
degrees, radians, log, log10, exp
### When astropy is available:
Defines nowMJD(); mjd2date(), date2mjd().<br>
Imports astropy.units as "u", i.e. u.cm or u.GHz
### Misc.
The variable 
__IsInteractive__ is True if in interpreter, False if running from command line.<br>
Line magic *cls* is defined, outputs 23 blank lines to 'clear' screen.<<br>
Sets ipython numeric format to %.5g


## jupyter_file_browser
This module implements a file browser that can be used
in a Jupyter Notebook.  (Not usable in Jupyter lab.)<br>
__Typical Usage:__

	from classroom_gizmos.jupyter_file_browser import box, get_file_path
    box
	
A file select widget will be created below that cell.

In a following notebook cell:

    path = get_file_path()  ## returns path of currently selected file in
    the file select cell.


## import_install
### importInstall()
    pkg = importInstall( 'pkg_name')
    OR
    pkg = importInstall( 'pkg_name, 'PyPI_name')
This function tries to import a specified package and if that fails,
it tries to install the package and then import it.<br>
_*importInstall*_ was written so that python programs can be
distributed to students without detailed instructions on checking if
packages are installed
and information on installing the needed packages.<br>
The function returns the package or None.<br>

**Warning:** _importInstall_ can not install all packages. It is less likely to install a package that is not pure python.

## BestByMinBefore
### functions
decCredit() returns perl code for use in WebAssign answer credit calculations.
Convenience functions:

    BBPdecCredit(), InCdecCredit(),
    HWdecCredit(), getCCode()

<hr>
getCCode() is an interactive 'wizard' that has no parameters, but steps through options needed to 
produce the Perl conditional code for various question types.

All functions should have doc strings that give more information about usage and parameters.

