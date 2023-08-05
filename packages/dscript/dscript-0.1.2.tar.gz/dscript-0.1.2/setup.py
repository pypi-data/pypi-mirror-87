#!/usr/bin/env python

from setuptools import setup, find_packages
import dscript

def clean_readme(readme):
    res = []
    with open(readme,'r') as f:
        for line in f:
            if not '.png' in line:
                res.append(line)
    return ''.join(res)

setup(name="dscript",
        version=dscript.__version__,
        description="D-SCRIPT: protein-protein interaction prediction",
        long_description=clean_readme('README.md'),
        author="Samuel Sledzieski",
        author_email="samsl@mit.edu",
        url="http://dscript.csail.mit.edu",
        license="GPLv3",
        packages=find_packages(),
        entry_points={
            "console_scripts": [
                "dscript = dscript.__main__:main",
            ],
        },
        include_package_data = True,
        install_requires=[
            "numpy",
            "scipy",
            "pandas",
            "torch",
            "matplotlib",
            "seaborn",
            "tqdm",
            "scikit-learn",
            "h5py",
        ]
    )
