"""
    Satis
"""

from setuptools import setup, find_packages
from glob import glob
from os.path import basename
from os import path as ospath

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='satis',
    version='0.0.2',
    description='Spectral Analysis for TIme Signals',
    keywords=["spectral analysis", "CFD", "signal processing"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Antoine Dauptain, Franchine Ni, Tamon Nakano, Matthieu Rossi',
    author_email='coop@cerfacs.fr',
    url='https://nitrox.cerfacs.fr/opentea/satis',
    #license=license,
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[ospath.splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "satis = satis.cli:main_cli"
        ]
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov'],
    install_requires=[
        "pandas",
        "click",
        "scipy",
        "numpy",
        "matplotlib",
    ],
)

