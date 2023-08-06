#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module."""
import inspect
#     @dataclasses.dataclass
#     class Meta:
#         """
#         Meta Class.
#
#         Examples:
#             >>> from bapy import fm, m
#             >>>
#             >>> # Cleaning
#             >>> project_env_file = m.project.path.joinpath('.env')
#             >>> project_env_file.rm()
#             >>> tmp_path = Path('/tmp')
#             >>> tmp_env_file = tmp_path.joinpath('.env')
#             >>> tmp_env_file.rm()
#             >>>
#             >>> # mod tests
#             >>> assert m.file.text.endswith('/bapy/bapy/__init__.py')
#             >>> assert m.project.name == 'bapy'
#             >>> assert m.project.path.text.endswith('/bapy')
#             >>> assert m.package.name == 'bapy'
#             >>> assert m.package.path.text.endswith('/bapy/bapy')
#             >>> assert m.prefix == 'BAPY_'
#             >>> assert m.package.name == 'bapy'
#             >>> assert m.package.name == 'bapy'
#             >>> assert m.home.is_dir()
#             >>> assert m.stream == 40
#             >>> assert str(m.log) == '<Logr bapy (DEBUG)>'
#         """
#         name: Text = None  # Init with name when project/pypi name != package/module name.
#         file: DataclassField = dataclasses.field(init=False)  # type: ignore
#         project: DataclassField = dataclasses.field(init=False)  # type: ignore
#         package: DataclassField = dataclasses.field(init=False)  # type: ignore
#         prefix: Text = None
#         home: DataclassField = dataclasses.field(init=False)  # type: ignore
#         stream: Logr.Level = None  # type: ignore
#         log: Logr = dataclasses.field(init=False)
#         distribution: Optional[importlib_metadata.Distribution] = dataclasses.field(init=False)
#         post: Callable = None  # type: ignore
#         setup: Dict = dataclasses.field(init=False)  # type: ignore
#
#         def __post_init__(self):
#             self.setup = dict(
#
#                 description=get_readme(self.project.path),
#                 name=self.project.name,
#                 python_requires='>=3.8',
#
#                 **get_requirements(self.project.path)
#             )
#             try:
#                 self.distribution = importlib_metadata.distribution(self.project.name)
#                 self.log.debug(fmt(self.distribution))
#                 self.log.debug(fmt(self.distribution.metadata))
#                 self.log.debug(fmt(self.distribution.version))
#                 self.log.debug(fmt(self.distribution.entry_points))
#                 self.log.debug(fmt(self.distribution.files))
#                 self.log.debug(fmt(self.distribution.requires))
#             except (importlib.metadata.PackageNotFoundError, AttributeError,) as exception:
#                 try:
#                     self.distribution = importlib_metadata.Distribution()
#                     self.log.error(fmt(self.file, exception))
#                 except AttributeError as exception:
#                     self.distribution = None
#                     self.log.error(fmt(self.file, exception))
#             self.log.debug(fmt(dataclasses.asdict(self)))
#
#     def get_init(path: Path) -> Text:
#         """
#         Create __init__.py for project with post install script, cli, scripts and templates dirs.
#
#         Args:
#             path: path
#
#         Returns:
#             Text:
#         """
#         readme = path / 'README.md'
#         if not readme.is_file():
#             readme.write_text(f'# {path.name.capitalize()}')
#             m.log.error(f'No README.md: {readme}')
#         try:
#             return path.read_text().splitlines()[0].split('#')[1]
#         except IndexError as exc:
#             m.log.error(f'Invalid first line README.md: {readme}. {exc}')
#             return str()
#
#     def get_readme(path: Path) -> Text:
#         """
#         Create README.md for project.
#
#         Args:
#             path: path
#
#         Returns:
#             Text:
#         """
#         readme = path / 'README.md'
#         if not readme.is_file():
#             readme.write_text(f'# {path.name.capitalize()}')
#             m.log.error(f'No README.md: {readme}')
#         try:
#             return path.read_text().splitlines()[0].split('#')[1]
#         except IndexError as exc:
#             m.log.error(f'Invalid first line README.md: {readme}')
#             return str()
#
#     def get_requirements(path: Path) -> Dict:
#         """
#         Get requirements or create requirements files for project.
#
#         Args:
#             path: path
#
#         Returns:
#             None:
#         """
#         rv = {}
#         requirements = path / 'requirements.txt'
#         if not requirements.is_file():
#             path.touch_add('requirements.txt').write_text(m.project.name if m.project.name else m.package.name)
#
#         requirements_setup = path / 'requirements_setup.txt'
#         if not requirements_setup.is_file():
#             path.touch_add('requirements_setup.txt').write_text(m.setup['setup_requires'])
#
#         requirements_test = path / 'requirements_test.txt'
#         if not requirements_test.is_file():
#             path.touch_add('requirements_test.txt').write_text(m.setup['tests_require'])
#
#         requirements_dev = path / 'requirements_dev.txt'
#         if not requirements_dev.is_file():
#             path.touch_add('requirements_dev.txt').write_text(
#                 '-r requirements.txt\n-r requirements_setup.txt\n-r requirements_test.txt')
#
#         try:  # for pip >= 10
#             # noinspection PyCompatibility
#             from pip._internal.req import parse_requirements
#         except ImportError:  # for pip <= 9.0.3
#             # noinspection PyUnresolvedReferences
#             from pip.req import parse_requirements
#         try:
#             rv = path.requirements
#         # noinspection PyUnresolvedReferences, noinspection PyCompatibility
#         except pip._internal.exceptions.RequirementsFileParseError as exc:
#             m.log.error(f'No requirements files: {exc}.')
#         return rv
#
#     def get_setup(path: Path) -> Text:
#         """
#         Create README.md for project.
#
#         Args:
#             path: path
#
#         Returns:
#             Text:
#         """
#         readme = path / 'README.md'
#         if not readme.is_file():
#             readme.write_text(f'# {path.name.capitalize()}')
#             m.log.error(f'No README.md: {readme}')
#         try:
#             return path.read_text().splitlines()[0].split('#')[1]
#         except IndexError as exc:
#             m.log.error(f'Invalid first line README.md: {readme}')
#             return str()
#
#     @app.command()
#     def project(
#             name: Text = Pathlib.cwd().parent.name if Pathlib.cwd().joinpath('setup.py').is_file() else str()) -> None:
#         """
#         Creates a new project or executes project tasks.
#
#         Args:
#             name: package name.
#
#         Returns:
#             None:
#         """
#         # noinspection PyCallByClass
#         p = Path.Name(name=name, path=Path.cwd() / name)
#         if not name:
#             p.name = rich.prompt.Prompt.ask('Enter project/package name:')
#             if not p.path.is_dir():
#                 are_you_sure = confirmation(f'Do you want to create new project/package: {p.name} in {Path.cwd()}')
#                 assert are_you_sure
#                 console.print(f'Starting installation of project/package: {p.name}')
#                 green(f'Installation finished: {p.name}', e=True)
#         if not p.path.joinpath('setup.py').is_file():
#             red(f'Directory not empty and no setup.py')
#         console.print(f'Updating project/package: {p.name}.')
#         green(f'Update finished: {p.name}', e=True)
#
#     @app.command()
#     def dist(deps: Bool = False, clean: Bool = False, test: Bool = False, bump: Bool = False, dist: Bool = False,
#                 merge: Bool = False, full: Bool = False, version: Text = Option.option(), stdout: Bool = False):
#         full: Bool = not (clean | test | bump | dist | merge)
#
#         if stdout:
#             console.print(version)
#
#     m = Meta()
#     app.help = __doc__ = m.setup['description']
#
#     @app.command()
#     def meta() -> None:
#         """
#         Package Meta.
#
#         Returns:
#             None:
#         """
#         console.print(dataclasses.asdict(m))
#

# from distutils.core import run_setup
# from setuptools import sandbox
# sandbox.run_setup('setup.py', ['clean', 'bdist_wheel'])
__all__ = [item for item in globals() if not item.startswith('_') and not inspect.ismodule(globals().get(item))]
