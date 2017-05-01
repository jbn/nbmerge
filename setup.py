import codecs
import os
import re

from setuptools import setup, find_packages

###############################################################################

NAME = 'nbmerge'

PACKAGES = find_packages(where=".")

META_PATH = os.path.join("nbmerge", "__init__.py")

KEYWORDS = ["jupyter", "ipython", "nbconvert"]

CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Framework :: IPython",
    "Intended Audience :: Science/Research",
    "Natural Language :: English",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

INSTALL_REQUIRES = []

###############################################################################

SELF_DIR = os.path.abspath(os.path.dirname(__file__))


def read_file_safely(*path_parts):
    with codecs.open(os.path.join(SELF_DIR, *path_parts), "rb", "utf-8") as f:
        return f.read()


META_FILE = read_file_safely(META_PATH)

META_VARS_RE = re.compile(r"^__([_a-zA-Z0-9]+)__ = ['\"]([^'\"]*)['\"]", re.M)

META_VARS = dict(META_VARS_RE.findall(META_FILE))

###############################################################################

if __name__ == "__main__":
    setup(
        name=NAME,
        entry_points={'console_scripts': ['nbmerge = nbmerge:main']},
        description=META_VARS["description"],
        license=META_VARS["license"],
        url=META_VARS["uri"],
        version=META_VARS["version"],
        author=META_VARS["author"],
        author_email=META_VARS["email"],
        maintainer=META_VARS["author"],
        maintainer_email=META_VARS["email"],
        keywords=KEYWORDS,
        long_description=read_file_safely("README.rst"),
        packages=PACKAGES,
        package_dir={"": "."},
        zip_safe=False,
        classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
    )
