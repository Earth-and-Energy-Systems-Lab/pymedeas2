# -*- mode: python ; coding: utf-8 -*-
import os
                                 
specpath = os.path.dirname(os.path.abspath(SPEC))

block_cipher = None

added_files = [('./models/', 'models'),
               ('./README.md', '.'),
               ('./LICENSE', '.'),
               ('./scenarios/', 'scenarios'),
               ('./pytools/*.json', 'pytools')
	       ]



a = Analysis(['run.py', 'plot_tool.py'],
             pathex=[],
             binaries=[],
             datas=added_files,
             hiddenimports=['PIL._tkinter_finder'],
             hookspath=[],
             hooksconfig={},
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
          name='pymedeas',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
	  icon= os.path.join(specpath, 'MEDEAS.ico'),
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=os.environ.get("KEY"),
          entitlements_file=None )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='run')
