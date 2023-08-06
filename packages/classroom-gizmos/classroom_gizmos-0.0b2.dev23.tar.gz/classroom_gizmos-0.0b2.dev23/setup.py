import setuptools
import codecs
import os.path

##   ---- Time-stamp: <2020-11-12T09:43:25.299646-05:00 hedfp> -----

## code to get version number from __init__.py

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
## end version number extraction functions


def timeStampStr():
    '''Returns a string with the current time in ISO format.'''
    import datetime
    import time
    
    dt = datetime.datetime.now()
    epoch = dt.timestamp() # Get POSIX timestamp of the specified datetime.
    st_time = time.localtime(epoch) #  Get struct_time for the timestamp. This will be created using the system's locale and it's time zone information.
    tz = datetime.timezone(datetime.timedelta(seconds = st_time.tm_gmtoff)) # Create a timezone object with the computed offset in the struct_time.
    return dt.astimezone(tz).isoformat()


def writeTS( rel_path):
    '''Writes the current time and date to specified file. The file path is
    relative to this file.'''
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'w') as tsf:
        tsf.write( timeStampStr())
        tsf.close()

def getTS( rel_path):
    '''Reads first line of specified file, which is expected to be a time-date
    string.'''
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as tsf:
        lines = tsf.read()
    linelist = lines.splitlines()
    return linelist[0]

## Run tests here??

## Save timestamp for update
writeTS(( 'classroom_gizmos/timestamp.txt'))

## Get description from README.md.
with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="classroom_gizmos",
    ####version="0.0b1.dev5", # X.YaN.devM format
    version=get_version("classroom_gizmos/__init__.py"),
    author="Carl Schmiedekamp",
    author_email="cw2@psu.edu",
    description="Several small functions for classroom instruction.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Danseur1/Classroom_gizmos",
    package_data={ ## See: https://packaging.python.org/guides/distributing-packages-using-setuptools/#package-data
        # all *.txt files
        "": ["*.txt"]} ,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
	"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
	"Development Status :: 3 - Alpha"
    ],
    python_requires='>=3.6',
)
