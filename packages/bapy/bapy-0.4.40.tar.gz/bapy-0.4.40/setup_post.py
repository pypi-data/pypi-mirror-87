#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The setup script."""
import atexit
import os
import shutil
import subprocess

import sys

from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install

from bapy import path, ic, ask, console, Url, User, asdict

## Alt 1

# post = True
#
#
# def post_command(obj):
#     """
#     Post Install Command.
#
#     Args:
#         obj: post command self obj.
#     """
#     ic(asdict(obj))
#     if post and not obj.root.startswith('build/bdist.macosx'):
#         if ask('Do you want to?'):
#             console.print("Start installation!")
#     return obj
#
#
# class PostDevelopCommand(develop):
#     """Post-installation for development mode."""
#     function = post_command
#     # Pre Install.
#
#     def run(self):
#         # Post Install.
#         if self.function:
#             # noinspection PyArgumentList
#             self.function()
#         develop.run(self)
#
#
# class PostInstallCommand(install):
#     """Post-installation for installation mode."""
#     function = post_command
#     # Pre Install.
#
#     def run(self):
#         # Post Install.
#         if self.function:
#             # noinspection PyArgumentList
#             self.function()
#         install.run(self)
#
#
# PostDevelopCommand.function = PostInstallCommand.function = post_command
#
#
# setup(
#     author=User.gecos,
#     author_email=Url.email(User.name),
#     cmdclass={
#         'develop': PostDevelopCommand,
#         'install': PostInstallCommand,
#     },
#     description=path.project.description(),
#     entry_points={
#         'console_scripts': [
#             f'{path.repo} = {path.repo}:app',
#         ],
#     },
#     include_package_data=True,
#     install_requires=path.project.requirements['requirements'],
#     name=path.repo,
#     package_data={
#         path.repo: [f'{path.repo}/scripts/*', f'{path.repo}/templates/*'],
#     },
#     packages=find_packages(include=[path.repo], exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
#     python_requires='>=3.8,<4',
#     scripts=[item.relative_to(path.project).text for item in path.scripts],
#     setup_requires=path.project.requirements['requirements_setup'],
#     tests_require=path.project.requirements['requirements_test'],
#     url=Url.lumenbiomics(http=True, repo=path.repo).url,
#     use_scm_version=False,
#     version='0.1.42',
#     zip_safe=False,
# )


## Alt 2

# def post_wrapper(obj):
#     """
#     Post Install Command.
#
#     Args:
#         obj: post command self obj.
#     """
#     def post_actions():
#         ic(obj)
#         if ask('Do you want to?'):
#             console.print("Start installation!")
#     post_actions()
#     return obj
#
#
# setup = post_wrapper(
#     setup(
#         author=User.gecos,
#         author_email=Url.email(User.name),
#         description=path.project.description(),
#         entry_points={
#             'console_scripts': [
#                 f'{path.repo} = {path.repo}:app',
#             ],
#         },
#         include_package_data=True,
#         install_requires=path.project.requirements['requirements'],
#         name=path.repo,
#         package_data={
#             path.repo: [f'{path.repo}/scripts/*', f'{path.repo}/templates/*'],
#         },
#         packages=find_packages(include=[path.repo], exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
#         python_requires='>=3.8,<4',
#         scripts=[item.relative_to(path.project).text for item in path.scripts],
#         setup_requires=path.project.requirements['requirements_setup'],
#         tests_require=path.project.requirements['requirements_test'],
#         url=Url.lumenbiomics(http=True, repo=path.repo).url,
#         use_scm_version=False,
#         version='0.1.42',
#         zip_safe=False,
#     )
# )


## Alt 3

# cmd_class = {}
#
# if 'darwin' in sys.platform:
#     class PostInstall(install):
#         """ Post installation - run install_name_tool on Darwin """
#         def run(self):
#             install.run(self)
#             if ask('Do you want to?'):
#                 console.print("Start installation!")
#
#
#     cmd_class = dict(install=PostInstall)
#
# setup(
#     author=User.gecos,
#     author_email=Url.email(User.name),
#     cmdclass=cmd_class,
#     description=path.project.description(),
#     entry_points={
#         'console_scripts': [
#             f'{path.repo} = {path.repo}:app',
#         ],
#     },
#     include_package_data=True,
#     install_requires=path.project.requirements['requirements'],
#     name=path.repo,
#     package_data={
#         path.repo: [f'{path.repo}/scripts/*', f'{path.repo}/templates/*'],
#     },
#     packages=find_packages(include=[path.repo], exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
#     python_requires='>=3.8,<4',
#     scripts=[item.relative_to(path.project).text for item in path.scripts],
#     setup_requires=path.project.requirements['requirements_setup'],
#     tests_require=path.project.requirements['requirements_test'],
#     url=Url.lumenbiomics(http=True, repo=path.repo).url,
#     use_scm_version=False,
#     version='0.1.42',
#     zip_safe=False,
# )


