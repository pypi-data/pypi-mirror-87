#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The setup script."""
from setuptools import setup, find_packages

import bapy
from bapy import User, Url, path, ic
ic(path)
ic(path.project.description())
ic(path.project)
ic(path.project.requirements)
ic(path.scripts_relative)
ic(path.scripts)
setup(
    author=User.gecos,
    author_email=Url.email(),
    description=path.project.description(),
    entry_points={
        'console_scripts': [
            f'{path.repo} = {path.repo}:app',
        ],
    },
    include_package_data=True,
    install_requires=path.project.requirements['requirements'],
    name=path.repo,
    package_data={
        path.repo: [f'{path.repo}/scripts/*', f'{path.repo}/templates/*'],
    },
    packages=find_packages(),
    python_requires='>=3.8,<4',
    scripts=path.scripts_relative,
    setup_requires=path.project.requirements['requirements_setup'],
    tests_require=path.project.requirements['requirements_test'],
    url=Url.lumenbiomics(http=True, repo=path.repo).url,
    use_scm_version=False,
    version='0.4.39',
    zip_safe=False,
)
