# -*- coding: utf-8 -*-
import setuptools


with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')


setuptools.setup(
    name='data-catalog-dcat-validator',
    version='0.0.6',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    python_requires='>=3.6',
    install_requires=install_requires,
    author="NAV IKT",
    description="Validator for value types",
    license="MIT",
    project_urls={
        "Bug Tracker": "https://github.com/navikt/data-catalog-dcat-validator",
        "Documentation": "https://github.com/navikt/data-catalog-dcat-validator",
        "Source Code": "https://github.com/navikt/data-catalog-dcat-validator",
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
)