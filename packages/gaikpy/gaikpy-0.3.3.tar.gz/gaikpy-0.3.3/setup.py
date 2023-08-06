from setuptools import find_packages, setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gaikpy',
    version='0.3.3',
    author='Erik Strahl',
    author_email='strahl@informatik.uni-hamburg.de',
    description='Calculates and visualises forward and (full-pose) inverse kinematic realised with a genetic algorithm (ga) for URDF models',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/knowledgetechnologyuhh/gaikpy",
    platforms='Posix; Linux; MacOS X; Windows',
    packages=find_packages(where='./src'),
    package_dir={
        '': 'src'
    },
    
    include_package_data=True,
    setup_requires=(
        'pytest-runner',
        'setuptools_scm'
    ),

    install_requires=['Sphinx', 'm2r2','sphinxcontrib-napoleon','numpy', 'scipy==1.4.1', 'sympy', 'math3d', "matplotlib","transforms3d","urdfpy","ikpy==3.0.1"],  
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Topic :: Scientific/Engineering",
    ],
    
    tests_require=(
        'pytest-cov',
    )
)