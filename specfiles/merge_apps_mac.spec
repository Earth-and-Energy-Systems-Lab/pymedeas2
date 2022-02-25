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



a_pymedeas = Analysis([os.path.join(main_path, 'run.py')],
                      pathex=[],
                      binaries=[],
                      datas=added_files_pymedeas,
                      hiddenimports=['PIL._tkinter_finder', 'cmath', 'scipy.special.cython_special', 'scipy.spatial.transform._rotation_groups'],
                      hookspath=[],
                      runtime_hooks=[],
                      excludes=['pytest],
                      win_no_prefer_redirects=False,
                      win_private_assemblies=False,
                      cipher=block_cipher,
                      noarchive=False)

a_plot = Analysis([os.path.join(main_path, 'plot_tool.py')],
                  pathex=[],
                  binaries=[],
                  datas=added_files,
                  hiddenimports=['PIL._tkinter_finder', 'cmath', 'scipy.special.cython_special'],
                  hookspath=[],
                  runtime_hooks=[],
                  excludes=['pytest'],
                  win_no_prefer_redirects=False,
                  win_private_assemblies=False,
                  cipher=block_cipher,
                  noarchive=False)





pyz_pymedeas = PYZ(a_pymedeas.pure,
                   a_pymedeas.zipped_data,
                   cipher=block_cipher)

pyz_plot = PYZ(a_plot.pure,
               a_plot.zipped_data,
               cipher=block_cipher)




exe_pymedeas = EXE(pyz_pymedeas,
                   a_pymedeas.scripts, 
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

exe_plot = EXE(pyz_plot,
               a_plot.scripts,
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
               

coll_pymedeas = COLLECT(exe_pymedeas,
                        a_pymedeas.binaries,
                        a_pymedeas.zipfiles,
                        a_pymedeas.datas, 
                        strip=False,
                        upx=True,
                        upx_exclude=[],
                        name='run')





