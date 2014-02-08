# coding:utf8
__author__ = 'loong'
import sys
from src.version import __version__
from elib.patch import make_all
import os
import tarfile
import shutil
from mkpatchdb import make_patchdb


if 'linux' in sys.platform:
    platform = 'linux'
else:
    platform = 'win32'


base_dir = 'build/' + platform
versions_dir = '%s/versions' % base_dir
patches_dir = '%s/patches' % base_dir
boot_dir = '{0}/broom-{1}-{2}'.format(base_dir, __version__, platform)
output_dir = os.path.join(boot_dir, 'bin', __version__)


def freeze():
    from cx_Freeze import Executable, Freezer
    import shutil
    from distutils.dist import DistributionMetadata

    base = "Console"

    if sys.platform == "win32":
        base = "Win32GUI"

    dep_modules = ["PySide.QtNetwork",
                   "PySide.QtWebKit",
                   "atexit"]

    executables = [Executable('src/broom.py')]

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    class MetaData(DistributionMetadata):
        def __init__(self):
            DistributionMetadata.__init__(self)
            self.name = 'broom'
            self.version = __version__
            self.description = u'Broom ' + __version__

    freezer = Freezer(executables,
                      includeFiles=[],
                      includeMSVCR=True,
                      packages=dep_modules,
                      #includes=dep_modules,
                      excludes=[],
                      replacePaths=[],
                      copyDependentFiles=True,
                      base=base,
                      path=sys.path + ['src'],
                      createLibraryZip=True,
                      appendScriptToExe=False,
                      targetDir=output_dir,
                      zipIncludes=[],
                      #icon=icon
                      metadata=MetaData())
    freezer.Freeze()


def make_patches():
    out_path = os.path.join(patches_dir, __version__)
    files = make_all(versions_dir, __version__, out_path, 'broom.exe')
    make_patchdb(files, __version__)


def package():
    outfile = os.path.join(versions_dir, '%s.tar' % __version__)
    if not os.path.exists(versions_dir):
        os.makedirs(versions_dir)
    elif os.path.exists(outfile):
        bn = os.path.basename(outfile)
        prompt = 'Package %s already exists, replace ? (y/N)' % bn
        if raw_input(prompt) == 'y':
            os.remove(outfile)
    tar = tarfile.TarFile.open(outfile, 'w')
    tar.add(output_dir, '')
    tar.close()


def make_bootloader():
    if not os.path.exists(boot_dir):
        os.makedirs(boot_dir)
    if platform == 'win32':
        info = "{0};broom.exe".format(os.path.join('bin', __version__))
        open("%s/version_info" % boot_dir, "wb").write(info)
        shutil.copy('../boot/release/broom-boot.exe', '%s/broom.exe' % boot_dir)
    elif platform == 'linux':
        boot_sh = '%s/broom' % boot_dir
        shutil.copy('bootloader.py', boot_sh)
        os.chmod(boot_sh, 0777)


freeze()
make_bootloader()

if platform == 'linux':
    package()
    make_patches()
elif platform == 'win32':
    package()
    make_patches()
else:
    print 'Unknown platform'
