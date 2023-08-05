'''import setuptools
from distutils.core import setup, Extension

with open("README.md", "r") as fh:
    long_description = fh.read()

module1 = Extension('timsort',
                    sources = ['sorting_code/timsort.c'], library_dirs = ['/home/leha/Desktop/projects/library/CustomTimSort_2/sorting_code', '/home/leha/Desktop/projects/library/CustomTimSort_2/sorting_code/clinic'], include_dirs = ['/home/leha/Desktop/projects/library/CustomTimSort_2/sorting_code', '/home/leha/Desktop/projects/library/CustomTimSort_2/sorting_code/clinic', '/home/leha/Desktop/projects/library/CustomTimSort_2/sorting_code/cpython'])

setuptools.setup(
    name="customtimsort",
    version="0.0.62",
    author="lehatr",
    author_email="lehatrutenb@gmail.com",
    description="Timsort sorting algorithm with custom minrun",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lehatrutenb/FastTimSort",
    ext_modules = [module1],
    package_dir={'': 'sorting_code/'},
    package_data={'': ['*', 'clinic/*', 'cpython/*']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)'''
from __future__ import absolute_import, division, print_function

import errno
import functools
import glob
import os
import os.path
import platform
import subprocess
import sys
from distutils.sysconfig import get_config_vars

from setuptools import Distribution, setup
from setuptools.command.build_ext import build_ext as _build_ext

try:
    from setuptools.command.build_clib import build_clib as _build_clib
except ImportError:
    from distutils.command.build_clib import build_clib as _build_clib


def here(*paths):
    return os.path.relpath(os.path.join(*paths))


def abshere(*paths):
    return os.path.abspath(here(*paths))


# sys.path.insert(0, abshere("src"))!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def which(name, flags=os.X_OK):  # Taken from twisted
    result = []
    exts = filter(None, os.environ.get("PATHEXT", "").split(os.pathsep))
    path = os.environ.get("PATH", None)
    if path is None:
        return []
    for p in os.environ.get("PATH", "").split(os.pathsep):
        p = os.path.join(p, name)
        if os.access(p, flags):
            result.append(p)
        for e in exts:
            pext = p + e
            if os.access(pext, flags):
                result.append(pext)
    return result


def use_system():
    install_type = os.environ.get("SODIUM_INSTALL")

    if install_type == "system":
        # If we are forcing system installs, don't compile the bundled one
        return True
    else:
        # By default we just use the bundled copy
        return False


class Distribution(Distribution):
    def has_c_libraries(self):
        return not use_system()


class build_clib(_build_clib):
    def get_source_files(self):
        '''files = glob.glob(here("src/libsodium/*"))
        files += glob.glob(here("src/libsodium/*/*"))
        files += glob.glob(here("src/libsodium/*/*/*"))
        files += glob.glob(here("src/libsodium/*/*/*/*"))
        files += glob.glob(here("src/libsodium/*/*/*/*/*"))
        files += glob.glob(here("src/libsodium/*/*/*/*/*/*"))'''
        files = glob.glob(here("/home/leha/Desktop/projects/library/CustomTimSort_2/sorting_code/*"))
        files += glob.glob(here("/home/leha/Desktop/projects/library/CustomTimSort_2/sorting_code/*/*"))
        files += glob.glob(here("/home/leha/Desktop/projects/library/CustomTimSort_2/sorting_code/*/*/*"))

        return files

    def build_libraries(self, libraries):
        raise Exception("build_libraries")

    def check_library_list(self, libraries):
        raise Exception("check_library_list")

    def get_library_names(self):
        return ["timsort"]

    def run(self):
        if use_system():
            return

        # use Python's build environment variables
        build_env = {
            key: val
            for key, val in get_config_vars().items()
            if key in ("LDFLAGS", "CFLAGS", "CC", "CCSHARED", "LDSHARED")
            and key not in os.environ
        }
        os.environ.update(build_env)

        # Ensure our temporary build directory exists
        build_temp = os.path.abspath(self.build_temp)
        try:
            os.makedirs(build_temp)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        # Ensure all of our executable files have their permission set
        '''for filename in [
            "src/libsodium/autogen.sh",
            "src/libsodium/compile",
            "src/libsodium/configure",
            "src/libsodium/depcomp",
            "src/libsodium/install-sh",
            "src/libsodium/missing",
            "src/libsodium/msvc-scripts/process.bat",
            "src/libsodium/test/default/wintest.bat",
        ]:
            os.chmod(here(filename), 0o755)'''

        if not which("make"):
            raise Exception("ERROR: The 'make' utility is missing from PATH")

        # Locate our configure script
        #configure = abshere("src/libsodium/configure")
        configure = abshere("/home/leha/Desktop/projects/library/CustomTimSort_2/sorting_code")

        # Run ./configure
        configure_flags = [
            "--disable-shared",
            "--enable-static",
            "--disable-debug",
            "--disable-dependency-tracking",
            "--with-pic",
        ]
        if platform.system() == "SunOS":
            # On Solaris, libssp doesn't link statically and causes linker
            # errors during import
            configure_flags.append("--disable-ssp")
        if os.environ.get("SODIUM_INSTALL_MINIMAL"):
            configure_flags.append("--enable-minimal")
        subprocess.check_call(
            [configure]
            + configure_flags
            + ["--prefix", os.path.abspath(self.build_clib)],
            cwd=build_temp,
        )

        make_args = os.environ.get("LIBSODIUM_MAKE_ARGS", "").split()
        # Build the library
        subprocess.check_call(["make"] + make_args, cwd=build_temp)

        # Check the build library
        subprocess.check_call(["make", "check"] + make_args, cwd=build_temp)

        # Install the built library
        subprocess.check_call(["make", "install"] + make_args, cwd=build_temp)


class build_ext(_build_ext):
    def run(self):
        if self.distribution.has_c_libraries():
            build_clib = self.get_finalized_command("build_clib")
            self.include_dirs.append(
                os.path.join(build_clib.build_clib, "include"),
            )
            self.library_dirs.insert(
                0,
                os.path.join(build_clib.build_clib, "lib64"),
            )
            self.library_dirs.insert(
                0,
                os.path.join(build_clib.build_clib, "lib"),
            )

        return _build_ext.run(self)


setup(
    name="customtimsort",
    version="0.0.63",
    description="Timsort sorting algorithm with custom minrun",
    url="https://github.com/lehatrutenb/FastTimSort",
    author="lehatr",
    author_email="lehatrutenb@gmail.com",
    package_dir={"": "sorting_code"},
    packages=[""],
    ext_package="timsort",
    cmdclass={"build_clib": build_clib, "build_ext": build_ext},
    distclass=Distribution,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
"""module1 = Extension('timsort',
                    sources = ['sorting_code/timsort.c'], library_dirs = ['/home/leha/Desktop/projects/library/CustomTimSort_2/sorting_code', '/home/leha/Desktop/projects/library/CustomTimSort_2/sorting_code/clinic'], include_dirs = ['/home/leha/Desktop/projects/library/CustomTimSort_2/sorting_code', '/home/leha/Desktop/projects/library/CustomTimSort_2/sorting_code/clinic', '/home/leha/Desktop/projects/library/CustomTimSort_2/sorting_code/cpython'])

setuptools.setup(
    name="customtimsort",
    version="0.0.62",
    author="lehatr",
    author_email="lehatrutenb@gmail.com",
    description="Timsort sorting algorithm with custom minrun",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lehatrutenb/FastTimSort",
    ext_modules = [module1],
    package_dir={'': 'sorting_code/'},
    package_data={'': ['*', 'clinic/*', 'cpython/*']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)"""