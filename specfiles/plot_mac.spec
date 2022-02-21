# -*- mode: python ; coding: utf-8 -*-

"""
For this script to work, we need to create an environmental variable named KEY,
which is the path to the key file used to sign the code
"""

block_cipher = None

import os
import matplotlib as mpl


specpath = os.path.dirname(os.path.abspath(SPEC))
main_path = os.path.dirname(specpath)

mtpl_path = os.path.dirname(mpl.matplotlib_fname())
matplotlibrc_path = os.path.join(mtpl_path, 'matplotlibrc')
mtplt_images_path = os.path.join(mtpl_path, 'images')

added_files = [(matplotlibrc_path, 'matplotlib/mpl-data'),
               (mtplt_images_path, 'matplotlib/mpl-data/images'),
               (os.path.join(main_path, 'pytools', '*.json'), 'pytools')]

a = Analysis([os.path.join(main_path, 'plot_tool.py')],
             pathex=[main_path],
             binaries=[],
             datas=added_files,
             hiddenimports=['PIL._tkinter_finder', 'cmath', 'scipy.special.cython_special'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='plot_tool',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          codesign_identity=os.environ.get('KEY'),
          icon= os.path.join(specpath, 'MEDEAS.icns'),
          console=True )

# if this does not work, replace it with what is below (coll)
app = BUNDLE(exe,
         a.binaries, # copied from coll
         a.zipfiles, # copied from coll
         a.datas, # copied from coll
         strip=False, # copied from coll
         upx=True, # copied from coll
         upx_exclude=[], # copied from coll
         name='plot.app',
         icon=os.path.join(specpath, 'MEDEAS.icns'),
         bundle_identifier=None)

#coll = COLLECT(exe,
#               a.binaries,
#               a.zipfiles,
#               a.datas,
#               strip=False,
#               upx=True,
#               upx_exclude=[],
#               name='plot_tool')
