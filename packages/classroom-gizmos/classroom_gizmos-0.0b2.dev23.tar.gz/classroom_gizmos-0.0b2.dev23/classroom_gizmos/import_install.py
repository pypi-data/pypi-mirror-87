#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 15:53:29 2020

@author: cws2
@Time-stamp: <2020-11-24T18:06:53.308934-05:00 hedfp>


importInstall - tests import of package and if that fails, tries to install
  and then tries again to import the package. If it succedes, returns module
  object.
Copyright (C) 2020 Carl Schmiedekamp

2020-09-30 /CS/ Added rough progress indication by outputing '*' on each call
                to runCatch(), when verboseInstall is False

"""

'''
Ref: https://stackoverflow.com/questions/12332975/installing-python-module-within-code

Ref: https://jakevdp.github.io/blog/2017/12/05/installing-python-packages-from-jupyter/
---------------------
'''

import sys
import subprocess



## Here add unusual install commands, use list if more than one command line is needed.

verboseInstall = False 

PipSpecialCases = { }

PipSpecialCases[ 'p2j'] = 'pip install git+https://github.com/remykarem/python2jupyter#egg=p2j'
PipSpecialCases[ 'pypulse'] = 'python -m pip install git+https://github.com/mtlam/PyPulse#egg=PyPulse'
PipSpecialCases[ 'saba'] = ['conda install --yes -c sherpa sherpa', 'pip install saba']

PipSpecialCases[ 'func_timeout'] = ['pip install func-timeout']

PipSpecialCases[ 'pscTest'] = [ 'echo This is a test.', 'echo test', 'echo test.']
PipSpecialCases[ 'vpython'] = 'pip install vpython'
PipSpecialCases[ 'ipyvolume'] = ['pip install ipyvolume', 
                               'jupyter nbextension enable --py --sys-prefix ipyvolume',
                               'jupyter nbextension enable --py --sys-prefix widgetsnbextension']

# pymc3 may require install of VC runtime:
#    https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads

CondaSpecialCases = {}
CondaSpecialCases[ 'pymc3'] = 'conda install --yes -c conda-forge pymc3'
CondaSpecialCases[ 'ipyvolume'] = 'conda install --yes -c conda-forge ipyvolume'
CondaSpecialCases[ 'wordcloud'] = 'conda install --yes -c conda-forge wordcloud'


## CondaSpecialCases[ 'vpython'] = 'conda install --yes -c vpython vpython'
## in illumidesk, installs with pip but not conda.



## PipInstallDict not currently used
PipInstallDict = { }
PipInstallDict[ 'pip'] = 'python -m pip install -U pip'
PipInstallDict[ 'scipy'] = 'python -m pip install --user scipy'
PipInstallDict[ 'matplotlib'] = 'python -m pip install --user matplotlib'
PipInstallDict[ 'ipython'] = 'python -m pip install --user ipython'
PipInstallDict[ 'jupyter'] = 'python -m pip install --user jupyter'
PipInstallDict[ 'pandas'] = 'python -m pip install --user pandas'
PipInstallDict[ 'sympy'] = 'python -m pip install --user sympy'
PipInstallDict[ 'nose'] = 'python -m pip install --user nose'
PipInstallDict[ 'numdifftools'] = 'python -m pip install --user numdifftools'
PipInstallDict[ 'pymc3'] = 'python -m pip install --user pymc3'
PipInstallDict[ 'statsmodels'] = 'python -m pip install --user statsmodels'
PipInstallDict[ 'astropy'] = 'python -m pip install --user astropy'
PipInstallDict[ 'seaborn'] = 'pip install seaborn'
PipInstallDict[ 'emcee'] = [ 'python -m pip install -U pip',
                             'pip install -U setuptools setuptools_scm pep517',
			     'pip install -U emcee']
PipInstallDict[ 'ptest'] = [ 'conda update conda', 'python -m pip install -U pip']

#-- special case:
PipInstallDict[ 'scipy+'] = 'python -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose'


## CondaInstallDict is not currently used
CondaInstallDict = { }
CondaInstallDict[ 'pip'] = 'conda install --yes pip'
CondaInstallDict[ 'sympy'] = 'conda install --yes sympy'
CondaInstallDict[ 'astropy'] = 'conda install --yes astropy'
CondaInstallDict[ 'matplotlib'] = 'conda install --yes matplotlib'
CondaInstallDict[ 'pymc3'] = 'conda install --yes -c conda-forge pymc3'
CondaInstallDict[ 'seaborn'] = 'conda install --yes seaborn '
CondaInstallDict[ 'emcee'] = [ 'conda update conda',
                               'conda install --yes -c conda-forge emcee']
CondaInstallDict[ 'ctest'] = [ 'conda update conda', 'python -m pip install -U pip']


def call( cmd):
    '''Modeled after call function in NANOGrav Spring 2020 workshop.
    call() just executes the command in the shell and displays output,
    while runCatch( cmd) tries to catch all errors and output and only returns
    True of False to indicate success or failure.'''
    subprocess.call( cmd, shell=True)

def runCatch( it):
    '''Run string(s) from commandline.
    Returns True if no error was produced and False if an error was produced.'''
    
    if isinstance( it, list):
        cmdList = it
    else:
        cmdList = [ it]

    success = True  ## is set to False if any command fails.
    for cmd_i in cmdList:
        if verboseInstall:
            print( 'Trying to execute:\n{}'.format( cmd_i))
        else:
            print( ' *', end='')

        try:
            cmds = cmd_i.split()
            returned = subprocess.Popen( cmds, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, universal_newlines=True)
            output, errors = returned.communicate()
            returncode = returned.returncode
            if verboseInstall:
                print(' Command line returned code {}.'.format( returncode))
                if len( errors) > 0:
                    print( "  stderr is:\n")
                    print( errors, '\n')
            if returncode == 0:
                success = True
            else:
                success = False
                            
        except Exception as e:
            if verboseInstall:
                print( e)
                success = False
    return success

def call_verbose( cmd):
    '''Execute shell command and report return code, output, and errors.
    cmd is string or list of strings to be executed.
    Note each command is executed in the current directory.
    Ref: https://www.golinuxcloud.com/python-subprocess/#Using_python_subprocess_call()_function'''
    
    import subprocess
    
    if isinstance( cmd, list):
        cmdList = cmd
    else:
        cmdList = [ cmd]

    for cmdstr in cmdList:
        print('cmd is\n >>>', cmdstr)
        # Use shell to execute the command
        sp = subprocess.Popen(cmdstr,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True)
        
        # Separate the output and error.
        # This is similar to Tuple where we store two values to two different variables
        out,err=sp.communicate()
        
        # Store the return code in rc variable
        rc=sp.wait()
        
        print('Return Code:',rc,'\n')
        print('output is: \n', out)
        print('error is: \n', err)
    

def hasConda():
    '''returns True if running in Conda (if package conda is available).'''
    try:
        __import__( 'conda')
        return True
    except ImportError: 
        return False

def locatePythonPrefix():
    '''setup python executable path and condaprefix if conda is used.
    sets 'pythonExe' to path of python executable and 
    sets 'condaPrefix' to the prefix path or None if conda is not used.'''
    pythonExe = sys.executable
    if hasConda():
        condaPrefix = sys.prefix
    else:
        condaPrefix = None
    return pythonExe, condaPrefix

def is_installed( pkgname):
    ''' Imports pkgname and returns package if installed.
        pkgname is a string with name of package as used in import stmt.
        If not installed, returns None.
        This should be a copy of isInstalled() in handies.
        No attempt to install is made.
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
    
def importInstall( pkgname, installname=None):
    '''Tries to import package named in string 'pkgname'.
    If import fails, tries to install pkgname and then import.
    
    Warning, only use the base package.  For example:
       matplotlib = importInstall( 'matplotlib')
       import matplotlib.pyplot as plt
     instead of 
       plt = importInstall( 'matplotlib.pyplot')
     which does not reliably work.
       
     If the repository nume is different from the package name,
     specify that name as the second argument.  Ex:
         importInstall( 'pint', 'pint_pulsar')
     If there were no successful install, an error message is reported and None
     is returned.
     Also defined are these two aliases:
         II
         import_install
        '''
    if installname == None:
        installfromname = pkgname
    else:
        installfromname = installname
    
    try:
        pkg = __import__( pkgname)
        ##print( 'At 4')
        if verboseInstall:
            print( ' {} imported.'.format( pkgname))
        return pkg
    except Exception:
        
        # print( '\nTrying to install {}, this may take a while.\n'.format( pkgname))
        print( '\nTrying to install {}, this may take a while.'.format(
            pkgname), end='')
        if verboseInstall:
            print('\n\n')

        
        ## import failed, so now try to install
        pythonExe, condaPrefix = locatePythonPrefix() ## get python executable, and conda prefix

    ## first check if package is known special case
        if hasConda() and installfromname in CondaSpecialCases:
            ck = runCatch(  CondaSpecialCases[ installfromname])
            
        elif installfromname in PipSpecialCases:
            ck = runCatch( PipSpecialCases[ installfromname])
        else:
            ck = False
            
        if ck:
            try:
                pkg = __import__( pkgname)
                if verboseInstall:
                    print( ' {} imported.'.format( pkgname))
                else:
                    print('\n')
                return pkg
            except Exception:
                None
            ## if special install fails, try other ways.
        

	## try installing from conda repository if conda is available
        if ( condaPrefix != None) and runCatch( 'conda install --yes --prefix ' +\
                                    condaPrefix + ' ' + installfromname):
            pkg = __import__( pkgname)
            if verboseInstall:
                print( ' {} imported.'.format( pkgname))
            else:
                print('\n')
            return pkg

	## try installing from conda-forge repository
        elif ( condaPrefix != None) and runCatch( 'conda install --yes --prefix ' +\
                                    condaPrefix + ' -c conda-forge ' + installfromname):
            pkg = __import__( pkgname)
            ##print( 'At 6')
            if verboseInstall:
                print( ' {} imported.'.format( pkgname))
            else:
                print('\n')
            return pkg

        # ## try installing with pip (disabled, in case it would prompt for permission)
        # elif runCatch( pythonExe + ' -m pip install ' + installfromname):
        #     pkg = __import__( pkgname)
        #     ##print( 'At 7')
        #     if verboseInstall:
        #         print( ' {} imported.'.format( pkgname))
        #     else:
        #         print('\n')
        #     return pkg
	
	## try installing with pip to user directory
        elif runCatch( pythonExe + ' -m pip install --user ' + installfromname):
            pkg = __import__( pkgname)
            ##print( 'At 7')
            if verboseInstall:
                print( ' {} imported.'.format( pkgname))
            else:
                print('\n')
            return pkg
        
        else:   
            ##print( 'At 8')
            if verboseInstall:
                print( ' --> Problems importing or installing {}!'.format( pkgname))
            else:
                print('\n')
            return None
        
II = importInstall             ## alias
import_install = importInstall ## alias

def pkg_from_path( pkg_name, pkg_path):
    '''
    Ref: https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path

    Parameters
    ----------
    pkg_name : string
        DESCRIPTION.
    pkg_path : string
        For a package, it is the full path to the __init__.py file.

    Returns
    -------
    my_module : module  --Experimental --
    
    Useful for testing a development version??
    
    usage:
            pkgname = 'classroom_gizmos'
            path = pkg_from_path(pkg_name, pkg_path)
        
            classroom_gizmos = pkg_from_path( pkgname, path)
        
            # pkg = import_local( pkgname, path)
            
            print( classroom_gizmos)
            
            from classroom_gizmos.handies import *
    


    '''
    # pkg_path = "/path/to/your/module/__init__.py"
    # pkg_name = "mymodule"
    
    import importlib
    import sys
    spec = importlib.util.spec_from_file_location(pkg_name, pkg_path)
    my_pkg = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = my_pkg
    spec.loader.exec_module( my_pkg)
    
    return my_pkg
    

   
if __name__ == "__main__":
        
    verboseInstall = False ## turn on/off extra output
    fullInstallList = False ## True -> do full list of install checks.
    
    platform = importInstall( 'platform')
    os = importInstall( 'os')
    subprocess = importInstall( 'subprocess')

    if hasConda():
        import conda
        print( '\nConda system version {}'.format( conda.__version__))
    else:
        print( '\nConda system NOT found.')
    print( 'Python version: {}'.format( platform.python_version()))
    print( 'OS name: {}, system name: {}, release: {}'.format( os.name,
                                       platform.system(), platform.release()))
    print( )

    np = importInstall( 'numpy')
    matplotlib = importInstall( 'matplotlib')
    import matplotlib.pyplot as plt
    
    vpython = importInstall( 'vpython')
    from vpython import *
    ## 2020-09-30  crashes Spyder when vpython browser window is clossed:
    # ball = sphere( color=color.blue)
    
    if fullInstallList: ## try a lot of packages
        ndt = importInstall( 'numdifftools')
    
        statsmodels = importInstall( 'statsmodels')
        astropy = importInstall( 'astropy')
        if os.name == 'posix':
            pint = importInstall( 'pint', 'pint-pulsar')
            pm3 = importInstall( 'pymc3')
        else:
            print( '\nSkipping pint, and pymc3.  They may not be supported on {}\n'.format( os.name))
            ##  pint doesn't install on Windows because of floating point precision problem.
        np = importInstall( 'numpy')
        emcee = importInstall( 'emcee')
        easygui = importInstall( 'easygui')
        passwordmeter = importInstall( 'passwordmeter')
        zxcvbn = importInstall( 'zxcvbn')
        pypulse = importInstall( 'pypulse')
        wxpython = importInstall( 'wx', 'wxpython')
        # func_timeout = importInstall( 'func_timeout')
    
        if os.name == 'nt':
            print( 'Note: sherpa may not install on NT, trying anyway.')
        saba = importInstall( 'saba')
        
        oops1 = importInstall( 'pscTest')
        oops2 = importInstall( 'fredricka')
        print( '\n\nsaba: {}; oops1: {}; oops2: {}'.format( saba, oops1, oops2))
    else:
        oops2 = importInstall( 'fredricka536092')
        print( 'Trying fredricka536092: ImportInstall returned {}'.format( oops2))
    
    import socket
    computer_name = socket.getfqdn()
    if  computer_name == 'Yoga-New':
        ckpypulse = pkg_from_path( 'pypulse', r"C:\Users\hedfp\OneDrive - The Pennsylvania State University\Pythonista\PyPulse\pypulse\__init__.py")
        print( 'For pypulse, pkg_from_path returned type {}'.format( type( ckpypulse)))
    import numpy as ckpath
    npck = pkg_from_path( 'numpy', ckpath.__file__)
    print( 'numpy version via pkg_from_path: {}'.format( npck.__version__))
    