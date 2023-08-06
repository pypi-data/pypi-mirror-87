#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 10:32:35 2020
-----    Time-stamp: <2020-08-02T14:16:35.633361-04:00 hedfp>      -----

@author: (of mods) Carl Schmiedekamp
@Original Source: https://gist.github.com/thomasaarholt/b89b3f29ad82cd32176f2605834fa8ac


WARNING: Does not work in Jupyter Lab!

Inssstructions:
    1. pip install classroom_gizmos
    in notebook:
        from classroom_gizmos.jupyter_file_browser import box, get_file_path
        box    ## creates the file selection ipywidget box.
        ---
        path = get_file_path()  ## every time this cell is executed, the currently 
                                ## selected file's path is returned.

Instructions, using source:
    1. paste code in Jupyter notebook cell
    2. execute the cell and select file
    3. in another cell call get_file_path() which returns selected file.

"""

import ipywidgets as widgets
## Ref: https://gist.github.com/thomasaarholt/b89b3f29ad82cd32176f2605834fa8ac

import os
from pathlib import Path

newpath = None ## path to selected file or folder
newfile = None ## full path returned by get_file_path()

cwd = Path(os.getcwd())

FOLDERLABEL = '-------FOLDERS-------'
FILESLABEL = '-------FILES-------'

def get_folder_contents(folder):
    'Gets contents of folder, sorting by folder then files, hiding hidden things'
    folder = Path(folder)
    folders = [item.name for item in folder.iterdir() if item.is_dir() and not item.name.startswith('.')]
    files = [item.name for item in folder.iterdir() if item.is_file() and not item.name.startswith('.')]
    # print( 'get_folder_contents--')
    return [FOLDERLABEL] + sorted(folders) + [FILESLABEL] + sorted(files)

def go_to_address(address):
    address = Path(address)
    if address.is_dir():
        address_field.value = str(address)
        base.value = os.path.basename( str(address))
        select.unobserve(selecting, names='value')
        select.options = get_folder_contents(folder=address)
        select.observe(selecting, names='value')
        select.value = None
    # print( 'go_to_address--')

def newaddress(value):
    go_to_address(address_field.value)
    ##print( 'newaddress--')
        
def selecting(value):
    global newpath
    if value['new'] and value['new'] not in [FOLDERLABEL, FILESLABEL]:
        path = Path(address_field.value)
        newpath = path / value['new']
        if newpath.is_dir():
            go_to_address(newpath)
            
        elif newpath.is_file():
            #some other condition
            pass
        # print( 'selecting-- path:{} newpath: {}'.format( path, newpath))
        # print( '  types path: {}, newpath: {}, value[ new]: {}'.format( type( path), type( newpath), type( value['new'])))

def parent(value):
    new = Path(address_field.value).parent
    go_to_address(new)
    # print( 'parent--')
    
def load(value):
    global newfile
    ##filepath = path / value['new']
    # load using your favourite python software!
    newfile = newpath
    # print( 'load-- newpath: {}, newfile: {}'.format( newpath, newfile))

def get_file_path():
    '''User access to last file selected.'''
    # print( 'getFilepath-- newfile: {}, newpath: {}'.format( newfile, newpath))
    return newfile
    
    
address_field = widgets.Text(value=str(cwd))
up_button = widgets.Button(description='Up')
select = widgets.Select(options=get_folder_contents(cwd), rows=15, value=None)
load_button = widgets.Button(description='Select')
base = widgets.Text( str( os.path.basename( cwd)))
box = widgets.HBox([widgets.VBox([address_field, base, select]), widgets.VBox([up_button, load_button])])

select.observe(selecting, names='value')
up_button.on_click(parent)
#load_button.observe(load)
load_button.on_click(load)
address_field.on_submit(newaddress)

##in jupyter execute box
##box