# -*- mode: python ; coding: utf-8 -*-
import os
import sys

block_cipher = None

specpath = os.path.dirname(os.path.abspath(SPEC))
main_path = os.path.dirname(specpath)

shared_added_files = [(os.path.join(main_path, 'pytools', '*.json'), 'pytools'),
                      (os.path.join(main_path, 'plot_tool.py'), '.')]


run_added_files = [(os.path.join(main_path, 'models'), 'models'),
                   (os.path.join(main_path, 'README.md'), '.'),
                   (os.path.join(main_path, 'LICENSE'), '.'),
                   (os.path.join(main_path, 'scenarios'), 'scenarios'),
                   (os.path.join(main_path, 'pytools', '*.json'), 'pytools'),
                   (os.path.join(main_path, 'plot_tool.py'), '.')]


plot_added_files = [(os.path.join(main_path, 'models'), 'models'),
                    (os.path.join(main_path, 'pytools', '*.json'), 'pytools')]

shared_a = Analysis([os.path.join(main_path, 'shared.py')],
                 pathex=['.'],
                 binaries=[],
                 datas=shared_added_files,
                 hiddenimports=['PIL._tkinter_finder'],
                 hookspath=[],
                 hooksconfig={},
                 runtime_hooks=[],
                 excludes=['pytest', 'IPython'],
                 win_no_prefer_redirects=False,
                 win_private_assemblies=False,
                 cipher=block_cipher,
                 noarchive=False)

run_a = Analysis([os.path.join(main_path, 'run.py')],
                 pathex=['.'],
                 binaries=[],
                 datas=run_added_files,
                 hiddenimports=['PIL._tkinter_finder'],
                 hookspath=[],
                 hooksconfig={},
                 runtime_hooks=[],
                 excludes=['pytest', 'IPython'],
                 win_no_prefer_redirects=False,
                 win_private_assemblies=False,
                 cipher=block_cipher,
                 noarchive=False)

plot_a = Analysis([os.path.join(main_path, 'plot_tool.py')],
                  pathex=['.'],
                  binaries=[],
                  datas=plot_added_files,
                  hiddenimports=['PIL._tkinter_finder'],
                  hookspath=[],
                  hooksconfig={},
                  runtime_hooks=[],
                  excludes=['pytest', 'IPython'],
                  win_no_prefer_redirects=False,
                  win_private_assemblies=False,
                  cipher=block_cipher,
                  noarchive=False)

"""
MERGE arguments
Its variable-length list of arguments consists of a list of tuples, each tuple having three elements:

    The first element is an Analysis object, an instance of class Analysis, as applied to one of the apps.

    The second element is the script name of the analyzed app (without the .py extension).

    The third element is the name for the executable (usually the same as the script).

"""


MERGE( (shared_a,
        'shared',
        os.path.join('shared', 'shared')
        ),
        (run_a,
         'run',
        'pymedeas'
        ),
        (plot_a,
        'plot_tool',
        'plot'
        ))


shared_pyz = PYZ(shared_a.pure,
                 shared_a.zipped_data,
                 cipher=block_cipher)


# The EXE object creates the executable file.

shared_exe = EXE(shared_pyz,
                 shared_a.scripts,
                 shared_a.dependencies,
                 [],
                 exclude_binaries=True,
                 name='shared',
                 debug=False,
                 bootloader_ignore_signals=False,
                 strip=False,
                 upx=True,
	             icon= os.path.join(specpath, 'MEDEAS.ico'))



run_pyz = PYZ(run_a.pure,
              run_a.zipped_data,
              cipher=block_cipher)

run_exe = EXE(run_pyz,
              run_a.scripts,
              run_a.datas,
              run_a.dependencies,
              [],
              exclude_binaries=True,
              name='pymedeas', # The filename for the executable. On Windows suffix '.exe' is appended.
              debug=False,
              bootloader_ignore_signals=False,
              strip=False,
              upx=True,
              console=True,
	          icon= os.path.join(specpath, 'MEDEAS.ico'),
              disable_windowed_traceback=False,
              target_arch=None,
              entitlements_file=None )

run_coll = COLLECT(run_exe,
                   run_a.binaries,
                   run_a.zipfiles,
                   run_a.datas,
                   strip=False,
                   upx=True,
                   upx_exclude=[],
                   name='')


plot_pyz = PYZ(plot_a.pure,
               plot_a.zipped_data,
               cipher=block_cipher)

plot_exe = EXE(plot_pyz,
               plot_a.scripts,
               plot_a.datas,
               plot_a.dependencies,
               plot_a.binaries,
               plot_a.zipfiles,
               [],
               name='plot', # The filename for the executable. On Windows suffix '.exe' is appended.
               debug=False,
               bootloader_ignore_signals=False,
               strip=False,
               upx=True,
               upx_exclude=[],
	           icon= os.path.join(specpath, 'MEDEAS.ico'),
               disable_windowed_traceback=False,
               target_arch=None,
               entitlements_file=None )


shared_coll = COLLECT(#shared_exe,
                      shared_a.binaries,
                      shared_a.zipfiles,
                      shared_a.datas,
                      strip=False,
                      upx=True,
                      upx_exclude=[],
                      name=os.path.join('dist', 'shared')) # The name of the directory to be built