## Alt 4


# class PostDevelopCommand(develop):
#     """Post-installation for development mode."""
#     def run(self):
#         develop.run(self)
#         subprocess.check_call("ls")
#         if ask('Do you want to?'):
#             console.print("Start installation!")
#
#
# class PostInstallCommand(install):
#     """Post-installation for installation mode."""
#     def run(self):
#         install.run(self)
#         subprocess.check_call("ls")
#         if ask('Do you want to?'):
#             console.print("Start installation!")
#
#
# setup(
#     author=User.gecos,
#     author_email=Url.email(User.name),
#     cmdclass=dict(develop=PostDevelopCommand, install=PostInstallCommand),
#     description=path.project.description(),
#     entry_points={
#         'console_scripts': [
#             f'{path.repo} = {path.repo}:app',
#         ],
#     },
#     include_package_data=True,
#     install_requires=path.project.requirements['requirements'],
#     name=path.repo,
#     package_data={
#         path.repo: [f'{path.repo}/scripts/*', f'{path.repo}/templates/*'],
#     },
#     packages=find_packages(include=[path.repo], exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
#     python_requires='>=3.8,<4',
#     scripts=[item.relative_to(path.project).text for item in path.scripts],
#     setup_requires=path.project.requirements['requirements_setup'],
#     tests_require=path.project.requirements['requirements_test'],
#     url=Url.lumenbiomics(http=True, repo=path.repo).url,
#     use_scm_version=False,
#     version='0.1.42',
#     zip_safe=False,
# )


## Alt 5
# def _post_install():
#     ic('POST INSTALL')
#     if ask('Do you want to?'):
#         console.print("Start installation!")
#
#
# class new_install(install):
#     def __init__(self, *args, **kwargs):
#         super(new_install, self).__init__(*args, **kwargs)
#         atexit.register(_post_install)
#
#
# setup(
#     author=User.gecos,
#     author_email=Url.email(User.name),
#     cmdclass={'install': new_install},
#     description=path.project.description(),
#     entry_points={
#         'console_scripts': [
#             f'{path.repo} = {path.repo}:app',
#         ],
#     },
#     include_package_data=True,
#     install_requires=path.project.requirements['requirements'],
#     name=path.repo,
#     package_data={
#         path.repo: [f'{path.repo}/scripts/*', f'{path.repo}/templates/*'],
#     },
#     packages=find_packages(include=[path.repo], exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
#     python_requires='>=3.8,<4',
#     scripts=[item.relative_to(path.project).text for item in path.scripts],
#     setup_requires=path.project.requirements['requirements_setup'],
#     tests_require=path.project.requirements['requirements_test'],
#     url=Url.lumenbiomics(http=True, repo=path.repo).url,
#     use_scm_version=False,
#     version='0.1.42',
#     zip_safe=False,
# )


# ## Alt 6
# def _post_install():
#     ic('POST INSTALL')
#     if ask('Do you want to?'):
#         console.print("Start installation!")
#
#
# setup(
#     author=User.gecos,
#     author_email=Url.email(User.name),
#     description=path.project.description(),
#     entry_points={
#         'console_scripts': [
#             f'{path.repo} = {path.repo}:app',
#         ],
#     },
#     include_package_data=True,
#     install_requires=path.project.requirements['requirements'],
#     name=path.repo,
#     package_data={
#         path.repo: [f'{path.repo}/scripts/*', f'{path.repo}/templates/*'],
#     },
#     packages=find_packages(include=[path.repo], exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
#     python_requires='>=3.8,<4',
#     scripts=[item.relative_to(path.project).text for item in path.scripts],
#     setup_requires=path.project.requirements['requirements_setup'],
#     tests_require=path.project.requirements['requirements_test'],
#     url=Url.lumenbiomics(http=True, repo=path.repo).url,
#     use_scm_version=False,
#     version='0.1.42',
#     zip_safe=False,
# )
#
# _post_install()

