# -*- mode: python ; coding: utf-8 -*-

"""
This creates a folder dist that contains the executables for the plot_tool and
for the pymedeas, as well as all the folders and files that the user should be
able to modify to parametrise the model. The libraries shared between the
pymedeas and plots executables will be placed in the shared directory.
 
To run this, we need to first create a copy of run.py and save it as shared.py

"""


import os
import sys
import platform

block_cipher = None

specpath = os.path.dirname(os.path.abspath(SPEC))
main_path = os.path.dirname(specpath)

mtpl_path = os.path.dirname(mpl.matplotlib_fname())
matplotlibrc_path = os.path.join(mtpl_path, 'matplotlibrc')
mtplt_images_path = os.path.join(mtpl_path, 'images')


shared_added_files = [(matplotlibrc_path, 'matplotlib/mpl-data'),
                      (os.path.join(main_path, 'pytools', '*.json'), 'pytools'),
                      (os.path.join(main_path, 'plot_tool.py'), '.')]


run_added_files = [(matplotlibrc_path, 'matplotlib/mpl-data'),
                   (os.path.join(main_path, 'models'), 'models'),
                   (os.path.join(main_path, 'README.md'), '.'),
                   (os.path.join(main_path, 'LICENSE'), '.'),
                   (os.path.join(main_path, 'scenarios'), 'scenarios'),
                   (os.path.join(main_path, 'pytools', '*.json'), 'pytools'),
                   (os.path.join(main_path, 'plot_tool.py'), '.')]


plot_added_files = [(matplotlibrc_path, 'matplotlib/mpl-data'),
                    (mtplt_images_path, 'matplotlib/mpl-data/images'),
                    (os.path.join(main_path, 'models'), 'models'),
                    (os.path.join(main_path, 'pytools', '*.json'), 'pytools')]

shared_a = Analysis([os.path.join(main_path, 'shared.py')],
                 pathex=['.'],
                 binaries=[],
                 datas=shared_added_files,
                 hiddenimports=[
                     'PIL._tkinter_finder',
                     'cmath',
                     'scipy.special.cython_special',
                     'scipy.spatial.transform._rotation_groups'],
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
                 hiddenimports=[
                     'PIL._tkinter_finder',
                     'cmath',
                     'scipy.special.cython_special',
                     'scipy.spatial.transform._rotation_groups'],
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
                  hiddenimports=[
                      'PIL._tkinter_finder',
                      'cmath',
                      'scipy.special.cython_special'],
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

# If we do not remove these binaries, we get this file shouldn't be here warnings
if platform.system() == "Windows":
    to_remove = ["libbz2.dll",
                 "msvcp140.dll",
                 "vcruntime140.dll",
                 "vcruntime140_1.dll"]
    for dep in plot_a.dependencies:
        for duplicate in to_remove:
            if duplicate in dep[1]:
                plot_a.dependencies.remove(dep)

    for dep in run_a.dependencies:
        for duplicate in to_remove:
            if duplicate in dep[1]:
                run_a.dependencies.remove(dep)



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
	             icon= os.path.join(specpath, 'MEDEAS.icns'),
                 codesign_identity=os.environ.get('KEY'),
                 entitlements_file=None)



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
              console=True, # this must be True
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
               console=False,
               upx=True,
               upx_exclude=[],
	           icon= os.path.join(specpath, 'MEDEAS.icns'),
               disable_windowed_traceback=False,
               target_arch=None,
               codesign_identity=os.environ.get('KEY'),
               entitlements_file=None)


shared_coll = COLLECT(#shared_exe,
                      shared_a.binaries,
                      shared_a.zipfiles,
                      shared_a.datas,
                      strip=False,
                      upx=True,
                      upx_exclude=[],
                      name=os.path.join('dist', 'shared')) # The name of the directory to be built
