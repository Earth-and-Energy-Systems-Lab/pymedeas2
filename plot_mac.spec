# -*- mode: python ; coding: utf-8 -*-
import os
import matplotlib as mpl


specpath = os.path.dirname(os.path.abspath(SPEC))
matplotlibrc_path = os.path.dirname(mpl.matplotlib_fname())

block_cipher = None

added_files = [(matplotlibrc_path, '.matplotlib/mpl-data/'),
               ('./pytools/config.json', './pytools'),
               ('./pytools/models.json', './pytools')]

a = Analysis(['plot_tool.py'],
             pathex=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='plot',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
	  icon= os.path.join(specpath, 'MEDEAS.ico'),
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
