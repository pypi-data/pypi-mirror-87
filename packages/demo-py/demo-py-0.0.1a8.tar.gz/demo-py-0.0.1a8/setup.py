# -*- coding: utf8 -*-

from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
from subprocess import check_call

# https: // stackoverflow.com/questions/20288711/post-install-script-with-python-setuptools

class CustomDevelopCommand(develop):
    """Custom Develop Command"""

    def run(self):
        develop.run(self)
        print("Installing jupyter extension")
        check_call("jupyter nbextension enable --py widgetsnbextension".split())


class CustomInstallCommand(install):
    """Custom Installation Command"""

    def run(self):
        install.run(self)
        check_call("jupyter nbextension enable --py widgetsnbextension".split())


with open("README.md") as fh:
    long_description = fh.read()

setup(
    # Basic info
    name="demo-py",
    version="0.0.1",
    author='Omar Eid',
    author_email='contact.omar.eid@gmail.com',
    url='https://github.com/omars-lab/demo-py',
    description='My Personal Demo Toolbox.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],
    cmdclass={
        "develop": CustomDevelopCommand,
        'install': CustomInstallCommand,
    },
    # Packages and depencies
    packages=find_packages(),
    install_requires=[
        "ipython",
        "ipywidgets",
        "pandas",
        "matplotlib",
        "jupyter_contrib_nbextensions",
        "spacy >= 2.3.2", # eventually move this over ... tpo parsing extras
    ],
    extras_require={
        'parsing': [
            'lark-parser'
            "spacy >= 2.3.2",
        ],
        'dev': [
            # "nbconvert==5.5.0",
            "mypy",
            "pytest",
            "pytest-pep8",
            "pytest-profiling",  # https://pypi.org/project/pytest-profiling/
            "pstats-view",  # https://github.com/ssanderson/pstats-view
            "flake8",
            # 'manuel',
            # 'pytest-cov',
            # 'coverage',
            # 'mock',
        ],
        "graph": [
            "py2cytoscape",
            "pycandela",
            "pygraphviz",
        ],
        "ext": [
            "mpldatacursor",  #(https://github.com/joferkington/mpldatacursor)
            "calmap",  #(https://github.com/martijnvermaat/calmap/blob/master/calmap/__init__.py),
            "ipython[notebook]",
        ],
        "toolz": [
            "attrs",
            "pydantic",
            "toolz",  # https://toolz.readthedocs.io/en/latest/api.html
            "numpy",
            # 'jinja2',
        ]
    },
    # Data files
    package_data={},
    # Scripts
    entry_points={
        'console_scripts': [
            'python-boilerplate = python_boilerplate.__main__:main'],
    },
    # Other configurations
    zip_safe=False,
    platforms='any'
)
