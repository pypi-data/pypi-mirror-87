# -*- coding: utf-8 -*-
import setuptools


with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')




setuptools.setup(
    name='koala-publisher',
    version='0.1.3',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=install_requires,
    author="NAV IKT",
    description="Koala graph object publisher",
    license="MIT",
    project_urls={
        "Bug Tracker": "https://github.com/navikt",
        "Documentation": "https://github.com/navikt",
        "Source Code": "https://github.com/navikt",
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
)