## Alt 7
# import atexit
# import os
# import sys
# from setuptools import setup
# from setuptools.command.install import install
#
#
# class CustomInstall(install):
#     def run(self):
#         def _post_install():
#             def find_module_path():
#                 for p in sys.path:
#                     if os.path.isdir(p) and 'jose' in os.listdir(p):
#                         return os.path.join(p, 'jose')
#             install_path = find_module_path()
#
#             # Add your post install code here
#
#             if ask('Do you want to?'):
#                 console.print("Start installation!")
#
#         atexit.register(_post_install)
#         install.run(self)
#
#
# setup(
#     author=User.gecos,
#     author_email=Url.email(User.name),
#     cmdclass={'install': CustomInstall},
#     description=path.project.description(),
#     entry_points={
#         'console_scripts': [
#             f'{path.repo} = {path.repo}:app',
#         ],
#     },
#     include_package_data=True,
#     install_requires=path.project.requirements['requirements'],
#     name=path.repo,
#     package_data={
#         path.repo: [f'{path.repo}/scripts/*', f'{path.repo}/templates/*'],
#     },
#     packages=find_packages(include=[path.repo], exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
#     python_requires='>=3.8,<4',
#     scripts=[item.relative_to(path.project).text for item in path.scripts],
#     setup_requires=path.project.requirements['requirements_setup'],
#     tests_require=path.project.requirements['requirements_test'],
#     url=Url.lumenbiomics(http=True, repo=path.repo).url,
#     use_scm_version=False,
#     version='0.1.42',
#     zip_safe=False,
# )


## Alt 8
# class InstallWrapper(install):
#   """Provides a install wrapper for WSGI applications
#   to copy additional files for Web servers to use e.g
#   static files. These were packaed using definitions
#   in MANIFEST.in and don't really belong in the
#   Python package."""
#
#   _TARGET_ROOT_PATH = "/private/tmp/"
#   _COPY_FOLDERS = ['tests', 'github']
#
#   def run(self):
#     # Run this first so the install stops in case
#     # these fail otherwise the Python package is
#     # successfully installed
#     self._copy_web_server_files()
#     # Run the standard PyPi copy
#     install.run(self)
#
#   def _copy_web_server_files(self):
#
#     # Check to see we are running as a non-privilleged user
#     if os.geteuid() == 0:
#       raise IndexError(
#         "Install should be as a non-privilleged user")
#
#     # Check to see that the required folders exists
#     # Do this first so we don't fail half way
#     for folder in self._COPY_FOLDERS:
#
#       if not os.access(folder, os.R_OK):
#         raise IOError("%s not readable from archive" %
#         folder)
#
#     # Check to see we can write to the target
#     if not os.access(self._TARGET_ROOT_PATH, os.W_OK):
#       raise IOError("%s not writeable by user" %
#       self._TARGET_ROOT_PATH)
#
#     # Clean target and copy files
#     for folder in self._COPY_FOLDERS:
#
#       target_path = os.path.join(
#         self._TARGET_ROOT_PATH, folder)
#
#       # If this exists at the target then
#       # remove it to ensure the target is clean
#       if os.path.isdir(target_path):
#         shutil.rmtree(target_path)
#
#       # Copy the files from the archive
#       shutil.copytree(folder, target_path)
#
#
# setup(
#     author=User.gecos,
#     author_email=Url.email(User.name),
#     cmdclass={'install': InstallWrapper},
#     description=path.project.description(),
#     entry_points={
#         'console_scripts': [
#             f'{path.repo} = {path.repo}:app',
#         ],
#     },
#     include_package_data=True,
#     install_requires=path.project.requirements['requirements'],
#     name=path.repo,
#     package_data={
#         path.repo: [f'{path.repo}/scripts/*', f'{path.repo}/templates/*'],
#     },
#     packages=find_packages(include=[path.repo], exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
#     python_requires='>=3.8,<4',
#     scripts=[item.relative_to(path.project).text for item in path.scripts],
#     setup_requires=path.project.requirements['requirements_setup'],
#     tests_require=path.project.requirements['requirements_test'],
#     url=Url.lumenbiomics(http=True, repo=path.repo).url,
#     use_scm_version=False,
#     version='0.1.42',
#     zip_safe=False,
# )
