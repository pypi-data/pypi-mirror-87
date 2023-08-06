#!/usr/bin/env python
# -*- coding: utf-8 -*-

import moustache_fusion
import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='Moustache-fusion.beta',
    version=moustache_fusion.__version__,
    python_requires='>=3',
    packages=setuptools.find_packages(),
    author='Libriciel SCOP',
    author_email='hackathon@libriciel.coop',
    description='Module post-Moustache pour fusion d\'annexes PDF dans PDF principal',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'flask>=1.1,<1.2',
        'python-magic>=0.4,<0.5',
        'PyPDF2>=1.26,<1.27',
        'reportlab>=3.5,<3.6'
    ],
    extras_require={
        'dev': [
            'coverage>=5.3,<5.4',
            'flake8>=3.8,<3.9',
            'pdf2image>=1.14,<1.15',
            'pixelmatch>=0.2,<0.3',
            'pytest>=6.1,<6.2'
        ]
    },
    include_package_data=True,
    url='https://gitlab.libriciel.fr/outils/skittlespy/',
    entry_points={
        'console_scripts': [
            'moustache_fusion = moustache_fusion:launch'
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6'
    ],
    license='CeCILL-2.1',
)
