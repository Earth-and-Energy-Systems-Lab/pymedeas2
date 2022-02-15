# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import os
import matplotlib as mpl


specpath = os.path.dirname(os.path.abspath(SPEC))

mtpl_path = os.path.dirname(mpl.matplotlib_fname())
matplotlibrc_path = os.path.join(mtpl_path, 'matplotlibrc')
mtplt_images_path = os.path.join(mtpl_path, 'images')

added_files = [(matplotlibrc_path, 'matplotlib/mpl-data'),
               (mtplt_images_path, 'matplotlib/mpl-data/images'),
               ('./pytools/config.json', 'pytools'),
               ('./pytools/models.json', 'pytools')]

a = Analysis(['plot_tool.py'],
             pathex=['/Users/roger/Development/pymedeas2'],
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
          icon= os.path.join(specpath, 'MEDEAS.ico'),
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='plot_tool')
