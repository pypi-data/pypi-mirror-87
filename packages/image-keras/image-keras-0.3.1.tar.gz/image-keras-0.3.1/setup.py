import glob
import os
import shutil
from os.path import abspath, dirname, normpath

import setuptools
import toolz
from toolz import curried

import image_keras

with open("README.md", "r") as fh:
    long_description = fh.read()

here = normpath(abspath(dirname(__file__)))


class CleanCommand(setuptools.Command):
    """Custom clean command to tidy up the project root."""

    CLEAN_FILES = "./build ./dist ./*.pyc ./*.tgz ./*.egg-info".split(" ")

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        global here

        for path_spec in self.CLEAN_FILES:
            # Make paths absolute and relative to this path
            abs_paths = glob.glob(os.path.normpath(os.path.join(here, path_spec)))
            for path in [str(p) for p in abs_paths]:
                if not path.startswith(here):
                    # Die if path in CLEAN_FILES is absolute + outside this directory
                    raise ValueError("%s is not a path inside %s" % (path, here))
                print("removing %s" % os.path.relpath(path))
                shutil.rmtree(path)


setup_requires = []

requirements = [
    ("toolz", "0.10.0"),
    ("Keras", "2.4.0"),
    ("tensorflow", "2.3.1"),
]

install_requires = toolz.pipe(
    requirements,
    curried.map(
        lambda name__min_version: name__min_version[0] + ">=" + name__min_version[1]
    ),
    list,
)

setuptools.setup(
    name="image-keras",
    cmdclass={
        "clean": CleanCommand,
    },
    version=image_keras.__version__,
    author="TenKeyLess",
    author_email="blivme84@naver.com",
    description="The fundamental package needed for common purpose with Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tenkeyless/image-keras",
    packages=setuptools.find_packages(exclude=["tests*"]),
    install_requires=install_requires,
    setup_requires=install_requires,
    license="MIT",
    keywords="common util",
    package_data={},
    zip_safe=False,
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: Unix",
    ],
    python_requires=">=3.7",
)
