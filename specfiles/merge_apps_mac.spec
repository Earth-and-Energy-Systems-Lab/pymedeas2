# -*- mode: python ; coding: utf-8 -*-

"""
For this script to work, we need to create an environmental variable named KEY, which is the path to the key file used to sign the code
"""
import os
import matplotlib as mpl
                                 
specpath = os.path.dirname(os.path.abspath(SPEC))
main_path = os.path.dirname(specpath)

mtpl_path = os.path.dirname(mpl.matplotlib_fname())
matplotlibrc_path = os.path.join(mtpl_path, 'matplotlibrc')
mtplt_images_path = os.path.join(mtpl_path, 'images')

block_cipher = None

added_files_shared = [(os.path.join(main_path, 'pytools', '*.json'), 'pytools'),
                      (matplotlibrc_path, 'matplotlib/mpl-data'),
                      (mtplt_images_path, 'matplotlib/mpl-data/images'),
                      (os.path.join(main_path, 'pytools', '*.json'), 'pytools'),
                      (os.path.join(main_path, 'plot_tool.py'), '.')]

added_files_pymedeas = [(os.path.join(main_path, 'models'), 'models'),
                        (os.path.join(main_path, 'README.md'), '.'),
                        (os.path.join(main_path, 'LICENSE'), '.'),
                        (os.path.join(main_path, 'scenarios'), 'scenarios'),
                        (os.path.join(main_path, 'pytools', '*.json'), 'pytools'),
                        (os.path.join(main_path, 'plot_tool.py'), '.'),
	        ]

added_files_plot = [(matplotlibrc_path, 'matplotlib/mpl-data'),
                    (mtplt_images_path, 'matplotlib/mpl-data/images'),
                    (os.path.join(main_path, 'pytools', '*.json'), 'pytools')]


shared_a = Analysis([os.path.join(main_path, 'shared.py')],
                    pathex=[],
                    binaries=[],
                    datas=added_files_shared,
                    hiddenimports=['PIL._tkinter_finder', 'cmath', 'scipy.special.cython_special', 'scipy.spatial.transform._rotation_groups'],
                    hookspath=[],
                    runtime_hooks=[],
                    excludes=['pytest', 'IPython'],
                    win_no_prefer_redirects=False,
                    win_private_assemblies=False,
                    cipher=block_cipher,
                    noarchive=False)

run_a = Analysis([os.path.join(main_path, 'run.py')],
                 pathex=[],
                 binaries=[],
                 datas=added_files_pymedeas,
                 hiddenimports=['PIL._tkinter_finder', 'cmath', 'scipy.special.cython_special', 'scipy.spatial.transform._rotation_groups'],
                 hookspath=[],
                 runtime_hooks=[],
                 excludes=['pytest','IPython'],
                 win_no_prefer_redirects=False,
                 win_private_assemblies=False,
                 cipher=block_cipher,
                 noarchive=False)

plot_a = Analysis([os.path.join(main_path, 'plot_tool.py')],
                  pathex=[],
                  binaries=[],
                  datas=added_files_plot,
                  hiddenimports=['PIL._tkinter_finder', 'cmath', 'scipy.special.cython_special'],
                  hookspath=[],
                  runtime_hooks=[],
                  excludes=['pytest', 'IPython'],
                  win_no_prefer_redirects=False,
                  win_private_assemblies=False,
                  cipher=block_cipher,
                  noarchive=False)


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

run_pyz = PYZ(run_a.pure,
              run_a.zipped_data,
              cipher=block_cipher)

plot_pyz = PYZ(plot_a.pure,
               plot_a.zipped_data,
               cipher=block_cipher)





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
                 console=True,
	             icon= os.path.join(specpath, 'MEDEAS.icns'),
                 disable_windowed_traceback=False,
                 target_arch=None,
                 codesign_identity=os.environ.get('KEY'),
                 entitlements_file=None)

run_exe = EXE(run_pyz,
              run_a.scripts,
              run_a.datas,
              run_a.dependencies,
              [],
              exclude_binaries=True,
              name='pymedeas',
              debug=False,
              bootloader_ignore_signals=False,
              strip=False,
              upx=True,
              console=True,
	          icon= os.path.join(specpath, 'MEDEAS.icns'),
              disable_windowed_traceback=False,
              target_arch=None,
              codesign_identity=os.environ.get('KEY'),
              entitlements_file=None)


run_coll = COLLECT(run_exe,
                   run_a.binaries,
                   run_a.zipfiles,
                   run_a.datas, 
                   strip=False,
                   upx=True,
                   upx_exclude=[],
                   name='')


plot_exe = EXE(plot_pyz,
               plot_a.scripts,
               plot_a.datas,
               plot_a.dependencies,
               plot_a.binaries,
               plot_a.zipfiles,
               [],
               exclude_binaries=True,
               name='plot_tool',
               debug=False,
               bootloader_ignore_signals=False,
               strip=False,
               upx=True,
               codesign_identity=os.environ.get('KEY'),
               icon= os.path.join(specpath, 'MEDEAS.icns'),
               console=False )
               


shared_coll = COLLECT(#shared_exe,
                      shared_a.binaries,
                      shared_a.zipfiles,
                      shared_a.datas,
                      strip=False,
                      upx=True,
                      upx_exclude=[],
                      name=os.path.join('dist', 'shared')) # The name of the directory to be built





