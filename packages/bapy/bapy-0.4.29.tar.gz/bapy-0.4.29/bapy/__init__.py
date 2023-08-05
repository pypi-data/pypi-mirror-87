#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
"""Lib package for Bapy."""
from __future__ import annotations

import ast
import asyncio
import asyncio.events
import asyncio.runners
import collections
import concurrent.futures
import configparser
import dataclasses
import datetime
import enum
import errno
import functools
import grp
import importlib.metadata
import inspect
import ipaddress
import json
import logging
import logging.handlers
import mailbox
import os
import pathlib
import pkgutil
import platform
import pwd
import shlex
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import tracemalloc
import types
import typing
import urllib.error
import urllib.request
import uuid
from typing import (
    Any,
    Awaitable,
    Dict,
    Final,
    Iterable,
    List,
    Literal,
    Optional,
    OrderedDict,
    Set,
    Text,
    Tuple,
    Type,
    Union,
)

import box
import click
import click_completion
import colorlog
import devtools
import distro
import environs
import furl
import git
import icecream
import importlib_metadata
import inflect
import jinja2
import motor.motor_asyncio
import psutil
import pymongo
import pymongo.errors
import requests
import rich
import rich.logging
import ruamel
import setuptools.command.develop
import setuptools.command.install
import shell_proc
import shellingham
import sty
import typer
import urllib3
import verboselogs
from asgiref.sync import sync_to_async
from typer.models import AnyType

app = typer.Typer()
console = rich.console.Console()
cprint = console.print
dbg = devtools.debug
fm = icecream.IceCreamDebugger(prefix=str()).format
fmt = icecream.IceCreamDebugger(prefix=str(), includeContext=True).format
ic = icecream.IceCreamDebugger(prefix=str())
icc = icecream.IceCreamDebugger(prefix=str(), includeContext=True)
os.environ["PYTHONWARNINGS"] = "ignore"

post = True
urllib3.disable_warnings()

# <editor-fold desc="Typing">
Absent = object
absent = object()
Bool = bool
Class = type  # type: ignore
CodeType = types.CodeType
DataclassField = dataclasses.Field
FrameInfo = inspect.FrameInfo
FrameType = types.FrameType
GenericAlias = typing._GenericAlias
Int = int
Logger = logging.Logger
MongoClient = pymongo.MongoClient
MotorClient = motor.motor_asyncio.AsyncIOMotorClient
Pathlib = pathlib.Path
PathLike = os.PathLike

DictAnyBool = Dict[Any, Bool]
DictAnyInt = Dict[Any, Int]
DictAnyText = Dict[Any, Text]
DictTextAny = Dict[Text, Any]
DictTextBool = Dict[Text, Bool]
DictTextInt = Dict[Text, Int]
DictTextText = Dict[Text, Text]
DictTextTextAny = Dict[Text, DictTextAny]

ListInt = List[Int]
ListText = List[Text]

SetInt = Set[Int]
SetText = Set[Text]

TupleAnyDict = Tuple[Any, Dict]
TupleBoolTextText = Tuple[Bool, Text, Text]
TupleInt = Tuple[Int]
TupleIntTextText = Tuple[Text, Text, Int]
TupleText = Tuple[Text]
TupleTextTextInt = Tuple[Text, Text, Int]

UnionAnyTuple = Union[Any, Tuple]  # type: ignore
UnionBoolText = Union[Bool, Text]
UnionDictAny = Union[Dict, Any]
UnionDictList = Union[Dict, List]
UnionDictListSetTextTuple = Union[Dict, List, Set, Text, Tuple]  # type: ignore
UnionDictListTextTuple = Union[Dict, List, Text, Tuple]  # type: ignore
UnionDictListTuple = Union[Dict, List, Tuple]  # type: ignore
UnionListAny = Union[List, Any]
UnionListSetTuple = Union[List, Set, Tuple]  # type: ignore
UnionListText = Union[List, Text]
UnionListTextTuple = Union[List, Text, Tuple]  # type: ignore
UnionListTuple = Union[List, Tuple]  # type: ignore

UnionMongo = Union[MongoClient, MotorClient]
UnionParser = Union[configparser.RawConfigParser, configparser.ConfigParser]
UnionTextBool = Union[Text, Bool]
UnionTextDataclassField = Union[Text, DataclassField]
UnionTextInt = Union[Text, Int]
UnionTextList = Union[Text, List]
UnionTextListDict = Union[Text, List, Dict]
UnionTextTuple = Union[Text, Tuple]

OptionalAny = Optional[Any]
OptionalBool = Optional[Bool]
OptionalBoolText = Optional[UnionBoolText]
OptionalCodeType = Optional[CodeType]
OptionalDict = Optional[Dict]
OptionalDictTextAny = Optional[DictTextAny]
OptionalDictTextText = Optional[DictTextText]
OptionalFrameType = Optional[FrameType]
OptionalFrameInfo = Optional[FrameInfo]
OptionalInt = Optional[Int]
OptionalList = Optional[List]
OptionalListText = Optional[ListText]
OptionalLogger = Optional[Logger]  # type: ignore
OptionalText = Optional[Text]
OptionalTuple = Optional[Tuple]  # type: ignore
OptionalTupleInt = Optional[TupleInt]

FinalAny = Final[Any]
FinalBool = Final[Bool]
FinalDict = Final[Dict]
FinalInt = Final[Int]
FinalText = Final[Text]
FinalTuple = Final[Tuple]
FinalTupleInt = Final[TupleInt]

IPaddress = Union[ipaddress.IPv4Address, ipaddress.IPv6Address]
IPLike = Union[Text, ipaddress.IPv4Address, ipaddress.IPv6Address]
IPv4Like = Union[ipaddress.IPv4Address, Text]
IPv6Like = Union[ipaddress.IPv6Address, Text]
OptionalIPaddress = Optional[IPaddress]
OptionalIPLike = Optional[IPLike]
OptionalIPv4Like = Optional[IPv4Like]
OptionalIPv6Like = Optional[IPv6Like]
# </editor-fold>


# <editor-fold desc="Constants & Data">
ALL_PORTS = range(0, 65535)
IP_VERSION = {4: dict(af=socket.AF_INET), 6: dict(af=socket.AF_INET6)}

LOCALHOST = '127.0.0.1'

Proto = collections.namedtuple('Protos', 'tcp udp')
PROTO_NAME = Proto(*Proto._fields)
PROTO_SOCK = Proto(socket.SOCK_STREAM, socket.SOCK_DGRAM)

ProtoStatus = collections.namedtuple('ProtoStatus', 'ip port proto open')


@dataclasses.dataclass
class Sem:
    atlas: Int = 499
    db: Int = 500
    io: Int = 500
    max: Int = 5000
    nmap: Int = 500
    os: Int = 500
    ping: Int = 750
    socket: Int = 500
    ssh: Int = 500

    def __post_init__(self):
        for item in self.defaults():
            setattr(self, item, asyncio.Semaphore(getattr(self, item)))

    @classmethod
    def defaults(cls) -> Dict:
        return {item.name: item.default for item in dataclasses.fields(cls)}

# </editor-fold>


# <editor-fold desc="Exceptions">
class BapyException(Exception):
    """Custom base class for all Repo exception types."""


class BapyFrameBackBack(BapyException):
    def __init__(self, message):
        self.message = message


class BapyGitDirectoryIsDirty(BapyException):
    def __init__(self, message):
        self.message = message


class BapyInvalidIP(BapyException):
    def __init__(self, ip):
        self.ip = ip
        self.message = f'Invalid IP: {self.ip}'


# </editor-fold>


# <editor-fold desc="Echo">
@app.command()
def black(msg: Text, bold: Bool = False, underline: Bool = False,
          blink: Bool = False, err: Bool = False, e: Bool = False) -> None:
    """
    Black.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='black', err=err)
    if e:
        sys.exit(0)


@app.command()
def red(msg: Text, bold: Bool = False, underline: Bool = False,
        blink: Bool = False, err: Bool = True, e: Bool = True) -> None:
    """
    Red.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='red', err=err)
    if e:
        sys.exit(1)


@app.command()
def green(msg: Text, bold: Bool = False, underline: Bool = False,
          blink: Bool = False, err: Bool = False, e: Bool = False) -> None:
    """
    Green.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='green', err=err)
    if e:
        sys.exit(0)


@app.command()
def yellow(msg: Text, bold: Bool = False, underline: Bool = False,
           blink: Bool = False, err: Bool = True, e: Bool = False) -> None:
    """
    Yellow.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='yellow', err=err)
    if e:
        sys.exit(0)


@app.command()
def blue(msg: Text, bold: Bool = False, underline: Bool = False,
         blink: Bool = False, err: Bool = False, e: Bool = False) -> None:
    """
    Blue.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='blue', err=err)
    if e:
        sys.exit(0)


@app.command()
def magenta(msg: Text, bold: Bool = False, underline: Bool = False,
            blink: Bool = False, err: Bool = False, e: Bool = False) -> None:
    """
    Magenta.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='magenta', err=err)
    if e:
        sys.exit(0)


@app.command()
def cyan(msg: Text, bold: Bool = False, underline: Bool = False,
         blink: Bool = False, err: Bool = False, e: Bool = False) -> None:
    """
    Cyan.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='cyan', err=err)
    if e:
        sys.exit(0)


@app.command()
def white(msg: Text, bold: Bool = False, underline: Bool = False,
          blink: Bool = False, err: Bool = False, e: Bool = False) -> None:
    """
    White.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='white', err=err)
    if e:
        sys.exit(0)


@app.command()
def bblack(msg: Text, bold: Bool = False, underline: Bool = False,
           blink: Bool = False, err: Bool = False, e: Bool = False) -> None:
    """
    Black.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='bright_black', err=err)
    if e:
        sys.exit(0)


@app.command()
def bred(msg: Text, bold: Bool = False, underline: Bool = False,
         blink: Bool = False, err: Bool = True, e: Bool = True) -> None:
    """
    Bred.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='bright_red', err=err)
    if e:
        sys.exit(1)


@app.command()
def bgreen(msg: Text, bold: Bool = False, underline: Bool = False,
           blink: Bool = False, err: Bool = False, e: Bool = False) -> None:
    """
    Bgreen.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='bright_green', err=err)
    if e:
        sys.exit(0)


@app.command()
def byellow(msg: Text, bold: Bool = False, underline: Bool = False,
            blink: Bool = False, err: Bool = True, e: Bool = False) -> None:
    """
    Byellow.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='bright_yellow', err=err)
    if e:
        sys.exit(0)


@app.command()
def bblue(msg: Text, bold: Bool = False, underline: Bool = False,
          blink: Bool = False, err: Bool = False, e: Bool = False) -> None:
    """
    Bblue.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='bright_blue', err=err)
    if e:
        sys.exit(0)


@app.command()
def bmagenta(msg: Text, bold: Bool = False, underline: Bool = False,
             blink: Bool = False, err: Bool = False, e: Bool = False) -> None:
    """
    Bmagenta.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='bright_magenta', err=err)
    if e:
        sys.exit(0)


@app.command()
def bcyan(msg: Text, bold: Bool = False, underline: Bool = False,
          blink: Bool = False, err: Bool = False, e: Bool = False) -> None:
    """
    Bcyan.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='bright_cyan', err=err)
    if e:
        sys.exit(0)


@app.command()
def bwhite(msg: Text, bold: Bool = False, underline: Bool = False,
           blink: Bool = False, err: Bool = False, e: Bool = False) -> None:
    """
    Bwhite.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='bright_white', err=err)
    if e:
        sys.exit(0)


@app.command()
def reset(msg: Text = str(), bold: Bool = False, underline: Bool = False, blink: Bool = False, err: Bool = False,
          e: Bool = False) -> None:
    """
    Reset.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='reset', err=err)
    if e:
        sys.exit(0)


# </editor-fold>


# <editor-fold desc="Functions">
def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


async def acprint(*args, **kwargs):
    await executor(cprint, *args, **kwargs)


def aiocaller():
    caller = inspect.currentframe().f_back.f_back
    func_name = inspect.getframeinfo(caller)[2]
    f = caller.f_locals.get(func_name, caller.f_globals.get(func_name))
    if any([inspect.iscoroutinefunction(f), inspect.isgeneratorfunction(f), inspect.iscoroutine(f),
            inspect.isawaitable(f), inspect.isasyncgenfunction(f), inspect.isasyncgen(f)]):
        return True
    else:
        return False


async def aiocmd(command: UnionTextList, onlyout: Bool = True,
                 onlyrc: Bool = False, decode: Bool = True, utf8: Bool = False) -> Union[TupleTextTextInt, Text, Int]:
    """
    Asyncio run cmd.

    Args:
        command: command.
        onlyout: return only stdout.
        onlyrc: return only rc.
        decode: decode and strip output.
        utf8: utf8 decode.

    Returns:
        TupleIntTextText: [stdout, stderr, proc.returncode].
    """
    proc = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE,
                                                 stderr=asyncio.subprocess.PIPE, loop=asyncio.get_running_loop())
    stdout, stderr = await proc.communicate()
    if decode:
        stdout = stdout.decode().rstrip('.\n')
        stderr = stderr.decode().rstrip('.\n')
    elif utf8:
        stdout = stdout.decode('utf8').strip()
        stderr = stderr.decode('utf8').strip()

    if onlyrc:
        return proc.returncode
    elif onlyout:
        return stdout
    else:
        return stdout, stderr, proc.returncode


def aioloop():
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        return None


def aiorun(call, *, debug=False):
    if loop := aioloop():
        if not asyncio.coroutines.iscoroutine(call):
            raise ValueError("a coroutine was expected, got {!r}".format(call))

        try:
            loop.set_debug(debug)
            return loop.run_until_complete(call)
        finally:
            try:
                asyncio.runners._cancel_all_tasks(loop)
                loop.run_until_complete(loop.shutdown_asyncgens())
            finally:
                asyncio.events.set_event_loop(None)
                loop.close()
    else:
        return asyncio.run(call)


def aiowrap(func):
    @functools.wraps(func)
    async def aio_run(*args, **kwargs):
        ic('aio: wrap')
        return await loop.run_in_executor(None, functools.partial(func, *args, **kwargs))

    @functools.wraps(func)
    def run(*args, **kwargs):
        ic('no aio: wrap')
        return func(*args, **kwargs)

    ic(aioloop())

    if loop := aioloop():
        ic('aio')
        return aio_run
    ic('no aio')
    return run


def app_version_callback(value: bool):
    if value:
        typer.echo(f"{importlib.metadata.version(path.repo)}")
        raise typer.Exit()


@app.command()
def appdir(stdout: Bool = False) -> None:
    """
    CLI/APP dir.

    Args:
        stdout: stdout.

    Returns:
        None:
    """
    if stdout:
        green(typer.get_app_dir(Path(__file__).parent))
    else:
        return green(typer.get_app_dir(Path(__file__).parent))


def asdict(obj: Any) -> Dict:
    """
    Instance/Object dict and/or properties (True for classes, False for instances).

    Args:
        obj: obj

    Returns:
        Dict:
    """
    rv = dict()

    rv_exclude, none_exclude = asdict_exclude(obj)
    for item in dir(obj):
        if not item.startswith('__') and item not in rv_exclude:
            if (value := getattr(obj, item, None)) or (value is None and (
                    item not in Asdict.__none__ and item not in none_exclude)):
                if inspect.isroutine(value) is False:
                    if isinstance(value, property):
                        if not inspect.isclass(obj):
                            rv[item] = value
                    else:
                        rv[item] = value
    return rv


def asdict_exclude(obj: Any) -> Tuple[Set, Set]:
    """
    Instance/Object __exclude__ mro.

    Args:
        obj: obj

    Returns:
        Set:
    """
    cls = inspect.isclass(obj)
    mro = obj.__mro__ if cls and hasattr(obj, '__mro__') else obj.__class__.__mro__ \
        if hasattr(obj.__class__, '__mro__') else tuple()
    rv_exclude = set()
    none_exclude = set()
    for item in mro:
        if value := getattr(item, '__exclude__', False):
            for exclude in value:
                rv_exclude.add(exclude)
        if value := getattr(item, '__none__', False):
            for exclude in value:
                none_exclude.add(exclude)

    for item in Asdict.__exclude__:
        rv_exclude.add(item)
    return rv_exclude, none_exclude


@app.command()
def ask(msg: Text) -> Bool:
    """
    Ask Yes or No.

    Args:
        msg: text message.

    Returns:
        Bool:
    """
    from rich.prompt import Prompt
    if Prompt.ask(msg, choices=['Yes', 'No'], default='Yes') == 'Yes':
        return True
    return False


@app.command()
def base64auth(username: Text, password: Text, stdout: Bool = False) -> Text:
    """
    Generates a base64 auth for usage with .npmrc.

    Args:
        username: user name.
        password: user password.
        stdout: stdout.

    Returns:
        Text: openssl base64.
    """
    rv = os.popen(f'echo -n "{username}:{password}" | openssl base64').read().splitlines()[0]
    if stdout:
        console.print(rv)
    return rv


def click_custom_startswith(string: Text, incomplete: Text) -> Bool:
    """
    A custom completion matching that supports case insensitive matching.

    Args:
        string: string
        incomplete: incomplete

    Returns:
        Bool:
    """
    case_insensitive_completion: Text = '_CLICK_COMPLETION_COMMAND_CASE_INSENSITIVE_COMPLETE'

    if os.environ.get(case_insensitive_completion):
        string = string.lower()
        incomplete = incomplete.lower()
    return string.startswith(incomplete)


click_completion.core.startswith = click_custom_startswith


def cmd(command: Iterable, onlyout: Bool = False, onlyrc: Bool = False, shell: Bool = True, sysexec: Bool = False,
        lines: Bool = True) -> Union[TupleTextTextInt, Int]:
    """
    Runs a cmd.

    Examples:
        >>> cmd('ls a')
        ([], ['ls: a: No such file or directory'], 1)
        >>> assert 'Requirement already satisfied' in cmd('pip install pip', sysexec=True)[0][0]
        >>> cmd('ls a', shell=False, lines=False)  # Extra '\' added to avoid docstring error.
        ('', 'ls: a: No such file or directory\\n', 1)
        >>> cmd('echo a', onlyout=True, lines=False)  # Extra '\' added to avoid docstring error.
        'a\\n'

    Args:
        command: command.
        onlyout: returns only stdout.
        onlyrc: return only rc.
        shell: expands shell variables and one line (shell True expands variables in shell).
        sysexec: runs with sys executable.
        lines: split lines so ``\\n`` is removed from all lines (extra '\' added to avoid docstring error).

    Returns:
        TupleTextTextInt:
    """
    if sysexec:
        command = f'{sys.executable} -m {command}'
    elif not shell:
        command = shlex.split(command)

    if lines:
        text = False
    else:
        text = True

    proc = subprocess.run(command, shell=shell, capture_output=True, text=text)

    def rv(out=True):
        if out:
            if lines:
                return proc.stdout.decode("utf-8").splitlines()
            else:
                # return proc.stdout.decode("utf-8").rstrip('.\n')
                return proc.stdout
        else:
            if lines:
                return proc.stderr.decode("utf-8").splitlines()
            else:
                # return proc.stderr.decode("utf-8").rstrip('.\n')
                return proc.stderr

    if onlyrc:
        return proc.returncode
    elif onlyout:
        return rv()
    else:
        return rv(), rv(False), proc.returncode


def cmd_completion(cls, append, case_insensitive, p):
    def provide_default():
        if os.name == 'posix':
            return os.path.basename(os.environ['SHELL'])
        elif os.name == 'nt':
            return os.path.basename(os.environ['COMSPEC'])
        raise NotImplementedError(f'OS {os.name!r} support not available')

    try:
        shell = shellingham.detect_shell()
    except shellingham.ShellDetectionFailure:
        shell = provide_default()

    extra_env = {cls.case_insensitive_completion: 'ON OFF'} if case_insensitive else {}
    shell, p = click_completion.core.install(shell=shell, path=p, append=append, extra_env=extra_env)
    click.echo(f'{shell} completion installed in {p}')


@app.command()
def confirmation(msg: Text) -> Bool:
    """
    Ask for Yes/no and confirmation.

    Args:
        msg: text message.

    Returns:
        Bool:
    """
    if ask(msg):
        are_you_sure = rich.prompt.Confirm.ask(f'Are you sure?')
        assert are_you_sure
        return True
    return False


def context(variables=str()):
    locals_context_dict = sys._getframe(2).f_locals
    if locals_context_dict.get('l'):
        del locals_context_dict['l']

    if locals_context_dict.get('cls'):
        del locals_context_dict['cls']
    aiotask_context_dict = {}
    try:
        # noinspection PyUnresolvedReferences
        aiotask_context_dict = {key: asyncio.current_task().get(key) for key in asyncio.current_task()}
    except (RuntimeError, AttributeError, NameError,):
        pass

    context_dict = {**locals_context_dict, **aiotask_context_dict, **sys._getframe(2).f_globals}
    context_dict_clean = {key: context_dict.get(key) for key in context_dict if not_(key)
                          and is_data(context_dict.get(key))}
    if variables:
        try:
            msg_dict = {var: str() for var in variables.split() if not context_dict_clean.get(var, None)}
            variables_dict = {var: eval(var, context_dict_clean, msg_dict) for var in variables.split()
                              if not_(var) and is_data(eval(var, context_dict, msg_dict))}
        except (AttributeError, NameError, KeyError):
            pass
        else:
            context_dict_clean = variables_dict
    else:
        if context_dict_clean.get('self', None):
            add = {'self': context_dict_clean['self']}
            context_dict_clean = {**context_dict_clean, **add}
    final = {**context_dict_clean}
    msg = ", ".join("{}: {}".format(key, value) for key, value in {
        var.replace("\\", ""): vars(final.get(var))
        if getattr(final.get(var), '__dict__', None) and var[:1] != '_'
        else final.get(var) for var in list(final)
    }.items() if not_(key) and is_data(key))
    # exception = sys.exc_info()[1]
    # if exception:
    #     exception.args = ('{} [{}]'.format(exception.args[0], msg) if exception.args else msg,) + exception.args[1:]
    return msg


def dict_exclude(data: Dict, exclude: UnionListTuple = None) -> OptionalDict:
    """
    Dict with vars in `exclude`. Default: private vars.

    Args:
        data: input dict.
        exclude: vars to exclude.

    Example:
        >>> import inspect
        >>>
        >>> new_dict = dict_include(inspect.stack(2)[0].frame.f_locals, include=('__annotations__', ))

    Returns:
        OptionalDict:
    """
    if exclude:
        return {key: value for key, value in data.items() if key != exclude}
    else:
        return {key: value for key, value in data.items() if key[:1] != '_'}


def dict_include(data: Dict, include: UnionListTuple = None) -> OptionalDict:
    """
    Dict with vars in `include`. Default: ``(str, int, tuple, set, list, bool, float, dict)``.

    Example:
        >>> import inspect
        >>>
        >>> new_dict = dict_include(inspect.stack(2)[0].frame.f_globals)

    Args:
        data: input dict.
        include: vars to include.

    Returns:
        OptionalDict:
    """
    if include:
        return {key: value for key, value in data.items() if key in include}
    else:
        return {key: value for key, value in data.items()
                if key[:1] != '_' and type(value) in (str, int, tuple, set, list, bool, float, dict)}


def dict_sort(name: Dict, sort: Bool = True) -> Dict:
    """
    Order a dict based on keys.

    Args:
        name: dict to be ordered.
        sort: default and only option True.

    Returns:
        Dict:
    """
    if sort:
        return {key: name[key] for key in sorted(name)}


def distribution(package: Text = str(), stdout: Bool = False) -> importlib.metadata.Distribution:
    """
    Package/Project Distribution Information.

    Args:
        package: package
        stdout: stdout

    Returns:
        importlib_metadata.Distribution:
    """
    try:
        rv = importlib.metadata.distribution(package if package else path.repo)
        if stdout:
            console.print(rv)
        return rv
    except importlib.metadata.PackageNotFoundError as exc:
        path.log.debug(fm(exc))


def dump_ansible_yaml(p: Any, data: Dict):
    """
    Dump yaml with ansible format.

    Args:
        p: path
        data: data
    """
    yaml = ruamel.yaml.YAML()
    yaml.indent(mapping=2, sequence=2, offset=2)
    # yaml.compact(seq_seq=False, seq_map=False)
    yaml.dump(data, p.open('w+'))


def flat_list(l: Iterable) -> Union[List, Iterable]:
    """
    Flattens an Iterable

    Args:
        l: iterable

    Returns:
        List:
    """
    flat = []
    _ = [flat.extend(item) if isinstance(item, list) else flat.append(item) for item in l if item]
    return list(set(flat))


def force_async(fn):
    """
    Turns a sync function to async function using threads.
    """
    from concurrent.futures import ThreadPoolExecutor
    import asyncio
    pool = ThreadPoolExecutor()

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        future = pool.submit(fn, *args, **kwargs)
        return asyncio.wrap_future(future)  # make it awaitable

    return wrapper


def force_sync(fn):
    """
    Turn an async function to sync function.
    """
    import asyncio

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        res = fn(*args, **kwargs)
        if asyncio.iscoroutine(res):
            return asyncio.get_event_loop().run_until_complete(res)
        return res

    return wrapper


def get_choice_class(data: Union[Iterable, GenericAlias], case_sensitive: Bool = True) -> click.Choice:
    """
    :class:`click.Echo` from different data sources.

    Examples:
        >>> choice = get_choice_class(Literal['a'])
        >>> choice
        Choice('['a']')
        >>> choice = get_choice_class(choice.choices)
        >>> choice
        Choice('['a']')
        >>> choice = get_choice_class(''.join(choice.choices))
        >>> choice
        Choice('['a']')

    Args:
        data: data
        case_sensitive: case_sensitive

    Returns:
        click.Choice:
    """
    if isinstance(data, GenericAlias):
        data = data.__args__
    elif isinstance(data, str):
        data = data.split()
    return click.Choice(data, case_sensitive)


def gen_key(home: AnyType = None, private: AnyType = None, public: AnyType = None, text: AnyType = None,
            email: AnyType = None):
    """
    Gpg key generation and exporting public and private keys.

    Args:
        home: gpg home path
        private: gpg private dest path
        public: gpg public dest path
        text: render template
        email: author email
    """
    home = shlex.quote(str(home))
    private = shlex.quote(str(private))
    public = shlex.quote(str(public))
    text = shlex.quote(str(text))
    email = shlex.quote(email)

    with shell_proc.Shell(stdout=sys.stdout, stderr=sys.stderr, blocking=False) as sh:
        sh(
            f'mkdir -p {home}; chmod go-rwx {home}; '
            f'rm -rf {home}/*; '
            f'rm -rf {private} {public}; '
            f'gpg --homedir {home} --batch --gen-key {text}; '
            f'gpg --homedir {home} --export --armor --output {public} {email};'
            f'gpg --homedir {home} --export-secret-key --armor {email} > {private}; '
            f'sudo rm -rf {home}/S.gpg-agent*;'
        )

    time.sleep(1)
    print('1 Second has passed', 'Running:', sh.current_command)
    time.sleep(1)
    print('2 Seconds have passed', 'Running:', sh.current_command)
    time.sleep(1)
    print('3 Seconds have passed', 'Running:', sh.current_command)

    sh.wait()

    table = '|{:_<20}|{:_<20}|{:_<20}|{:_<50}|'
    print(table.format(str(), str(), str(), str()).replace('|', '_'))
    print(table.format("Exit Code", "Has Error", "Has Output", "Command").replace('_', ' '))
    print(table.format(str(), str(), str(), str()))
    for item in sh.history:
        print(table.format(item.exit_code, item.has_error(), item.has_output(), item.cmd).replace('_', ' '))
    print(table.format(str(), str(), str(), str()).replace('|', '_'))


def get_key(data: Dict, value: Any) -> OptionalAny:
    """
    Get Dict Key from Value.

    Args:
        data: data
        value: value

    Returns:
        OptionalAny:
    """
    for key, val in data.items():
        if val == value:
            return key


def get_vars_docs(fname: Text) -> Dict:
    """
    Read the module referenced in fname (often <module>.__file__) and return a
    dict with global variables, their value and the "docstring" that follows
    the definition of the variable.

    Args:
        fname: fname

    Returns:
        Dict:
    """
    file = os.path.splitext(fname)[0] + '.lib'  # convert .pyc to .lib
    with open(file, 'r') as f:
        fstr = f.read()
    rv = {}
    key = None
    for node in ast.walk(ast.parse(fstr)):
        if isinstance(node, ast.Assign):
            key = node.targets[0].id
            rv[key] = [node.value.id, str()]
            continue
        elif isinstance(node, ast.Expr) and key:
            rv[key][1] = node.value.s.strip()
        key = None
    return rv


@app.command()
def info(dist: Text = str(), executable: Bool = False, linux: Bool = False,
         machine: Bool = False, project: Bool = False, py: Bool = False, user: Bool = False) -> None:
    """
    Command to provide info.

    Args:
        dist: importlib distribution.
        executable: executables in server.
        linux: linux distribution.
        machine: machine information.
        project: package and path information.
        py: python information.
        user: user data.
    """
    if not (bool(dist) | executable | linux | machine | project | py | user):
        executable = linux = machine = project = py = user = True
        dist = dist if dist else path.repo

    if dist:
        d = distribution(dist)
        console.print('[bold blue]Distribution: ', asdict(d), '\n', '[bold blue]Metadata: ', metadata(dist), str())
    if executable:
        console.print('[bold blue]Executable: ', dataclasses.asdict(Executable()), str())
    if linux:
        console.print('[bold blue]Distro: ', dataclasses.asdict(Distro()), str())
    if machine:
        console.print('[bold blue]Machine: ', dataclasses.asdict(Machine()), str())
    if project:
        console.print('[bold blue]Path: ', path.asdict, str())
    if py:
        console.print('[bold blue]Py: ', dataclasses.asdict(Py()), str())
    if user:
        console.print('[bold blue]User: ', dataclasses.asdict(User()), str())


def is_data(obj) -> Bool:
    def exclude():
        for module in [typing, ]:
            if module is inspect.getmodule(obj):
                return True
        if 'wrapper' in str(type(obj)) or ('__' in str(obj) and '__main__' not in str(obj)):
            return True
        return False

    return not \
        inspect.isabstract(obj) | inspect.isroutine(obj) | inspect.iscode(obj) | inspect.isframe(obj) | \
        inspect.istraceback(obj) | inspect.isawaitable(obj) | inspect.iscoroutine(obj) | inspect.isgenerator(obj) | \
        inspect.isasyncgen(obj) | inspect.isasyncgenfunction(obj) | inspect.iscoroutinefunction(obj) | \
        inspect.isgeneratorfunction(obj) | inspect.isgetsetdescriptor(obj) | inspect.isdatadescriptor(obj) | \
        inspect.ismodule(obj) | inspect.isclass(obj) | exclude()


@app.command()
def is_pip(stdout: Bool = False) -> Bool:
    """
    Checks if pip is installed.

    Args:
        stdout: stdout.

    Returns:
        Bool
    """
    try:
        # noinspection PyCompatibility
        import pip
        if stdout:
            green(str(True))
        return True
    except ModuleNotFoundError:
        if stdout:
            red(str(False))
        return False


def iter_split(data: Iterable, ret: Bool = False) -> Any:
    """
    Item str().split() and Iterables.

    Args:
        data: data
        ret: return list if True or yield.

    Raises:
        TypeError: TypeError

    Yields:
        Any:
    """
    if isinstance(data, Iterable):
        if isinstance(data, str):
            data = data.split() if ' ' in data else data
        if ret:
            return data
        for item in data:
            yield item
    else:
        raise TypeError(f'data: {data} must be iterable.')


def load_modules(p) -> None:
    """
    Load Modules of Package.

    Args:
        p: package.
    """
    p = p if p else path.repo
    p._modules = []

    pkgname = p.__name__
    pkgpath = Path(p.__file__).parent

    for mod in pkgutil.iter_modules([pkgpath]):
        modulename = pkgname + '.' + mod[1]
        __import__(modulename, locals(), globals())
        module = sys.modules[modulename]

        module._package = p
        # module._packageName = pkgname

        p._modules.append(module)
        if Path(module.__file__).parent == pkgpath:
            module._isPackage = False
        else:
            module._isPackage = True
            # noinspection PyTypeChecker,PydanticTypeChecker
            load_modules(module)


# noinspection PyUnusedLocal
@app.callback()
def main(version: bool = typer.Option(None, "--version", callback=app_version_callback, is_eager=True)):
    # Do other global stuff, handle other global options here
    return


def mapped_commands(command_map: Dict) -> Any:
    """
    Commands mapping.

    Args:
        command_map: command_map

    Returns:
        Any:
    """

    class CommandGroup(click.Group):
        def get_command(self, ctx, cmd_name):
            for real_command, aliases in command_map.items():
                if cmd_name in aliases:
                    return click.Group.get_command(self, ctx, real_command)
            return None

        def list_commands(self, ctx):
            return [a for b in command_map.values() for a in b]

    return CommandGroup


def metadata(package: Text = str(), stdout: Bool = False) -> mailbox.Message:
    """
    Package/Project Metadata Information.

    Args:
        package: package
        stdout: stdout
    Returns:
        Dict:
    """
    try:
        rv = importlib.metadata.metadata(package if package else path.repo)
        if stdout:
            console.print(rv)
        return rv
    except importlib.metadata.PackageNotFoundError as exc:
        path.log.debug(fm(exc))


def mod_name(mod):
    return mod.__name__.rpartition('.')[-1]


def move_to_key(mydict: Dict, new_key: Text, keys_to_move: UnionListTuple):
    if set(mydict.keys()).intersection(keys_to_move):
        mydict[new_key] = {}
        for k in keys_to_move:
            mydict[new_key][k] = mydict[k]
            del mydict[k]


def namedtuple(typename: Any, fields: UnionListTextTuple = None, defaults: Tuple = None,
               fieldtype: Any = Text) -> Any:
    """
    Makes a new typing `collections.namedtuple`.

    Examples:
        >>> domain_fields: Tuple = ('company', 'server', )
        >>> Domain = namedtype('Domain', domain_fields)
        >>> assert 'Domain' in str(Domain)
        >>> domain_values: Tuple = ('nference.net', 'nferx.com', )
        >>> domain: Domain = namedtuple('Domain', domain_fields, defaults=domain_values)
        >>> domain
        Domain(company='nference.net', server='nferx.com')
        >>> assert 'Domain' in str(type(domain))
        >>> dir_names: Tuple = 'download', 'generated',
        >>> # noinspection PyUnresolvedReferences
        >>> dir_defaults: Tuple = tuple(Path('/tmp') / item for item in dir_names)
        >>> dir_defaults
        (Path('/tmp/download'), Path('/tmp/generated'))
        >>> dirs = namedtuple('TmpDir', dir_names, dir_defaults, Path)
        >>> dirs
        TmpDir(download=Path('/tmp/download'), generated=Path('/tmp/generated'))
        >>> assert'TmpDir' in str(type(dirs))

    Args:
        typename: Named Tuple Yyping Name.
        fields: Named Tuple Field Names.
        fieldtype: Named Tuple Fields typing.
        defaults: Creates Named Tuple with defaults values.

    Returns:
        Any: new typing `collections.namedtuple`.
    """
    fields = fields.split() if isinstance(fields, str) else fields
    typename = namedtype(typename, fields, fieldtype) if isinstance(typename, str) else typename
    TypeNameDefaults: typename = collections.namedtuple(typename.__name__, typename._fields, defaults=defaults)
    name_defaults: typename = TypeNameDefaults()
    return name_defaults


def namedtype(typename, fields: UnionListTextTuple, fieldtype: Any = Text) -> Any:
    """
    Returns a typing NamedTuple associating fieldtype to fields.

    Examples:
        >>> domain_fields: Tuple = ('company', 'server', )
        >>> Domain = namedtype('Domain', domain_fields)
        >>> assert 'Domain' in str(Domain)
        >>> type(Domain)
        <class 'type'>
        >>> home_dir_names: Tuple = ('download', 'generated', 'github', 'log', 'tmp', )
        >>> HomeDir = namedtype('HomeDir', home_dir_names, Path)
        >>> assert 'HomeDir' in str(HomeDir)
        >>> type(HomeDir)
        <class 'type'>

    Args:
        typename: Named Tuple Typing Name.
        fields: Named Tuple Field Names.
        fieldtype: Named Tuple Fields typing.

    Returns:
        Any: new typing `collections.namedtuple`.
    """
    fields = fields.split() if isinstance(fields, str) else fields
    return typing.NamedTuple(typename, **{item: fieldtype for item in fields})


def not_(name: Text) -> Bool:
    """
    Is not private?

    Args:
        name: name

    Returns:
        Bool:
    """
    return name[:1] != '_'


def once(f: Any) -> Any:
    """
    Runs a function (successfully) only once.
    The running can be reset by setting the :data:`wrapper.run` attribute to False

    Example:
        >>> import os
        >>>
        >>> from dotenv import load_dotenv
        >>>
        >>> @once
        ... def dot_env():
        ...    load_dotenv(os.path.join(os.getcwd(), '.env'))
        ...     # ic(os.getenv('PASSWORD'))
        >>>
        >>> dot_env()
        >>> dot_env()

    Args:
        f: f

    Returns:
        Any:
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if not wrapper.run:
            result = f(*args, **kwargs)
            wrapper.run = True
            return result

    wrapper.run = False
    return wrapper


def other(data: UnionListSetTuple, value: Any) -> Any:
    """
    Get The Other Value.

    Args:
        data: data
        value: value

    Returns:
        Any:
    """
    return data[0] if data[1] == value else data[1]


def package_info(p: Text = str(), stdout: Bool = False) -> TupleBoolTextText:
    """
    Check if installed version of package is the latest.

    Args:
        p: package name.
        stdout: stdout.

    Returns:
        TupleBoolTextText: [``upgrade_version`` upgrade version current != latest, ``current_version``,
            ``latest_version``].
    """
    p = p if p else path.repo
    latest_version = str(subprocess.run([sys.executable, '-m', 'pip', 'install', '{}==random'.format(p)],
                                        capture_output=True, text=True))
    latest_version = latest_version[latest_version.find('(from versions:') + 15:]
    latest_version = latest_version[:latest_version.find(')')]
    latest_version = latest_version.replace(' ', '').split(',')[-1]

    current_version = str(subprocess.run([sys.executable, '-m', 'pip', 'show', '{}'.format(p)],
                                         capture_output=True, text=True))
    current_version = current_version[current_version.find('Version:') + 8:]
    current_version = current_version[:current_version.find('\\n')].replace(' ', '')

    upgrade_version = False if latest_version == current_version else True
    if stdout:
        console.print(upgrade_version, current_version, latest_version)
    return upgrade_version, current_version, latest_version


@app.command()
def package_latest(p: Text = str(), stdout: Bool = False) -> Text:
    """
    Latest version of package using pip install random as version.

    Args:
        p: package.
        stdout: stdout.

    Returns:
        Text: latest_version.
    """
    p = p if p else path.repo
    latest_version = str(subprocess.run([sys.executable, '-m', 'pip', 'install', '{}==random'.format(p)],
                                        capture_output=True, text=True))
    latest_version = latest_version[latest_version.find('(from versions:') + 15:]
    latest_version = latest_version[:latest_version.find(')')]
    latest_version = latest_version.replace(' ', '').split(',')[-1]
    if stdout:
        console.print(latest_version)
    return latest_version


@app.command()
def package_latest_search(p: Text = str(), stdout: Bool = False) -> Text:
    """
    Latest version of package using pip search.

    Args:
        p: package.
        stdout: stdout.

    Returns:
        Text: latest_version.
    """
    p = p if p else path.repo
    latest_version = str(subprocess.run([sys.executable, '-m', 'pip', 'search', p], capture_output=True, text=True))
    text = f'{p} ('
    latest_version = latest_version[latest_version.find(text) + len(text):]
    latest_version = latest_version[:latest_version.find(')')]
    if stdout:
        console.print(latest_version)
    return latest_version


plural = inflect.engine().plural


def pop_default(data: Dict, key: Any, default: Any = None) -> TupleAnyDict:
    """
    Dict Pop with Default.

    Examples:
        >>> pop_default(dict(a=1), 'b', True) #doctest: +ELLIPSIS
        (True, {'a': 1})
        >>> pop_default(dict(a=1), 'b') #doctest: +ELLIPSIS
        (None, {'a': 1})
        >>> pop_default(dict(a=1), 'a') #doctest: +ELLIPSIS
        (1, {})

    Args:
        data: data
        key: key
        default: default

    Returns:
        TupleAnyDict:
    """
    try:
        value = data.pop(key)
    except KeyError:
        value = default
    return value, data


def print_modules(p: Text):
    p = p if p else path.repo
    p = importlib.import_module(p)
    # noinspection PydanticTypeChecker
    console.print(mod_name(p))
    # noinspection PyUnresolvedReferences
    for mod in p._modules:
        if mod._isPackage:
            print_modules(mod)
        else:
            # noinspection PyCallingNonCallable
            console.print(mod_name(mod))


@app.command()
def pypifree(name: Text, stdout: Bool = False) -> Bool:
    """
    Pypi name available.

    Examples:
        >>> assert pypifree('common') is False
        >>> assert pypifree('sdsdsdsd') is True

    Args:
        name: package.
        stdout: stdout.

    Returns:
        Bool: True if available.
    """
    r = requests.get(f'https://pypi.org/pypi/{name}/json')

    if r:
        if stdout:
            red('Taken')
        return False
    else:
        if stdout:
            green('Available')
        return True


def rename_keys(mydict: Dict, rename_map: Dict) -> Dict:
    for current_name, new_name in rename_map.items():
        if mydict.get(current_name) is not None:
            mydict[new_name] = mydict[current_name]
            del mydict[current_name]
    return mydict


@app.command()
def secrets():
    """Secrets Update."""
    dist = distro.LinuxDistribution().info()['id']
    if dist == 'darwin':
        os.system(f'secrets-push.sh')
    elif dist == 'Kali':
        os.system(f'secrets-pull.sh')


def sub_run(command: Text = None, arguments: Tuple = tuple()) -> Any:
    """
    Subprocess run.

    Args:
        command: os command to run.
        arguments: os command arguments.

    Returns:
        Union[subprocess.CompletedProcess[Text], subprocess.CompletedProcess]:
    """
    try:
        return subprocess.run([command, *arguments], stdout=subprocess.PIPE, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        repr(e)


def sub_run_sys(command: Text = None, arguments: Tuple = tuple()) -> Int:
    """
    Subprocess run with the same interpreter as the module has been invoked.

    Args:
        command: command to run.
        arguments: command arguments.

    Returns:
        Int:
    """
    try:
        ret = subprocess.check_call([sys.executable, '-m', command, *arguments])
        return ret
    except subprocess.CalledProcessError as e:
        repr(e)


def true_bool(value: UnionTextBool = None, none_as_false: Bool = True) -> OptionalBool:
    """
    Return a bool for the arg.

    Args:
        value: value
        none_as_false: returns False if None or None.

    Returns:
        OptionalBool:
    """
    if isinstance(value, bool):
        return value
    if value is None and not none_as_false:
        return None
    if isinstance(value, str):
        value = value.lower()
    if value in ('yes', 'on', '1', 'true', 1):
        return True
    return False


@app.command()
def tty_max(stdout: Bool = False) -> Int:
    """
    Max tty width.

    Args:
        stdout: stdout.

    Returns:
        Int:
    """
    try:
        tty_max_width = shutil.get_terminal_size().columns
        # tty_max_width = os.get_terminal_size().columns
    except OSError:
        tty_max_width = 80
    if stdout:
        console.print(tty_max_width)
    return tty_max_width


def reverse_dict(data: Dict) -> Dict:
    """
    Reverse a Dict.

    Args:
        data: data

    Returns:
        Dict:
    """
    keys_list = list(map(lambda k: k, data))
    reverse_key_list = keys_list[::-1]
    reverse_d = dict()
    i = 0
    while i < len(reverse_key_list):
        key = reverse_key_list[int(i)]
        reverse_d[key] = data[key]
        i += 1
    if len(reverse_d) > 0:
        return reverse_d


def upcase_values(mydict: Dict, keys: List = None) -> Dict:
    if keys is None:
        keys = []
    for key in keys:
        value = mydict.get(key)
        if value is not None:
            mydict[key] = value.upper()
    return mydict


def upgrade_message(p: Text = str(), out: Bool = False):
    """
    Prints message to user if package must be upgraded.

    Args:
        p: package.
        out: exit.
    """
    p = p if p else path.repo
    upgrade, current, latest = package_info(p)
    latest = package_latest(p)
    if latest != current:
        sty.fg.orange = sty.Style(sty.RgbFg(255, 150, 50))
        print(sty.fg.orange + f'Please upgrade: {p} ({latest})' + sty.fg.rs)
        print(f'  INSTALLED: {current}')
        print(f'  LATEST:    {latest}')
        print(sty.fg.orange + f'python3 -m pip install --upgrade {p}' + sty.fg.rs)
        print()
    if out:
        sys.exit(1)


def upper_prefix(data: UnionDictListSetTextTuple = None, *, prefix: Text = None,
                 envs: environs.Env = None) -> Optional[UnionDictListSetTextTuple]:
    """
    Dict/List/Tuple Upper Items/Keys and Prefix Add.

    Examples:
        >>> upper_prefix()
        >>> pfx = 'repo'
        >>> tests = {'first': 1, 'second': 2}
        >>> upper_prefix(prefix=pfx)
        'REPO_'
        >>> upper_prefix(tests)
        {'FIRST': 1, 'SECOND': 2}
        >>> upper_prefix(tests, prefix=pfx)
        {'REPO_FIRST': 1, 'REPO_SECOND': 2}
        >>> data_new = tuple(tests.keys())
        >>> upper_prefix(data_new, prefix=pfx)
        ('REPO_FIRST', 'REPO_SECOND')
        >>> data_new = list(tests.keys())
        >>> upper_prefix(data_new, prefix=pfx)
        ['REPO_FIRST', 'REPO_SECOND']
        >>> upper_prefix('first', prefix=pfx)
        'REPO_FIRST'

    Args:
        data: data to upper and to add prefix.
        prefix: prefix to add.
        envs: `environs.Env` file.

    Returns:
        Optional[UnionDictListSetTextTuple]:
    """

    def get_prefix(v: Text):
        p = f'{prefix.upper()}_' if prefix and not prefix.endswith('_') else prefix
        return f'{p.upper()}{v.upper()}' if prefix else v.upper()

    if data is None and prefix and envs is None:
        return get_prefix(str())
    if isinstance(data, dict):
        return {get_prefix(key): value for key, value in data.items()}
    else:
        for item in (list, set, tuple):
            if isinstance(data, item):
                if envs is None:
                    return item(get_prefix(var) for var in data)
                else:
                    return {var: envs(get_prefix(var), None) for var in data}
        if isinstance(data, str):
            return get_prefix(data)


def vars_to_dict(search_dict: Dict, variables: UnionTextListDict) -> Dict:
    """
    List or string words to dict with vars and values from dict.

    Args:
        search_dict: search_dict
        variables: variables

    Returns:
        Dict:
    """
    if isinstance(variables, str):
        return {var: search_dict.get(var, '') if '.' not in var else getattr(
            search_dict.get(var.split('.')[0]), var.split('.')[1], '') for var in variables.split()}
    elif isinstance(variables, list):
        return {var: search_dict.get(var, '') if '.' not in var else getattr(
            search_dict.get(var.split('.')[0]), var.split('.')[1], '') for var in variables}
    elif isinstance(variables, dict):
        return {var: search_dict.get(var, '') if '.' not in var else getattr(
            search_dict.get(var.split('.')[0]), var.split('.')[1], '') for var in list(variables)}


# </editor-fold>


class AliasedGroup(click.Group):
    """
    Implements execution of the first partial match for a command. Fails with a
    message if there are no unique matches.

    See: https://click.palletsprojects.com/en/7.x/advanced/#command-aliases.
    """

    def get_command(self, ctx, cmd_name: Text):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            return None
        if len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))


class Asdict:
    """Dict and Attributes Tuple Class."""
    __exclude__ = ('asdict', 'asdict_keys',)
    __none__ = '_cached_cparts',

    @property
    def asdict(self) -> Dict:
        """
        Dict including properties without routines.

        Returns:
            Dict:
        """
        return asdict(self)

    @property
    def asdict_keys(self) -> Tuple:
        """
        Return a Tuple with instances attributes names.

        Returns:
            Tuple:
        """
        return tuple(self.asdict.keys())


class AsdictLarge:
    """Additional Helper Methods Data Dict Sub Class."""
    __exclude__ = ('asdict', 'asdict_keys',)

    @property
    def asdict(self) -> Dict:
        """
        Dict including properties without routines.

        Returns:
            Dict:
        """
        return asdict(self)

    @property
    def asdict_keys(self) -> Tuple:
        """
        Return a Tuple with instances attributes names.

        Returns:
            Tuple:
        """
        return tuple(self.asdict.keys())

    @classmethod
    def attrs(cls) -> Tuple:
        """
        Return a Tuple with dataclass and not dataclass attrs names (annotated attrs and not annotated attrs).

        Returns:
            Tuple:
        """
        return tuple(cls.defaults().keys())

    @classmethod
    def attrs_class(cls) -> Tuple:
        """
        Return a Tuple with not dataclass attrs names (not annotated attrs).

        Returns:
            Tuple:
        """
        return tuple(cls.defaults_class().keys())

    @classmethod
    def attrs_dataclass(cls) -> Tuple:
        """
        Return a Tuple with dataclass attrs names (annotated attrs).

        Returns:
            Tuple:
        """
        if cls.is_dataclass():
            return tuple(cls.defaults_dataclass().keys())
        return tuple()

    @classmethod
    def attrs_make_public(cls) -> Tuple:
        """
        Return a Tuple with dataclass and not dataclass attrs names (annotated attrs and not annotated attrs).
        Attrs names are converted from private to public.

        Returns:
            Tuple:
        """
        return tuple(cls.defaults_make_public().keys())

    @classmethod
    def defaults(cls) -> Dict:
        """
        Return a Dict describing dataclass and not dataclass attrs names (annotated attrs and not annotated attrs)
        with values.

        Returns:
            Dict:
        """
        return {**cls.defaults_class(), **cls.defaults_dataclass()}

    @classmethod
    def defaults_class(cls) -> Dict:
        """
        Return a Dict describing not dataclass attrs names (not annotated attrs) with values.

        Returns:
            Dict:
        """
        attrs_dataclass = cls.attrs_dataclass()
        return {key: value for key, value in cls.__dict__.items() if key.startswith('__') is False
                and key not in attrs_dataclass
                and key not in asdict_exclude(cls)
                and isinstance(value, property) is False
                and inspect.isroutine(value) is False}

    @classmethod
    def defaults_dataclass(cls) -> Dict:
        """
        Return a Dict describing dataclass attrs names (annotated attrs) with values.

        Returns:
            Dict:
        """
        if cls.is_dataclass():
            # noinspection PyDataclass
            return {item.name: item.default for item in dataclasses.fields(cls)}
        return dict()

    @classmethod
    def defaults_make_public(cls) -> Dict:
        """
        Return a Dict describing dataclass and not dataclass attrs names (annotated attrs and not annotated attrs)
        with values. Attrs names are converted from private to public.

        Returns:
            Dict:
        """
        defaults = cls.defaults()
        return {key[1:] if key.startswith('_') else key: value for key, value in defaults.items()}

    @classmethod
    def dict_cls(cls) -> Dict:
        """
        Dict including properties without routines.

        Returns:
            Dict:
        """
        return asdict(cls)

    def dict_attrs(self) -> Tuple:
        """
        Tuple Dict with all public and private instance attributes and properties names.

        Returns:
            Tuple
        """
        return tuple(self.asdict.keys())

    def dict_private(self) -> Dict[Text, Any]:
        """
        Dict with all private instance attributes and properties values.

        Returns:
            Dict[Text, Any]:
        """
        return {item: self.asdict.get(item) for item in self.asdict if item.startswith('_')}

    def dict_private_attrs(self) -> Tuple:
        """
        Dict with all private instance attributes names.

        Returns:
            Tuple:
        """
        return tuple(self.dict_private().keys())

    def dict_public(self) -> DictTextAny:
        """
        Dict with all public instance attributes and properties values.

        Returns:
            Dict[Text, Any]:
        """
        return {item: self.asdict.get(item) for item in self.asdict if item.startswith('_') is False}

    def dict_public_attrs(self) -> Tuple:
        """
        Dict with all public instance attributes names.

        Returns:
            Tuple:
        """
        return tuple(self.dict_public().keys())

    @classmethod
    def is_dataclass(cls) -> bool:
        """
        Is Data Class?.

        Returns:
            bool:
        """
        return hasattr(cls, dataclasses._FIELDS)


class Box(box.Box):
    """Frozen Box."""

    def __init__(self, *args: Any, **kwargs: Any):
        if 'default_box' not in kwargs:
            kwargs['default_box'] = True
        super().__init__(*args, **kwargs)

    @property
    def hash(self) -> Box:
        return Box(self, frozen_box=True)

    @classmethod
    def box_enum(cls, keys: Text) -> Box:
        """
        Box enum.

        Args:
            keys: keys

        Returns:
            Box:
        """
        return cls({key: value.lower() for key, value in keys.split()}, default_box=True)


@dataclasses.dataclass
class Count:
    percentage: Text = str()
    ok: Int = int()
    error: Int = int()
    no: Int = int()
    count: Int = int()
    total: Int = 1
    log: Logr = None
    verbose: Bool = False

    async def aouterr(self, msg: Text = str()):
        await executor(self.outerr, msg)

    async def aoutno(self, msg: Text = str()):
        await executor(self.outno, msg)

    async def aoutok(self, msg: Text = str()):
        await executor(self.outok, msg)

    def console(self, msg, error: Bool = False, no: Bool = False):
        if self.verbose:
            if error:
                cprint(f"[bold blue]{self.percentage}[white] "
                       f"\[ok: [bold green]{self.ok}[white], "
                       f"error: [bold red]{self.error}[white], "
                       f"no: [bold magenta]{self.no}[white], "
                       f"total: [bold blue]{self.total}[white]] "
                       f"[bold red]{msg}")
                self.log.error(self.format(msg))
                return
            if no:
                cprint(f"[bold blue]{self.percentage}[white] "
                       f"\[ok: [bold green]{self.ok}[white], "
                       f"error: [bold red]{self.error}[white], "
                       f"no: [bold magenta]{self.no}[white], "
                       f"total: [bold blue]{self.total}[white]] "
                       f"[bold magenta]{msg}")
            cprint(f"[bold blue]{self.percentage}[white] "
                   f"\[ok: [bold green]{self.ok}[white], "
                   f"error: [bold red]{self.error}[white], "
                   f"no: [bold magenta]{self.no}[white], "
                   f"total: [bold blue]{self.total}[white]] "
                   f"[bold green]{msg}")
        self.log.debug(self.format(msg))

    def format(self, msg):
        try:
            return fm(self, msg)
        except IndexError:
            self.log.debug('fm IndexError')

    def get_percentage(self):
        return f'{round(self.count * 100 / self.total, 2)}%'

    def outerr(self, msg: Text = str()):
        self.error += 1
        self.count += 1
        self.percentage = self.get_percentage()
        self.console(msg, error=True)

    def outno(self, msg: Text = str()):
        self.no += 1
        self.count += 1
        self.percentage = self.get_percentage()
        self.console(msg, no=True)

    def outok(self, msg: Text = str()):
        self.ok += 1
        self.count += 1
        self.percentage = self.get_percentage()
        self.console(msg)


class DataProxy:
    """Dict+Attr Get/Set Data Proxy Helper Class."""

    def attrs_get(self, *args, **kwargs) -> Dict:
        """
        Get One or More Attributes.

        Examples:
            >>> dataproxy = DataProxy()
            >>> dataproxy.d1 = 1
            >>> dataproxy.d2 = 2
            >>> dataproxy.d3 = 3
            >>> assert dataproxy.attrs_get('d1') == {'d1': 1}
            >>> assert dataproxy.attrs_get('d1', 'd3') == {'d1': 1, 'd3': 3}
            >>> assert dataproxy.attrs_get('d1', 'd4', default=False) == {'d1': 1, 'd4': False}

        Raises:
            ValueError: ValueError

        Args:
            *args: attr(s) name(s).
            **kwargs: default.

        Returns:
            Dict:
        """
        if not args:
            raise ValueError(f'args must be provided.')
        default = kwargs.get('default', None) if kwargs else None
        return {item: getattr(self, item, default) for item in args}

    def attrs_set(self, *args, **kwargs) -> Any:
        """
        Sets one or more attributes.

        Examples:
            >>> dataproxy = DataProxy()
            >>> dataproxy.attrs_set(d_1=31, d_2=32)
            >>> dataproxy.attrs_set('d_3', 33)
            >>> d_4_5 = dict(d_4=4, d_5=5)
            >>> dataproxy.attrs_set(d_4_5)
            >>> dataproxy.attrs_set('c_6', 36, c_7=37)
            >>> assert asdict(dataproxy) == {'c_6': 36, 'c_7': 37, 'd_1': 31, 'd_2': 32, 'd_3': 33, 'd_4': 4, 'd_5': 5}


        Raises:
            ValueError: ValueError

        Args:
            *args: attr name and value.
            **kwargs: attrs names and values.
        """
        if args:
            if len(args) > 2 or (len(args) == 1 and not isinstance(args[0], dict)):
                raise ValueError(f'args, invalid args length: {args}. One dict or two args (var name and value.')
            kwargs.update({args[0]: args[1]} if len(args) == 2 else args[0])

        for key, value in kwargs.items():
            setattr(self, key, value)


@dataclasses.dataclass
class Distro:
    """Distro Class."""
    _info: Any = collections.namedtuple('LinuxDistribution', tuple(distro.LinuxDistribution().info().keys()),
                                        defaults=tuple(distro.LinuxDistribution().info().values()))()
    _id: Text = _info.id
    _codename: Text = _info.codename
    _like: Text = _info.like
    _distro_version_parts: Any = collections.namedtuple('DistroVersionParts', tuple(_info.version_parts.keys()),
                                                        defaults=tuple(_info.version_parts.values()))()
    _version_parts_major: Int = int(_distro_version_parts.major)
    _version_parts_minor: Int = int(_distro_version_parts.minor)
    _version_parts_build_number: Union[Int, Text] = int(_distro_version_parts.build_number) \
        if _distro_version_parts.build_number else str()
    CENTOS: Bool = True if _id == 'centos' else False
    centos_codenames: Tuple = ('Core', 'Final',)  # type: ignore
    CENTOS_CORE: Bool = True if _codename == 'Core' else False
    CENTOS_FINAL: Bool = True if _codename == 'Final' else False
    centos_releases: Tuple = ('8', '7', '6',)  # type: ignore
    CENTOS_8: Bool = True if _version_parts_major == '8' else False
    CENTOS_7: Bool = True if _version_parts_major == '7' else False
    CENTOS_6: Bool = True if _version_parts_major == '6' else False
    DEBIAN: Bool = True if _id == 'debian' else False
    debian_codenames: Tuple = ('bookworm', 'bullseye', 'buster', 'stretch',)  # type: ignore
    DEBIAN_BOOKWORM: Bool = True if _codename == 'bookworm' else False
    DEBIAN_BULLSEYE: Bool = True if _codename == 'bullseye' else False
    DEBIAN_BUSTER: Bool = True if _codename == 'buster' else False
    DEBIAN_STRETCH: Bool = True if _codename == 'stretch' else False
    DEBIAN_LIKE: Bool = True if _like == 'debian' or _id == 'debian' else False
    FEDORA: Bool = True if _id == 'fedora' else False
    fedora_codenames: Tuple = ('',)  # type: ignore
    FEDORA_LIKE: Bool = \
        True if _like == 'fedora' or _id == 'fedora' or 'fedora' in _like else False
    fedora_releases: Tuple = ('33', '32',)  # type: ignore
    FEDORA_33: Bool = True if _version_parts_major == '33' else False
    FEDORA_32: Bool = True if _version_parts_major == '32' else False
    KALI: Bool = True if _id == 'kali' else False
    MACOS: Bool = psutil.MACOS
    macos_codenames: Tuple = ('',)  # type: ignore
    POSIX: Bool = psutil.POSIX
    RHEL: Bool = True if _id == 'rhel' else False
    rhel_codenames: Tuple = ('Ootpa', 'Maipo',)  # type: ignore
    RHEL_LIKE: Bool = True if 'rhel' in _like else False
    rhel_releases: Tuple = ('8', '7',)  # type: ignore
    RHEL_8: Bool = True if _version_parts_major == '8' else False
    RHEL_7: Bool = True if _version_parts_major == '7' else False
    UBUNTU: Bool = True if _id == 'ubuntu' else False
    ubuntu_codenames: Tuple = ('focal', 'bionic', 'xenial',)  # type: ignore
    UBUNTU_FOCAL: Bool = True if _codename == 'focal' else False
    UBUNTU_BIONIC: Bool = True if _codename == 'bionic' else False
    UBUNTU_XENIAL: Bool = True if _codename == 'xenial' else False
    kernel: Text = _id  # darwin (macOS), linux (redhat, ubuntu) - os.uname().sysname is capitalized
    kernels: Tuple = ('darwin', 'linux',)  # type: ignore
    KERNEL_AIX: Bool = psutil.AIX
    KERNEL_BSD: Bool = psutil.BSD
    KERNEL_FREEBSD: Bool = psutil.FREEBSD
    KERNEL_DARWIN: Bool = True if _id == 'darwin' else False
    KERNEL_LINUX: Bool = psutil.LINUX
    KERNEL_NETBSD: Bool = psutil.NETBSD
    KERNEL_OPENBSD: Bool = psutil.OPENBSD
    KERNEL_SUNOS: Bool = psutil.SUNOS
    KERNEL_WINDOWS: Bool = psutil.WINDOWS
    build: Int = _version_parts_build_number
    codename: Text = _codename
    distro: Text = _id
    distros: Tuple = ('centos', 'darwin', 'debian', 'fedora', 'rhel', 'ubuntu',)  # type: ignore
    like: Text = _like  # centos is like 'rhel fedora'
    likes: Tuple = ('debian', 'fedora', 'rhel fedora',)  # type: ignore
    major: Int = _version_parts_major
    minor: Int = _version_parts_minor
    version: Text = _info.version  # macOS (19.5.0), Ubuntu (16.04), rhel (8.2)

    @classmethod
    def exec(cls, name) -> Bool:
        """
        Checks if executable is in ``PATH``.

        Args:
            name: executable/command name.

        Returns:
            Bool:
        """
        return True if shutil.which(name) is not None else False

    @classmethod
    def install(cls, name, cask: Bool = False) -> Text:
        """
        Installs package.

        Args:
            name: executable/command name.
            cask: brew cask.

        Raises:
            NotImplementedError: Not installer.
            FileNotFoundError: Not in PATH after install.

        Returns:
            Text:
        """
        brew_url = 'https://raw.githubusercontent.com/Homebrew/install/master/install.sh'
        if not cls.exec(name):
            if cls.MACOS:
                if not cls.exec('brew'):
                    _, stderr, rc = cmd(f'yes yes | /bin/bash -c "$(curl -fsSL {brew_url})" ')
                    if rc != 0:
                        raise NotImplementedError(f'package not available {name}.')
                options = 'cask' if cask else str()
                command = f'brew {options} install'
            elif cls.DEBIAN_LIKE or cls.KALI:
                command = f'apt install -y'
            elif cls.FEDORA_LIKE:
                command = f'yum install -y'
            else:
                raise NotImplementedError('Not installer available.')

            _, stderr, rc = cmd(f'{command} {name}')
            if rc != 0:
                red(fm(stderr))

        if cls.exec(name):
            return shutil.which(name)
        raise FileNotFoundError(f'{name} not in PATH.')


class Enum(enum.Enum):
    @classmethod
    def new(cls, name, attrs: Iterable, doc: Text = str(), start: Union[Bool, Int, Tuple, Absent] = 1,
            default: Int = 0) -> Union[Type[enum.Enum], Iterable]:
        """
        Creates a new enum.

        # Examples:
        #     >>> from bapy import DataProxy, Executor, ExitCode, Extend, ListUtils, Logr, Path, Meta
        #     >>> Enum.new('ApiVersion', 'v1 beta', doc='Nexus API version')
        #     <enum 'ApiVersion'>
        #     >>> Enum.new('ApiVersion', 'v1 beta', doc='Nexus API version').default
        #     <ApiVersion.v1: 1>
        #     >>> Executor.asdict
        #     {'NONE': 1, 'THREAD': 2, 'PROCESS': 3}
        #     >>> ExitCode.default
        #     <ExitCode.LARGE_FILE_ERROR: 100>
        #     >>> assert DataProxy in Extend.ALL.value
        #     >>> ListUtils.attrs
        #     ('LOWER', 'UPPER', 'CAPITALIZE', 'PREFIX', 'SUFFIX')
        #     >>> Logr.Levels.asdict
        #     {'DEBUG': 10, 'INFO': 20, 'WARNING': 30, 'ERROR': 40, 'CRITICAL': 50}
        #     >>> Logr.Levels.DEBUG.describe
        #     ('DEBUG', 10)
        #     >>> Path.Mode.__doc__
        #     'Group/Other File/Dir Mode'
        #     >>> Path.Mode['FILE']
        #     <Mode.FILE: 511>
        #     >>> Path.Option.FILES
        #     <Option.FILES: 'files'>
        #     >>> Path.Output.NAMED.value
        #     'named'
        #     >>> Path.Suffix.default
        #     <Option.NO_SUFFIX: 'no_suffix'>

        Args:
            name: name
            attrs: field names
            doc: docstring
            start: True ``name.lower()``, False ``name``. Absent getattr(start, name), Tuple values like methods, et.
            default: default

        Returns:
            Type[Enum]:
        """
        new_cls = Enum(name, attrs, start=start)
        if isinstance(start, tuple):
            new_cls.values = start
        new_cls.__doc__ = doc if doc else f'{name} Enum'
        new_cls.asdict = {key: value._value_ for key, value in new_cls.__members__.items()}
        new_cls.attrs = tuple(new_cls.__members__)
        new_cls.default = new_cls[new_cls.attrs[default]]
        return new_cls

    def _generate_next_value_(self, start, count, last_values):
        if isinstance(start, bool):
            if start:
                return self.lower()
            else:
                return self
        elif isinstance(start, int):
            for last_value in reversed(last_values):
                try:
                    return last_value + 1
                except TypeError:
                    pass
            else:
                return start
        elif isinstance(start, tuple):
            return start[count]
        else:
            return getattr(start, str(self))

    @property
    def describe(self) -> Tuple:
        """
        Returns:
            Tuple:
        """
        # self is the member here
        return self.name, self.value


class Env(Asdict):
    """
    Env Class.

    # Examples:
        # >>> import os
        # >>> from bapy import Path, m
        # >>>
        # >>> # Cleaning
        # >>> project_env_file = m.project.path.joinpath('.env')
        # >>> project_env_file.rm()
        # >>> tmp_path = Path('/tmp')
        # >>> tmp_env_file = tmp_path.joinpath('.env')
        # >>> tmp_env_file.rm()
        # >>>
        # >>> # env.environ tests
        # >>> env = Env()
        # >>> env.environ = dict(a=1, b=2)
        # >>> env.environ
        # {'a': '1', 'b': '2'}
        # >>> os.environ['A']
        # '1'
        # >>> os.environ['B']
        # '2'
        # >>> env.asdict  # doctest: +ELLIPSIS
        # {'_environ': ['a', 'b'], 'environ': {'a': '1', 'b': '2'}, ...
        # >>>
        # >>> # env.file tests
        # >>> tmp_path = Path().cd('/tmp')
        # >>> tmp_env_file = tmp_path.joinpath('.env')
        # >>> tmp_env_file.write_text('export LOG_LEVEL=DEBUG')
        # 22
        # >>> assert tmp_env_file.read_text() == 'export LOG_LEVEL=DEBUG'
        # >>> env = Env()
        # >>> assert env.file.log_level('LOG_LEVEL') == 10
        # >>> assert env.file.dump()['LOG_LEVEL']  == 10
        # >>> tmp_env_file.rm()
    """
    _environ: List = None  # type: ignore
    file: environs.Env = environs.Env()

    def __init__(self, prefix: Text = str()):
        self.log_level_default = Logr.stream
        self.verbose_default = False
        self.debug_async_default = False
        self.debug_default = False
        self.prefix = prefix
        self.file.read_env(Path.cwd().joinpath('.env').text, verbose=True, override=True)
        self.log_level = self.file.log_level(upper_prefix('LOG_LEVEL', prefix=prefix), self.log_level_default)
        self.debug_async = self.file.bool(upper_prefix('DEBUG_ASYNC', prefix=prefix), self.debug_async_default)
        self.verbose = self.file.bool(upper_prefix('VERBOSE', prefix=prefix), self.verbose_default)
        self.debug = self.file.bool(upper_prefix('DEBUG', prefix=prefix), self.debug_default)
        self.username = self.file('USERNAME', os.environ.get('USERNAME', None))
        self.nferx_atlas_password = self.file('NFERX_ATLAS_PASSWORD', os.environ.get('NFERX_ATLAS_PASSWORD', None))
        self.bapy = Path(BAPY) if (BAPY := self.file('BAPY', os.environ.get('BAPY', None))) else User.home
        self.pen = Path(PEN) if (PEN := self.file('PEN', os.environ.get('PEN', None))) else User.home

        if self.log_level == 'DEBUG' or self.log_level == logging.DEBUG:
            self.verbose = True
        if self.verbose:
            self.log_level = logging.DEBUG
        self.aiodebug()

    def aiodebug(self, enable: Bool = False):
        # import warnings

        def ok():
            tracemalloc.start()
            self.environ = {'PYTHONASYNCIODEBUG': 1}
            logger = logging.getLogger('asyncio')
            logger.setLevel('DEBUG')
            # warnings.simplefilter("default", ResourceWarning)

        def no():
            tracemalloc.stop()
            self.environ = {'PYTHONASYNCIODEBUG': 0}
            logger = logging.getLogger('asyncio')
            logger.setLevel('ERROR')
            # warnings.simplefilter("ignore", ResourceWarning)

        if self.debug_async or enable:
            return ok()
        return no()

    @property
    def environ(self) -> Dict:
        """
        OS Environ Vars Set.

        Returns:
            Dict:
        """
        if self._environ:
            return {item: os.environ.get(item.upper()) for item in self._environ}

    @environ.setter
    def environ(self, value: Dict):
        """
        Sets `os.environ` Vars and stores keys in `self.environ`.

        Args:
            value: value
        """
        if not self.environ:
            self._environ = list()
        for key in value:
            os.environ[key.upper()] = str(value[key])
            self._environ.append(key)

    @property
    async def sem(self):
        return Sem(*[self.file.int(upper_prefix(k, prefix=self.prefix), v)
                     for k, v in Sem.defaults().items()])


class EnvInterpolation(configparser.BasicInterpolation):
    """
    Extended Interpolation which expands environment variables in values.

    Examples:
        >>> import os
        >>> os.environ['PATH_TEST'] = System.exe_path.text
        >>> cfg = '''
        ...     [section]
        ...     key = value
        ...     my_path = ${PATH_TEST}:/private/tmp
        ... '''
        >>>
        >>> config = configparser.ConfigParser(interpolation=EnvInterpolation())
        >>> config.read_string(cfg)
        >>> my_path = config['section']['my_path']
        >>> if my_path == f'{System.exe_path.text}:/private/tmp':
        ...     print(True)
        True
    """

    def before_get(self, parser, section, option, value, defaults):
        value = super().before_get(parser, section, option, value, defaults)
        return os.path.expandvars(value)

    @staticmethod
    def read_ini(p: Path, raw: Bool = True) -> UnionParser:
        """
        Read ini with :class:'~configparser.RawConfigParser` or :class:`EnvInterpolation`.

        Args:
            p: path.
            raw: raw.

        Returns:
            UnionParser:
        """
        if raw:
            i = configparser.RawConfigParser()
            i.optionxform = str
        else:
            i = configparser.ConfigParser(interpolation=EnvInterpolation())

        i.read(str(p))
        return i


Executable = dataclasses.make_dataclass('Executable',
                                        [(item.upper(), Bool, dataclasses.field(default=Distro.exec(item)))
                                         for item in ('apt', 'brew', 'curl', 'docker', 'go', 'haproxy', 'make',
                                                      'nmap', 'npm', 'pip', 'pip3', 'r', 'sudo', 'tar', 'yum',)])

Executor = Enum.new('Executor', 'NONE THREAD PROCESS')


async def executor(func: Any, *args: Any, pool: Executor = Executor.NONE.name, **kwargs: Any) -> Any:
    """
    Run in :lib:func:`loop.run_in_executor` with :class:`concurrent.futures.ThreadPoolExecutor`,
        :class:`concurrent.futures.ProcessPoolExecutor` or
        :lib:func:`asyncio.get_running_loop().loop.run_in_executor` or not poll.

    Args:
        func: func
        *args: args
        pool: pool
        **kwargs: kwargs

    Raises:
        ValueError: ValueError

    Returns:
        Awaitable:
    """
    loop = asyncio.get_running_loop()
    call = functools.partial(func, *args, **kwargs)
    if not func:
        raise ValueError

    if pool == Executor.THREAD.name:
        with concurrent.futures.ThreadPoolExecutor() as thread_pool:
            return await loop.run_in_executor(thread_pool, call)
    elif pool == Executor.PROCESS.name:
        with concurrent.futures.ProcessPoolExecutor() as process_pool:
            return await loop.run_in_executor(process_pool, call)
    else:
        return await loop.run_in_executor(None, call)


ExitCode = Enum.new('ExitCode', 'LARGE_FILE_ERROR HTTP_REQUEST_ERROR INVALID_CREDENTIALS_ERROR '
                                'GET_NOT_FOUND_404_ERROR JSON_DECODER_RESPONSE_ERROR INVALID_REPO_PATH_ERROR '
                                'FILE_OR_DIR_ERROR UPLOAD_INVALID_REPO_ERROR UPLOAD_DIR_TO_FILE_ERROR '
                                'SHOW_INVALID_REPO_ERROR LS_UNKNOWN_OR_PATH_ERROR '
                                'UP_DOWN_COUNT_0_ERROR UP_DOWN_API_ERROR UNKNOWN_ERROR API_ERROR SUBCOMMAND_ERROR '
                                'DOWNLOAD_ERROR CONFIG_ERROR ADMIN_CREDENTIALS_NEEDED CONNECTION_ERROR '
                                'DELETE_RESPONSE_ERROR INVALID_ENVIRONMENT_ERROR INVALID_API_VERSION_ERROR '
                                'INVALID_LOG_DIR_ERROR INVALID_LOG_LEVEL_ERROR INVALID_SSH_KEY_FILE_ERROR '
                                'INVALID_CONFIG_FIELD_ERROR INVALID_CONFIG_ATTR_ERROR INVALID_CONFIG_SET_ATTR_ERROR '
                                'INVALID_CONFIG_ERROR', 'Error codes returned by :lib:mod:`repo.cli.cli`.', 100)

Extend = Enum.new('Extend', 'DICT DICTLARGE PROXY ALL', 'Extend bases for simple namespace',
                  ({Asdict, }, {AsdictLarge, }, {DataProxy, }, {AsdictLarge, DataProxy, }))

FlowRunType = Enum.new('FlowRunType', 'BASH PYTHON PIPE')

FlowRunState = Enum.new('FlowRunType', 'FAIL INIT RUNNING SUCCESS')


@dataclasses.dataclass
class Flows:
    """Flow type class"""
    pass


@dataclasses.dataclass
class Flow(Flows):
    """
    Add python and/or bash tasks to flow.

    Attributes:
    # noinspection PyUnresolvedReferences
        name: Flow to run.
        l: Logging logger
        added: Tasks added.
        depends: Flow dependencies.
        state: Flow thread run state.
    """
    name: Text
    l: Any
    added: OrderedDict = None  # type: ignore
    depends: List = None  # type: ignore
    state: FlowRunState = None  # type: ignore

    def __post_init__(self):
        self.name = f'Flow({self.name})'
        self.added = collections.OrderedDict()
        self.thread = collections.OrderedDict()
        self.depends = list()

    def add_tasks(self, tasks: Union[List, FlowPython, FlowBash]) -> Any:
        """
        Add tasks to flow.

        Args:
            tasks: List of tasks/flows to run.

        Raises:
            TypeError: Invalid task type.

        Returns:
            Any:
        """
        if not tasks:
            return
        print(type(tasks))
        print(type(list()))

        if not isinstance(tasks, list):
            tasks = ['tasks']

        for task in tasks:
            valid = isinstance(task, FlowTask) or isinstance(task, Flows)
            if not valid:
                raise TypeError(f'Task should be type Python or Bash: {type(task)}')

        for task in tasks:
            self.added[uuid.uuid4()] = [task]
            self.l.v(f'{task} added to flow: {self.name}')
        return self

    def add_dependencies(self, flows: Union[List, Flows]):
        """
        Add flow dependencies (other flows).

        Args:
            flows: Flow dependencies.

        Raises:
            TypeError: Invalid flow type.
        """

        for task in flows:
            if not isinstance(task, Flows):
                raise TypeError(f'Dependencies should be type Flow: {type(task)}')
        self.depends.extend(flows)

    def check_depends(self) -> Bool:
        """
        Check success of dependencies.

        Returns:
            Bool:
        """
        allowed = True
        for item in self.depends:
            allowed = allowed and (item.state == FlowRunState.SUCCESS)
        return allowed

    def run(self):
        """Method to run the flow."""
        self.l.v(f'{self.name}: run')

        if not self.check_depends():
            return

        # NOTE: fully implement threading. Now only serial and run ready with reports and graphs.
        broken = False
        prev = True
        for key, tasks in self.added.items():
            if not prev:
                break
            threads = []
            # Threads: Tasks - Create
            for task in tasks:
                threads.append(FlowRun(task))
            # Threads: Tasks - Start
            for thread in threads:
                thread.start()
            # Thread: Main Flow - Created
            for thread in threads:
                thread.join()
            self.thread[key] = tuple(threads)
            # Thread: Stage - Finished
            for thread in threads:
                prev = prev and (thread.state == FlowRunState.SUCCESS)
                if not prev:
                    broken = True
                prev = prev or False

        if prev and not broken:
            self.state = FlowRunState.SUCCESS
        else:
            self.state = FlowRunState.FAIL


@dataclasses.dataclass(init=False)
class FlowTask:
    """ Flow base task. """
    pass


@dataclasses.dataclass(init=False)
class FlowBash(FlowTask):
    # noinspection PyUnresolvedReferences
    """
    Bash Commands to flow tasks.

    Attributes:
        command: Command to run.
    """
    command: Any = None
    name: Any = None

    def __init__(self, command):
        self.command = command
        self.name = f'Bash({" ".join(self.command)})'


@dataclasses.dataclass(init=False)
class FlowPython(FlowTask):
    # noinspection PyUnresolvedReferences
    """
    Python Routines to flow tasks.

    Attributes:
        name:
        routine: Routine to run.
        args: Arguments to run with.
        kwargs: Keyword arguments to run with.
    """
    routine: Any
    args: Any
    kwargs: Any
    name: Any = None

    def __init__(self, routine, args=tuple(), kwargs=tuple()):
        self.name = f'Python({routine.__name__})'
        self.routine = routine
        self.args = args
        self.kwargs = kwargs


@dataclasses.dataclass(init=False)
class FlowRun(threading.Thread):
    # noinspection PyUnresolvedReferences
    """
        Run flow class. Wrapper around Thread.

        Attributes:
            task: Thread task.
            type: Task type.
            state: Task run state.
            exception: Task thread exception.
        """
    # _task: Optional[Any, Python, Bash, Flows] = None
    _task: Any = None
    _type: FlowRunType = None  # type: ignore
    _state: FlowRunState = None  # type: ignore
    _exception: Any = None

    def __init__(self, task: Any):
        self._task = task
        if isinstance(task, FlowPython):
            self._type = FlowRunType.PYTHON
            super().__init__(target=task.routine, args=task.args, kwargs=task.kwargs)
        elif isinstance(task, FlowBash):
            # Lambda to avoid subprocess.Popen to run immediately.
            self._type = FlowRunType.BASH
            super().__init__(target=lambda: subprocess.Popen(task.command).wait())
        else:
            self._type = FlowRunType.PIPE
            super().__init__(target=task.run)

        self._state = FlowRunState.INIT
        self._exception = None

    def run(self):
        """Runs the thread in an exception free way."""
        try:
            self._state = FlowRunState.RUNNING
            super().run()
            if self._type == FlowRunType.PIPE:
                self._state = self._task.state
            else:
                self._state = FlowRunState.SUCCESS
        except Exception as e:
            self._state = FlowRunState.FAIL
            self._exception = e

    @property
    def task(self) -> Any:
        """
        Thread task.

        Returns:
            Any:
        """
        return self._task

    @property
    def type(self) -> FlowRunType:
        """
        Task type.

        Returns:
            FlowRunType:
        """
        return self._exception

    @property
    def state(self) -> FlowRunState:
        """
        Task run state.

        Returns:
            FlowRunState:
        """
        return self._state

    @property
    def exception(self) -> Any:
        """
        Task thread exception.

        Returns:
            Any:
        """
        return self._exception


class Frame:
    """Convenience Frame and Stack Class."""
    ctx: Int = 1
    index: Int = 1

    def __init__(self, index: Int = index, ctx: Int = ctx):
        frameinfo: FrameInfo = inspect.stack(ctx)[index]
        frame: FrameType = frameinfo.frame
        self.frame = frame
        self.code_context: List = frameinfo.code_context
        self.function: Text = frameinfo.function
        self.lineno: Int = frameinfo.lineno
        self.filename: Path = Path(frameinfo.filename).resolved

        self.parent: Path = self.filename.parent
        self.module: Text = inspect.getmodulename(self.filename.text)

        self.f_code: CodeType = frame.f_code
        self.f_lineno = frameinfo.frame.f_lineno
        self.globals: Box = Box(frame.f_globals)

        self.locals: Box = Box(inspect.currentframe().f_locals)

        self.package: Text = self.globals.get('__package__', None)
        self.globals_name: Text = self.globals.get('__name__', None)
        self.globals_file: Path = Path(self.globals.get('__file__', None)).resolved

        self.globals_file_parent: Path = self.globals_file.parent
        self.globals_file_module: Text = inspect.getmodulename(self.globals_file.text)

        self.locals_name: Text = self.locals.get('__name__', None)

        if back := getattr(frame, 'f_back', None):
            if 'importlib._bootstrap' in str(back):
                if frame_back := getattr(back, 'f_back', None) is None:
                    raise BapyFrameBackBack(str(back))
                else:
                    path.log.warning(fm(back, frame_back))
                    frame = frame_back
            self.back = getattr(frame, 'f_back', None)

            self.back_code: CodeType = back.f_code
            self.back_lineno: CodeType = back.f_lineno
            self.back_function: Text = self.back_code.co_name
            self.back_globals: Box = Box(back.f_globals)
            self.back_locals: Box = Box(back.f_locals)

            self.back_package: Text = self.globals.get('__package__', None)
            self.back_globals_name: Text = self.back_globals.get('__name__', None)
            self.back_file: Path = Path(self.back_globals.__file__).resolved

            self.back_parent: Path = self.back_file.parent
            self.back_file_module: Text = inspect.getmodulename(self.back_file.text)

            self.back_locals_name: Text = self.back_locals.get('__name__', None)

    def installed(self, p: Any = None, index: Int = index, ctx: Int = ctx) -> Bool:
        """
        Checks if path installed in sys.

        Args:
            p: path
            index: index
            ctx: context

        Returns:
            Bool:
        """
        p = str(p) if p else str(self.__class__(index, ctx).back_file)
        return True if p.startswith(str(Py.exe_prefix)) or p.startswith(str(Py.sys_prefix)) else False

    @classmethod
    def vars_all(cls) -> List:
        return [
            key for key, value in cls().back_globals.items() if key[:1] != '_' and (
                    isinstance(value, str) or
                    isinstance(value, int) or
                    isinstance(value, list) or
                    isinstance(value, tuple) or
                    isinstance(value, set) or
                    isinstance(value, float) or
                    isinstance(value, dict) or
                    isinstance(value, Path) or
                    isinstance(value, Url)
            )
        ]


@dataclasses.dataclass
class GitHub:
    path: Any
    repo: git.Repo = dataclasses.field(default=None, init=False)
    git: git.Git = dataclasses.field(default=None, init=False)
    remote: git.Remote = dataclasses.field(default=None, init=False)
    config: git.GitConfigParser = dataclasses.field(init=False)
    cli: Dict[Text, List] = dataclasses.field(init=False)  # type: ignore
    config_path: Any = None
    id_rsa: Any = None
    url: Any = dataclasses.field(init=False)
    username: Text = None

    _version_new: Text = None
    _version_old: Text = None

    def __post_init__(self):
        self.url = Url.lumenbiomics(repo=self.path.name)
        try:
            self.repo = git.Repo(self.path)
        except git.exc.NoSuchPathError:
            self.repo = self.clone()
        except git.exc.InvalidGitRepositoryError:
            pass

        if self.repo:
            self.cmd = self.repo.git
            self.remote = self.repo.remote()

        self.cli = {
            'test_usable': ['git', 'rev-parse', '--git-dir'],
            'commit': ['git', 'commit', '-F'],
        }

        self.config_path = self.config_path if self.config_path else User.git_config_path
        self.config = git.GitConfigParser(self.config_path)
        self.id_rsa = self.id_rsa if self.id_rsa else User.id_rsa
        self.username = self.username if self.username else self.config.get_value(section='user', option='username',
                                                                                  default=str())
        os.environ['GIT_SSH_COMMAND'] = f'ssh -i {self.id_rsa} -o UserKnownHostsFile=/dev/null ' \
                                        f'-o StrictHostKeyChecking=no -o IdentitiesOnly=yes'
        if self.path.exists() is False:
            self.clone()

    @property
    def version_new(self):
        return self._version_new

    @version_new.setter
    def version_new(self, version: Text):
        self._version_new = version

    @property
    def version_old(self):
        return self._version_old

    @version_old.setter
    def version_old(self, version: Text):
        self._version_old = version

    @property
    def message(self):
        return f'Bump: {self.version_old} --> {self.version_new}'

    def add(self, force: Bool = False, write: Bool = True):
        """
        Adds untracked files to Git.

        Args:
            force: force
            write: write
        """
        for file in self.repo.untracked_files:
            added = self.repo.index.add(file, force=force, write=write)
            ic(f'{added[0][3]=}')

    def clone(self, url: Text = None, p: Path = None) -> git.Repo:
        """
        Wrapper for :meth:`git.Repo.clone_from`.
        #
        # Examples:
        #     >>> from bapy import Path, m
        #     >>> ssh_options = '-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o IdentitiesOnly=yes'
        #     >>> os.environ['GIT_SSH_COMMAND'] = f'ssh -i {User.id_rsa} {ssh_options}'
        #     >>> repo = m.project.name
        #     >>> dest_dir = Path(f'/tmp/{repo}')
        #     >>> dest_dir.rm()
        #     >>> GitHub.clone(Url.lumenbiomics(http=False, repo=repo), dest_dir) #doctest: +ELLIPSIS
        #     <git.repo.base.Repo '/tmp/bapy/.git'>
        #     >>> dest_dir.rm()

        Args:
            url: git url
            p: destination path

        Returns:
            git.Repo:
        """
        return git.Repo.clone_from(url=url if url else self.url, to_path=p.text if p else self.path.text)

    def commit_cmd(self, message: Text = None) -> None:
        if message is None:
            message = self.message
        commit = self.cmd.commit('-m', message)
        ic(commit)

    def commit_cli(self, message, ctx, extra_args=None):
        extra_args = extra_args or []
        with tempfile.NamedTemporaryFile('wb', delete=False) as f:
            f.write(message.encode('utf-8'))
        env = os.environ.copy()
        env['HGENCODING'] = 'utf-8'
        for key in ('current_version', 'new_version'):
            env[str('BUMPVERSION_' + key.upper())] = str(ctx[key])
        try:
            subprocess.check_output(
                self.cli['commit'] + [f.name] + extra_args, env=env
            )
        except subprocess.CalledProcessError as exc:
            err_msg = f'Failed to run {exc.cmd}: return code {exc.returncode}, output: {exc.output}'
            path.log.exception(err_msg)
            raise exc
        finally:
            os.unlink(f.name)

    def push(self, remote: Text = 'origin'):
        push = self.repo.remote(remote).push()
        ic(push[0].summary, 'push[0].flags')

    def tag(self, version: Text = None):
        if version is None:
            version = self.version_new
        tag = self.repo.create_tag(version)
        ic(tag)

    def is_usable(self):
        try:
            return (
                    subprocess.call(
                        self.cli['test_usable'],
                        stderr=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                    )
                    == 0
            )
        except OSError as e:
            if e.errno in (errno.ENOENT, errno.EACCES):
                return False
            raise

    @classmethod
    def assert_nondirty(cls):
        lines = [
            line.strip()
            for line in subprocess.check_output(
                ['git', 'status', '--porcelain']
            ).splitlines()
            if not line.strip().startswith(b"??")
        ]

        if lines:
            raise BapyGitDirectoryIsDirty(
                "Git working directory is not clean:\n{}".format(
                    b"\n".join(lines).decode()
                )
            )

    @classmethod
    def latest_tag_info(cls):
        try:
            # git-describe doesn't update the git-index, so we do that
            subprocess.check_output(['git', 'update-index', '--refresh'])

            # get info about the latest tag in git
            describe_out = (
                subprocess.check_output(
                    [
                        'git',
                        'describe',
                        '--dirty',
                        '--tags',
                        '--long',
                        '--abbrev=40',
                        '--match=v*',
                    ],
                    stderr=subprocess.STDOUT,
                ).decode().split("-")
            )
        except subprocess.CalledProcessError:
            # m.log.debug('Error when running git describe')
            return {}

        inf = {}

        if describe_out[-1].strip() == 'dirty':
            inf['dirty'] = True
            describe_out.pop()

        inf['commit_sha'] = describe_out.pop().lstrip('g')
        inf['distance_to_latest_tag'] = int(describe_out.pop())
        inf['current_version'] = '-'.join(describe_out).lstrip('v')

        return inf

    @classmethod
    def add_path(cls, p):
        subprocess.check_output(['git', 'add', '--update', p])

    @classmethod
    def tag_cli(cls, sign, tag, message):
        command = ['git', 'tag', tag]
        if sign:
            command += ['--sign']
        if message:
            command += ['--message', message]
        subprocess.check_output(command)


GetAll = Enum.new('GetAll', 'KEYS VALUES')


def get_all(obj: UnionDictList, get: GetAll = GetAll.KEYS) -> Iterable:
    # noinspection PyUnresolvedReferences
    """
    All keys or values of nested Dict or List.

    Examples:
        >>> data = dict(key1=dict(key2=dict(key3=dict(key4='value1'))))
        >>> keys = tuple(item for item in get_all(data))
        >>> keys
        ('key1', 'key2', 'key3', 'key4')
        >>> values = tuple(item for item in get_all(data, GetAll.VALUES))
        >>> values
        ('value1',)

    Args:
        obj: obj
        get: get

    Raises:
        ValueError: ValueError

    Yields:
        Iterable:
    """
    if isinstance(obj, dict):
        for key, value in obj.items():
            if get is GetAll.KEYS:
                yield key
            elif get == GetAll.VALUES:
                if not (isinstance(value, dict) or isinstance(value, list)):
                    yield value
            else:
                raise ValueError('`GetAll.KEYS` or `GetAll.VALUES`')
            for ret in get_all(value, get=get):
                yield ret
    elif isinstance(obj, list):
        for el in obj:
            for ret in get_all(el, get=get):
                yield ret


@dataclasses.dataclass
class Ip:
    """
    IP Class.

    Examples:
        >>> assert asyncio.run(Ip('10:12:14').init) is None
        >>> valid = asyncio.run(Ip('8.8.8.8').init)
        >>> assert valid.info['ipv4'] == '8.8.8.8'
        >>> assert valid.info['ipv6'] is False
        >>> assert valid.location['country_name'] == 'United States'
        >>> assert valid.location['city'] is None
        >>> assert valid.ping is True
        >>> assert 'ping' in valid.attrs()
        >>> assert valid.asdict['info']['global'] is True
        >>> local = asyncio.run(Ip('192.168.1.134').init)
        >>> assert local.ping is False
        >>> myip = asyncio.run(Ip().init)
        >>> assert myip.info['global'] is True
    """
    info: Dict = dataclasses.field(default=None, init=False)
    ip: OptionalText = None
    location: Dict = dataclasses.field(default=None, init=False)
    name: Text = None
    retry: Int = 0
    retry_max: Int = 3
    retry_sleep: Int = 10

    def __post_init__(self):
        if self.ip is None:
            self.ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')

    @property
    def asdict(self) -> Dict:
        """
        Instance Dict.

        Returns:
            Dict:
        """
        return dataclasses.asdict(self)

    @classmethod
    def attrs(cls) -> Tuple:
        """
        Attrs tuple.

        Returns:
            Tuple:
        """
        return tuple(item.name for item in dataclasses.fields(cls))

    @property
    async def init(self) -> Optional[Ip]:
        """
        Ip Instance.

        Returns:
            Optional[Ip]:
        """
        self.info = dict()
        self.location = dict()
        if await self.IPClass:
            _ = await self.Location
            try:
                self.name = socket.getfqdn(self.ip)
            except socket.herror:
                pass
            return self

    @property
    async def IPClass(self) -> OptionalIPaddress:
        """
        Validates, stores ip, ipv4 and ipv6 as str and returns IPaddress.

        Returns:
            OptionalIPaddress:
        """
        try:
            rv = await sync_to_async(ipaddress.ip_address)(self.ip)
            self.ip = rv.compressed
            self.info['ipv4'] = rv.compressed if rv.version == 4 else False
            self.info['ipv6'] = rv.compressed if rv.version == 6 else False
            self.info['global'] = rv.is_global
            self.info['reverse_pointer'] = rv.reverse_pointer
            self.info['version'] = rv.version
        except ValueError:
            self.ip = rv = None
        return rv

    @property
    async def Location(self) -> OptionalDict:
        """
        IP Location Info.

        Returns:
            OptionalDict:
        """
        if self.ip:
            try:
                with await sync_to_async(urllib.request.urlopen)(
                        f'https://geolocation-db.com/json/697de680-a737-11ea-9820-af05f4014d91/{self.ip}') \
                        as geolocation:
                    location = await sync_to_async(json.loads)(geolocation.read().decode())
                self.location['city'] = location['city'] if location['city'] != 'Not found' else None
                self.location['country_code'] = location['country_code'] \
                    if location['country_code'] != 'Not found' else None
                self.location['country_name'] = location['country_name'] \
                    if location['country_name'] != 'Not found' else None
                self.location['latitude'] = location['latitude'] if location['latitude'] != 'Not found' else None
                self.location['longitude'] = location['longitude'] if location['longitude'] != 'Not found' else None
                self.location['postal'] = location['postal'] if location['postal'] != 'Not found' else None
                self.location['state'] = location['state'] if location['state'] != 'Not found' else None
                return location
            except urllib.error.HTTPError as exception:
                if self.retry < self.retry_max:
                    self.retry += 1
                    await asyncio.sleep(self.retry_sleep)
                    _ = await self.Location
                else:
                    path.log.error(fm(self.ip, exception))


ListUtils = Enum.new('ListUtils', 'LOWER UPPER CAPITALIZE PREFIX SUFFIX')


def list_utils(list_: [typing.List, Tuple] = None, option: ListUtils = ListUtils.LOWER, value: str = None) -> List:
    if option is ListUtils.LOWER:
        return [item.lower() for item in list_]
    if option is ListUtils.UPPER:
        return [item.upper() for item in list_]
    if option is ListUtils.CAPITALIZE:
        return [item.capitalize() for item in list_]
    if option is ListUtils.PREFIX:
        return [f'{value}{item}' for item in list_]
    if option is ListUtils.SUFFIX:
        return [f'{item}{value}' for item in list_]


class Log(verboselogs.VerboseLogger):
    """
    :class:`~verboselogs.VerboseLogger` helper to enter variable names in strings and creates logs records
    with variable name and value.

    Includes additional debugging information for debug and critical levels.
    """
    Level: Any = Literal['DEBUG', 'VERBOSE', 'INFO', 'WARNING', 'SUCCESS', 'ERROR', 'CRITICAL']
    Levels: Type[Enum] = Enum.new('Levels', Level.__args__, start=logging)
    file: Int = Levels.VERBOSE.value
    stream: Int = Levels.ERROR.value
    packages: Int = stream
    all: Dict = dict(package={}, packages={}, handlers=set(), root=set())  # type: ignore
    manager: Log = None
    package: Text = None
    format: Literal['short', 'large', 'date'] = 'large'
    formats: Dict[Literal['short', 'large', 'date'], Text] = dict(
        short='%(thin)s%(white)s[ %(log_color)s%(levelname)-8s%(white)s ] [ %(log_color)s%(name)-30s%(white)s ] '
              '%(white)s %(log_color)s%(message)s %(white)s%(reset)s',
        large='%(thin)s%(white)s[%(log_color)s%(asctime)s%(white)s] %(white)s[%(log_color)s%(levelname)s%(white)s] '
              '%(white)s[%(log_color)s%(name)s%(white)s] '
              '%(white)s[%(log_color)s%(funcName)s%(white)s:%(log_color)s%(lineno)d%(white)s] '
              '%(log_color)s%(message)s%(white)s%(reset)s',
        date='%(thin)s%(white)s[%(log_color)s%(asctime)s%(reset)s%(white)s] '
             '%(white)s[%(log_color)s%(levelname)s%(white)s] %(white)s[%(log_color)s%(name)s%(white)s] '
             '%(white)s[%(log_color)s%(filename)s%(reset)s:%(log_color)s%(lineno)d%(reset)s - '
             '%(log_color)s%(module)s%(reset)s - %(log_color)s%(funcName)s%(reset)s%(white)s] '
             '%(white)s %(log_color)s%(message)s %(white)s%(reset)s')  # type: ignore
    colors: Tuple = ('white', 'cyan', 'green', 'yellow', 'blue', 'purple', 'red',)  # type: ignore
    rotate: Dict = dict(count=5, interval=1, when='d')  # type: ignore

    __exclude__: Tuple = ('child',)  # type: ignore

    def __init__(self, name: Text = None, level: UnionTextInt = packages):
        self.name = name
        self.level = self._get_level(level)
        super().__init__(self.name, self.level)

    @property
    def child(self) -> Log:
        """
        Child logger with module name.

        Returns:
            child logger
        """
        frame = Frame()
        name = frame.back_parent.name if (module := frame.back_file_module) == '__init__' else module
        _l = self.getChild(name)
        _l.level_set()
        return _l

    @classmethod
    def get_log(cls, name: Text = None, p: Union[PathLike, Pathlib, Path] = None, file: UnionTextInt = file,
                stream: UnionTextInt = stream, packages: UnionTextInt = packages,
                installed: Bool = True) -> Union[Log, Logger]:
        """
        Sets Logger.

        Args:
            name: name
            p: path
            file: file
            stream: stream
            packages: packages
            installed: installed

        Returns:
            LogType:
        """
        f = Frame()
        cls.file = file if installed else 'DEBUG'
        cls.stream = stream
        cls.packages = packages
        logging.setLoggerClass(Log)
        logger = logging.getLogger(name if name else f.back_parent.name)
        logger.package = logger.name
        if root := (getattr(logger, 'parent', None)):
            root.setLevel(cls._get_level(cls.packages))
        logger.setLevel(cls._get_min(cls.file, cls.stream))
        formatter = colorlog.ColoredFormatter(fmt=cls.formats[cls.format],
                                              log_colors=dict(zip(cls.Levels.attrs, cls.colors)))
        fh = logging.FileHandler(p.text, 'w')
        rotating = logging.handlers.TimedRotatingFileHandler(
            str(p), when=cls.rotate['when'], interval=cls.rotate['interval'], backupCount=cls.rotate['count'])
        fh = rotating if installed else fh
        fh.setLevel(cls.file)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        sh = logging.StreamHandler()
        sh.setLevel(cls.stream)
        sh.setFormatter(formatter)
        logger.addHandler(sh)

        cls.manager = getattr(logger, 'manager', None)
        cls.level_set('packages', cls._get_level(cls.packages))
        start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f'{start=}')
        return logger

    @classmethod
    def _get_level(cls, level: UnionTextInt) -> Int:
        """
        Get Level Value

        Args:
            level: level

        Returns:
            Int:
        """
        if isinstance(level, str):
            level = getattr(logging, level.upper())
        return level

    @classmethod
    def _get_min(cls, x: UnionTextInt, y: UnionTextInt) -> Int:
        """
        Get Min Value

        Args:
            x: x
            y: y

        Returns:
            Int:
        """
        return min(cls._get_level(x), cls._get_level(y))

    @classmethod
    def level_set(cls, attr: Text = None, value: UnionTextInt = None):
        """
        Helper to sets Handler or Logger Level for caller setter.

        Args:
            attr: handler or logger attribute.
            value: level value to set.
        """
        if attr is not None:
            value = getattr(cls, attr) if value is None else cls._get_level(value)
            setattr(cls, attr, value)

        cls._level_set_logger('root', cls.packages)
        if (loggerDict := getattr(cls.manager, 'loggerDict', None)) is not None:
            for name in loggerDict:
                key = 'package' if name.startswith(cls.package if cls.package else name) else 'packages'
                level = cls._get_min(cls.file, cls.stream) if key == 'package' else cls.packages
                cls._level_set_logger(name, level, key)

    @classmethod
    def _level_set_handler(cls, logger):
        """
        Sets Handler Level.

        Args:
            logger: logger
        """
        if logger.hasHandlers():
            for handler in logger.handlers:
                if isinstance(handler, logging.handlers.TimedRotatingFileHandler) \
                        or isinstance(handler, logging.FileHandler):
                    handler.setLevel(cls._get_level(cls.file))
                if isinstance(handler, logging.StreamHandler) \
                        and not isinstance(handler, logging.handlers.TimedRotatingFileHandler) \
                        and not isinstance(handler, logging.FileHandler):
                    handler.setLevel(cls._get_level(cls.stream))
                key = logger.name if logger.name == 'root' else 'handlers'
                cls.all[key].add(handler)

    @classmethod
    def _level_set_logger(cls, name: Text, level: UnionTextInt, key: Text = None):
        """
        Sets Logger Level.

        Args:
            name: logger name.
            level: level value.
            key: `Log.all` key.
        """
        logger = logging.getLogger(name)
        logger.setLevel(cls._get_level(level))
        if key is None:
            cls.all[name].add(logger)
        else:
            cls.all[key][name] = logger
        if name == cls.package:
            cls._level_set_handler(logger)

    def out(self, msg: Text, err: ExitCode = None, exc: Any = None):
        """
        Prints message, logs and raise exception if enabled.

        Args:
            msg: if only message is provided: logs msg if enabled and prints green msg.
            err: if err is provided: logs msg if enabled, prints red msg and `sys.exit` with `err.value`.
            exc: if exception is provided, err must be provided and logs critical with exception.

        Raises:
            AttributeError: AttributeError
        """
        if exc is not None and err is None:
            raise AttributeError(f'ExitCode must be provided when exception is not None: {err}')
        if exc is not None:
            try:
                raise exc(msg)
            except exc as e:
                self.critical(e)
                red(f'[{err.name}]: {msg}')
                sys.exit(err.value)
        elif exc is None and err is None:
            self.debug(msg)
            green(msg)
        else:
            self.debug(msg)
            red(f'[{err.name}]: {msg}')
            sys.exit(err.value)

    @classmethod
    def prepare_msg(cls, msg, *args) -> Text:
        rv = ', '.join(str(item) for item in (msg, *args,))
        return rv

    def log(self, level, msg, *args, **kwargs):
        if not isinstance(level, int):
            if logging.raiseExceptions:
                raise TypeError("level must be an integer")
            else:
                return
        if self.isEnabledFor(level):
            self._log(level, '\n' + self.prepare_msg(msg, *args), (), **kwargs)

    def debug(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.DEBUG):
            self._log(logging.DEBUG, '\n' + self.prepare_msg(msg, *args), (), **kwargs)

    def verbose(self, msg, *args, **kwargs):
        if self.isEnabledFor(verboselogs.VERBOSE):
            self._log(verboselogs.VERBOSE, '\n' + self.prepare_msg(msg, *args), (), **kwargs)

    def info(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.INFO):
            self._log(logging.INFO, '\n' + self.prepare_msg(msg, *args), (), **kwargs)

    def warning(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.WARNING):
            self._log(logging.WARNING, '\n' + self.prepare_msg(msg, *args), (), **kwargs)

    def success(self, msg, *args, **kwargs):
        if self.isEnabledFor(verboselogs.SUCCESS):
            self._log(verboselogs.SUCCESS, '\n' + self.prepare_msg(msg, *args), (), **kwargs)

    def error(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.ERROR):
            self._log(logging.ERROR, '\n' + self.prepare_msg(msg, *args), (), **kwargs)

    def critical(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.CRITICAL):
            self._log(logging.CRITICAL, '\n' + self.prepare_msg(msg, *args), (), **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        self.error('\n' + self.prepare_msg(msg, *args), (), exc_info=exc_info, **kwargs)


class Logr(Logger):
    Level: Any = Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']  # type: ignore
    Levels: Type[Enum] = Enum.new('Levels', Level.__args__, start=logging)
    file: Int = Levels.DEBUG.value
    stream: Int = Levels.ERROR.value
    packages: Int = stream
    all: Dict = dict(package={}, packages={}, handlers=set(), root=set())  # type: ignore
    manager: Log = None
    package: Text = None
    format: Literal['short', 'large'] = 'large'
    formats: Dict[Literal['short', 'large', 'date'], Text] = dict(
        short='%(message)s',
        large='[%(name)s| %(module)s| %(funcName)s %(lineno)s] - %(message)s', )  # type: ignore
    rotate: Dict = dict(count=5, interval=1, when='d')  # type: ignore
    colors: Tuple = ('white', 'green', 'yellow', 'red', 'purple',)  # type: ignore
    propagate: Bool = True
    mode: Text = 'a'

    def __init__(self, name: Text = None, level: UnionTextInt = packages):
        self.name = name
        self.level = self._get_level(level)
        super().__init__(self.name, self.level)

    @property
    def child(self) -> Logr:
        """
        Child logger with module name.

        Returns:
            child logger
        """
        frame = Frame()
        name = frame.back_parent.name if (module := frame.back_file_module) == '__init__' else \
            f'{frame.back_parent.name}.{module}'
        _l = self.getChild(name)
        _l.level_set()
        return _l

    @classmethod
    def get_log(cls, name: Text = None, p: Union[PathLike, Pathlib, Path] = None, file: UnionTextInt = file,
                stream: UnionTextInt = stream, packages: UnionTextInt = packages, installed: Bool = True,
                markup: Bool = True) -> Union[Logr, Logger]:
        """
        Sets Logger.

        Args:
            name: name
            p: path
            file: file
            stream: stream
            packages: packages
            installed: installed
            markup: markup

        Returns:
            LogType:
        """
        f = Frame()
        cls.file = file if installed else 'DEBUG'
        cls.stream = stream
        cls.packages = packages
        logging.setLoggerClass(Logr)
        logger = logging.getLogger(name if name else f.back_parent.name)
        logger.propagate = cls.propagate
        logger.package = logger.name
        if root := (getattr(logger, 'parent', None)):
            root.setLevel(cls._get_level(cls.packages))
        logger.setLevel(cls._get_min(cls.file, cls.stream))

        if installed or cls.mode == 'a':
            fh = logging.handlers.TimedRotatingFileHandler(
                str(p), when=cls.rotate['when'], interval=cls.rotate['interval'], backupCount=cls.rotate['count'])
        else:
            fh = logging.FileHandler(p.text, cls.mode)
        fh_formatter = colorlog.ColoredFormatter(fmt=Log.formats[Log.format],
                                                 log_colors=dict(zip(cls.Levels.attrs, cls.colors)))
        fh.setLevel(cls.file)
        fh.setFormatter(fh_formatter)
        logger.addHandler(fh)

        rh_formatter = logging.Formatter(fmt=cls.formats[cls.format])
        rh = rich.logging.RichHandler(markup=markup)
        rh.setLevel(cls.stream)
        rh.setFormatter(rh_formatter)
        logger.addHandler(rh)

        cls.manager = getattr(logger, 'manager', None)
        cls.level_set('packages', cls._get_level(cls.packages))
        # start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return logger

    @classmethod
    def _get_level(cls, level: UnionTextInt) -> Int:
        """
        Get Level Value

        Args:
            level: level

        Returns:
            Int:
        """
        if isinstance(level, str):
            level = getattr(logging, level.upper())
        return level

    @classmethod
    def _get_min(cls, x: UnionTextInt, y: UnionTextInt) -> Int:
        """
        Get Min Value

        Args:
            x: x
            y: y

        Returns:
            Int:
        """
        return min(cls._get_level(x), cls._get_level(y))

    @classmethod
    def level_set(cls, attr: Text = None, value: UnionTextInt = None):
        """
        Helper to sets Handler or Logger Level for caller setter.

        Args:
            attr: handler or logger attribute.
            value: level value to set.
        """
        if attr is not None:
            value = getattr(cls, attr) if value is None else cls._get_level(value)
            setattr(cls, attr, value)

        cls._level_set_logger('root', cls.packages)
        if (loggerDict := getattr(cls.manager, 'loggerDict', None)) is not None:
            for name in loggerDict:
                key = 'package' if name.startswith(cls.package if cls.package else name) else 'packages'
                level = cls._get_min(cls.file, cls.stream) if key == 'package' else cls.packages
                cls._level_set_logger(name, level, key)

    @classmethod
    def _level_set_handler(cls, logger):
        """
        Sets Handler Level.

        Args:
            logger: logger
        """
        if logger.hasHandlers():
            for handler in logger.handlers:
                if isinstance(handler, logging.handlers.TimedRotatingFileHandler) \
                        or isinstance(handler, logging.FileHandler):
                    handler.setLevel(cls._get_level(cls.file))
                if isinstance(handler, logging.StreamHandler) \
                        and not isinstance(handler, logging.handlers.TimedRotatingFileHandler) \
                        and not isinstance(handler, logging.FileHandler):
                    handler.setLevel(cls._get_level(cls.stream))
                key = logger.name if logger.name == 'root' else 'handlers'
                cls.all[key].add(handler)

    @classmethod
    def _level_set_logger(cls, name: Text, level: UnionTextInt, key: Text = None):
        """
        Sets Logger Level.

        Args:
            name: logger name.
            level: level value.
            key: `Log.all` key.
        """
        logger = logging.getLogger(name)
        logger.setLevel(cls._get_level(level))
        if key is None:
            cls.all[name].add(logger)
        else:
            cls.all[key][name] = logger
        if name == cls.package:
            cls._level_set_handler(logger)

    def out(self, msg: Text, err: ExitCode = None, exc: Any = None):
        """
        Prints message, logs and raise exception if enabled.

        Args:
            msg: if only message is provided: logs msg if enabled and prints green msg.
            err: if err is provided: logs msg if enabled, prints red msg and `sys.exit` with `err.value`.
            exc: if exception is provided, err must be provided and logs critical with exception.

        Raises:
            AttributeError: AttributeError
        """
        if exc is not None and err is None:
            raise AttributeError(f'ExitCode must be provided when exception is not None: {err}')
        if exc is not None:
            try:
                raise exc(msg)
            except exc as e:
                self.critical(e)
                red(f'[{err.name}]: {msg}')
                sys.exit(err.value)
        elif exc is None and err is None:
            self.debug(msg)
            green(msg)
        else:
            self.debug(msg)
            red(f'[{err.name}]: {msg}')
            sys.exit(err.value)

    @classmethod
    def prepare_msg(cls, msg, *args) -> Text:
        rv = ', '.join(str(item) for item in (msg, *args,))
        return rv

    def log(self, level, msg, *args, **kwargs):
        if not isinstance(level, int):
            if logging.raiseExceptions:
                raise TypeError("level must be an integer")
            else:
                return
        if self.isEnabledFor(level):
            self._log(level, self.prepare_msg(msg, *args), (), **kwargs)

    async def adebug(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.DEBUG):
            await executor(self._log, logging.DEBUG, self.prepare_msg(msg, *args), (), **kwargs)

    async def ainfo(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.INFO):
            await executor(self._log, logging.INFO, self.prepare_msg(msg, *args), (), **kwargs)

    async def awarning(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.WARNING):
            await executor(self._log, logging.WARNING, self.prepare_msg(msg, *args), (), **kwargs)

    async def aerror(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.ERROR):
            await executor(self._log, logging.ERROR, self.prepare_msg(msg, *args), (), **kwargs)

    async def acritical(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.CRITICAL):
            await executor(self._log, logging.CRITICAL, self.prepare_msg(msg, *args), (), **kwargs)

    async def aexception(self, msg, *args, exc_info=True, **kwargs):
        await self.aerror(self.prepare_msg(msg, *args), (), exc_info=exc_info, **kwargs)

    def debug(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.DEBUG):
            self._log(logging.DEBUG, self.prepare_msg(msg, *args), (), **kwargs)

    def info(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.INFO):
            self._log(logging.INFO, self.prepare_msg(msg, *args), (), **kwargs)

    def warning(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.WARNING):
            self._log(logging.WARNING, self.prepare_msg(msg, *args), (), **kwargs)

    def error(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.ERROR):
            self._log(logging.ERROR, self.prepare_msg(msg, *args), (), **kwargs)

    def critical(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.CRITICAL):
            self._log(logging.CRITICAL, self.prepare_msg(msg, *args), (), **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        self.error(self.prepare_msg(msg, *args), (), exc_info=exc_info, **kwargs)


UnionTextLogger = Union[Text, Logger, Log, Logr]


@dataclasses.dataclass
class Machine:
    """Server OS and Platform Class."""
    fqdn: Text = socket.getfqdn()
    hostname: Text = os.uname().nodename.split('.')[0]  # pro, repo
    machine: Text = os.uname().machine  # x86_64
    nodename: Text = os.uname().nodename  # pro, repo.nferx.com
    processor: Text = platform.processor()  # amdk6,


@dataclasses.dataclass
class MongoBase:
    """
    Mongo DB Base Helper Class.

    Examples:
    >>> base = MongoBase()
    >>> base.db.name
    'pen'
    >>> base.db_name = 'admin'
    >>> base.db.name
    'admin'
    >>> base.db_default.name
    'pen'
    """
    _db_name: Text = None
    uri_name: Text = 'pen'
    address: Tuple = ('127.0.0.1', 27017)
    uri: UnionTextTuple = address
    FiltersBase: Any = collections.namedtuple('FiltersBase', 'col_names')
    filters_base: FiltersBase = FiltersBase({"name": {"$regex": r"^(?!system\.|.*file|.*glob|.*invalid)"}})
    nap: Int = 10

    @property
    def client(self) -> UnionMongo:
        while True:
            try:
                client = MotorClient(self.uri, connectTimeoutMS=200000, serverSelectionTimeoutMS=300000,
                                     maxPoolSize=300) if aioloop() else MongoClient(self.uri)
                return client
            except (socket.gaierror, pymongo.errors.ConnectionFailure, pymongo.errors.AutoReconnect,
                    pymongo.errors.ServerSelectionTimeoutError, pymongo.errors.ConfigurationError) as exception:
                path.log.warning(f'Waiting for connection: {repr(exception)}')
                time.sleep(self.nap)
                continue

    @property
    def col_names(self) -> List:
        return self.db.list_collection_names(filter=self.filters_base.col_names)

    @property
    async def col_names_async(self) -> List:
        return await self.db.list_collection_names(filter=self.filters_base.col_names)

    @property
    def cols_list(self) -> List:
        return [self.db.get_collection(item) for item in self.col_names]

    @property
    async def cols_list_async(self) -> List:
        return [self.db.get_collection(item) for item in await self.col_names_async]

    @property
    def cols_count_estimated(self) -> Dict:
        return {item.name: item.estimated_document_count() for item in self.cols_list}

    @property
    async def cols_count_estimated_async(self) -> Dict:
        return {item.name: await item.estimated_document_count() for item in await self.cols_list_async}

    def cols_unique(self, field: Text = '_id') -> Dict:
        return {item.name: item.distinct(field) for item in self.cols_list}

    async def cols_unique_async(self, field: Text = '_id') -> Dict:
        return {item.name: item.distinct(field) for item in await self.cols_list_async}

    @property
    def db(self) -> Any:
        return self.client.get_database(self.db_name)

    @property
    def db_default(self) -> Any:
        return self.client.get_default_database()

    @property
    def db_name(self) -> Text:
        return self._db_name if self._db_name else self.db_default.name

    @db_name.setter
    def db_name(self, value):
        self._db_name = value


@dataclasses.dataclass
class Mongo(MongoBase):
    """Mongo Helper Class."""
    _col_name: Text = None
    col_name_default: Text = 'test'

    @property
    def col(self) -> Any:
        return self.db.get_collection(self.col_name)

    @property
    def col_default(self) -> Any:
        return self.db.get_collection(self.col_name_default)

    @property
    def col_name(self) -> Text:
        return self._col_name if self._col_name else self.col_default.name

    @col_name.setter
    def col_name(self, value):
        self._col_name = value

    @property
    def count_estimated(self) -> List:
        return self.col.estimated_document_count()

    @property
    async def count_estimated_async(self) -> List:
        return await self.col.estimated_document_count()

    @property
    def count_estimated_default(self) -> List:
        return self.col_default.estimated_document_count()

    @property
    async def count_estimated_default_async(self) -> List:
        return await self.col_default.estimated_document_count()

    def unique(self, field: Text = '_id') -> List:
        return self.col.distinct(field)


class Path(Pathlib, pathlib.PurePosixPath, Asdict, DataProxy):
    """
    Path Helper Class.

    Examples:
        # >>> from bapy import System
        # >>> os.chdir('/usr/local')
        # >>> path = Path('/usr/local').parent
        # >>> path.text, path.str, path.resolved, path.cwd()
        # ('/usr', '/usr', Path('/usr'), Path('/usr/local'))
        # >>> path.cd(System.sys_site)  # cd to new path
        # Path('/usr/local/lib/python3.8/site-packages')
        # >>> path.cd()  # cd to previous
        # Path('/usr/local')
        # >>> path_new = path.cd(System.sys_site)
        # >>> path_new
        # Path('/usr/local/lib/python3.8/site-packages')
        # >>> path_previous = path_new.cd()
        # >>> path_previous
        # Path('/usr/local')
        # >>> path_mkdir_add_test = Path('/tmp').mkdir_add('path_mkdir_add_test')
        # >>> assert '/tmp/path_mkdir_add_test' in path_mkdir_add_test.text
        # >>> path_touch_add_test = Path('/tmp').touch_add('path_touch_add_test')
        # >>> assert '/tmp/path_touch_add_test' in path_touch_add_test.text
        # >>> for glob_test in Path('/tmp').rglob('path*'):
        # ...     glob_test
        # Path('/tmp/path_mkdir_add_test')
        # Path('/tmp/path_touch_add_test')
        # >>> path_mkdir_add_test.rmdir()
        # >>> os.remove(path_touch_add_test.text)
        # >>>
        # >>> from bapy import User
        # >>> Path('/tmp/templates').rm()
        # >>> test = Path('/tmp').mkdir_add('templates') / 'test.templates'
        # >>> test.write_text('Defaults: {{ User.name }} !logfile, !syslog') #doctest: +ELLIPSIS
        # 43
        # >>> Path('/tmp').templates['test'].dump(dest='/tmp/sudoers')
        # >>> Path('/tmp/sudoers').read_text() #doctest: +ELLIPSIS
        # 'Defaults:... !logfile, !syslog'
        # >>> Path('/tmp/templates').rm()
        # >>> Path('/tmp/sudoers').rm()
        # >>> m.package.path.templates['sudoers'].dump()  # Fixme
    """
    cd_: Path = None
    package: Path = absent
    repo: Text = str()
    project: Path = absent
    installed: Bool = True
    prefix: Text = str()
    work: Path = absent
    env: Env = absent
    log: Logr = absent
    git: GitHub = absent
    scripts_suffix: Bool = False

    Mode = Enum.new('Mode', 'DIR FILE', 'Group/Other File/Dir Mode', (0o666, 0o777,))
    Option = Enum.new('Option', 'BOTH DIRS FILES', 'Scan Option', True, 2)
    Output = Enum.new('Option', 'BOTH BOX DICT LIST NAMED TUPLE', 'Scan Output', True, 1)
    Suffix = Enum.new('Option', 'BASH C CC CFG CONF CONFIG CSS CSV DBM DOCKER ENV GO GPG INI J2 JINJA2 JS JSON '
                                'JSON5 KEY LIST LOG MD MOD NO_SUFFIX PEM PUB REPO REPOS REST RST SH SPEC SQL '
                                'SWIFT TEXT TOML TS TSX TXT XML YAML YML', 'Scan File Suffix', True, 24)
    __exclude__ = ('templates', 'requirements', 'scripts', 'scripts_relative',)

    @dataclasses.dataclass
    class J2:
        """Jinja2 Templates Helper Class."""
        src: Path
        data: Dict = None  # type: ignore
        dest: Union[Path, Text] = None
        name: Text = dataclasses.field(init=False)
        stream: Any = dataclasses.field(init=False)
        render: Any = dataclasses.field(init=False)

        def __init__(self, src: Path, data: Dict = None, dest: Union[Path, Text] = None):
            self.src = src
            self.name = src.stem
            self.stream = jinja2.Template(self.src.read_text(), autoescape=True).stream
            self.render = jinja2.Template(self.src.read_text(), autoescape=True).render
            self.data = self.get_data(data)
            self.dest = self.get_dest(dest)

        @staticmethod
        def get_data(variables: Dict = None) -> Dict:
            f = Frame()
            return variables if variables else {**f.back_globals, **f.back_locals}

        def get_dest(self, dest: Union[Path, Text] = None) -> Path:
            return Path(dest) if dest else path.work.mkdir_add(self.__class__.__name__.lower()) / self.name

        def dump(self, data: Dict = None, dest: Union[Path, Text] = None):
            self.stream(self.get_data(data)).dump(self.get_dest(dest).text)

    def append_text(self, data, encoding=None, errors=None):
        """
        Open the file in text mode, append to it, and close the file.
        """
        if not isinstance(data, str):
            raise TypeError('data must be str, not %s' %
                            data.__class__.__name__)
        with self.open(mode='a', encoding=encoding, errors=errors) as f:
            return f.write(data)

    @property
    def templates(self) -> Dict:
        """
        Iter dir for templates and create dict with name and dump func

        Returns:
            Dict:
        """
        if self.name != 'templates':
            # noinspection PyMethodFirstArgAssignment
            self /= 'templates'

        if self.is_dir():
            return {item.stem: self.J2(item) for item in self.glob(f'*.{Path.Suffix[self.J2.__name__].value}')}
        return dict()

    def cd(self, p: Any = '-') -> Path:
        """
        Change working dir, returns new Path and stores previous.

        Args:
            p: path

        Returns:
            Path:
        """
        if self.cd_ is None:
            self.cd_ = self.cwd()
        p = self.cd_ if p == '-' else p
        cd_ = self.cwd()
        os.chdir(Path(str(p)).text)
        p = self.cwd()
        p.cd_ = cd_
        return p

    @property
    def endseparator(self) -> Text:
        """
        Add trailing separator at the end of path if does not exist.

        Returns:
            Text: path with separator at the end.
        """
        return self.text + os.sep

    def fd(self, *args, **kwargs):
        return os.open(self.text, *args, **kwargs)

    def mkdir_add(self, name, mode=0o700, parents=True, exist_ok=True) -> Path:
        """
        Add directory, make directory and return new Path.

        Args:
            name: name
            mode: mode
            parents: parents
            exist_ok: exist_ok

        Returns:
            Path:
        """
        if not (p := (self / name).resolved).is_dir():
            p.mkdir(mode=mode, parents=parents, exist_ok=exist_ok)
        return p

    @property
    def pwd(self) -> Path:
        return self.cwd().resolved

    # noinspection PydanticTypeChecker
    @property
    def requirements(self) -> Dict:
        """
        Scans for requirements files and returns a dict with parsed requirements per requirement file.

        Returns:
            Dict: dict with parsed requirements per requirement file.
        """
        try:  # for pip >= 10
            # noinspection PyCompatibility
            from pip._internal.req import parse_requirements
        except ImportError:  # for pip <= 9.0.3
            # noinspection PyUnresolvedReferences
            from pip.req import parse_requirements

        # noinspection PydanticTypeChecker,PyTypeChecker
        return {item.stem: [str(req.requirement) for req in parse_requirements(item.text, session='workaround')]
                for item in self.glob('requirements*')}

    @property
    def resolved(self) -> Path:
        return self.resolve()

    def rm(self, missing_ok=True):
        """
        Delete a folder/file (even if the folder is not empty)

        Args:
            missing_ok: missing_ok
        """
        if not missing_ok and not self.exists():
            raise
        if self.exists():
            # It exists, so we have to delete it
            if self.is_dir():  # If false, then it is a file because it exists
                shutil.rmtree(self)
            else:
                self.unlink()

    def scan(self, option: Path.Option = Option.FILES,
             output: Path.Output = Output.BOX, suffix: Path.Suffix = Suffix.NO_SUFFIX,
             level: Bool = False, hidden: Bool = False, frozen: Bool = False) -> Union[Box, Dict, List]:
        """
        Scan Path.

        Args:
            option: what to scan in path.
            output: scan return type.
            suffix: suffix to scan.
            level: scan files two levels from path.
            hidden: include hidden files and dirs.
            frozen: frozen box.

        Returns:
            Union[Box,Dict,List]: List [paths] or Dict {name: path}.
        """

        def scan_level():
            b = Box()
            for level1 in self.iterdir():
                if not level1.stem.startswith('.') or hidden:
                    if level1.is_file():
                        if option is Path.Option.FILES:
                            b[level1.stem] = level1
                    else:
                        b[level1.stem] = {}
                        for level2 in level1.iterdir():
                            if not level2.stem.startswith('.') or hidden:
                                if level2.is_file():
                                    if option is Path.Option.FILES:
                                        b[level1.stem][level2.stem] = level2
                                else:
                                    b[level1.stem][level2.stem] = {}
                                    for level3 in level2.iterdir():
                                        if not level3.stem.startswith('.') or hidden:
                                            if level3.is_file():
                                                if option is Path.Option.FILES:
                                                    b[level1.stem][level2.stem][level3.stem] = level3
                                            else:
                                                b[level1.stem][level2.stem][level3.stem] = {}
                                                for level4 in level3.iterdir():
                                                    if not level3.stem.startswith('.') or hidden:
                                                        if level4.is_file():
                                                            if option is Path.Option.FILES:
                                                                b[level1.stem][level2.stem][level3.stem][level4.stem] \
                                                                    = level4
                                                if not b[level1.stem][level2.stem][level3.stem]:
                                                    b[level1.stem][level2.stem][level3.stem] = level3
                                    if not b[level1.stem][level2.stem]:
                                        b[level1.stem][level2.stem] = level2
                        if not b[level1.stem]:
                            b[level1.stem] = level1
            return b

        def scan_dir():
            s = f'*.{suffix.value}' if suffix is not Path.Suffix.NO_SUFFIX else '*'
            both = Box({Path(item).stem: Path(item) for item in self.glob(s)
                        if not item.stem.startswith('.') or hidden})
            if option is Path.Option.BOTH:
                return both
            if option is Path.Option.FILES:
                return Box({key: value for key, value in both.items() if value.is_file()})
            if option is Path.Option.DIRS:
                return Box({key: value for key, value in both.items() if value.is_dir()})

        rv = scan_level() if level else scan_dir()
        if output is Path.Output.LIST:
            return list(rv.values())
        if frozen:
            return rv.frozen
        return rv

    @property
    def scripts(self) -> List:
        if self.name == 'scripts':
            scripts = self
        else:
            scripts = self / 'scripts'

        if scripts.is_dir():
            if self.scripts_suffix:
                return [item for item in scripts.iterdir() if item.suffix.endswith(Path.Suffix.BASH.value)
                        or item.suffix.endswith(Path.Suffix.SH.value)]
            return [item for item in scripts.iterdir()]
        return list()

    @property
    def scripts_relative(self) -> List:
        scripts = self.scripts
        return [item.relative_to(self.project).text for item in scripts] if scripts else list()

    def description(self) -> Text:
        """
        Create README.md for project.

        Returns:
            Text:
        """
        readme = self.readme()
        try:
            return readme.splitlines()[0].strip('# ')
        except IndexError as exc:
            path.log.error(f'Invalid first line {exc} for README.md: {readme}')
            return str()

    def readme(self) -> Text:
        """
        Create or Read README.md for project.

        Returns:
            Path:
        """
        readme = self / 'README.md'
        if not readme.is_file():
            readme.write_text(f'# {self.name.capitalize()}')
            path.log.debug(f'README.md created: {readme}')
        return readme.read_text()

    @property
    def str(self) -> Text:
        return self.text

    def touch_add(self, name, mode=0o600, exist_ok=True) -> Path:
        """
        Add file, touch and return new Path.

        Args:
            name: name
            mode: mode
            exist_ok: exist_ok

        Returns:
            Path:
        """
        if (p := (self / name).resolved).is_file() is False:
            p.touch(mode=mode, exist_ok=exist_ok)
        return p

    @property
    def text(self):
        return str(self)


PathLike.register(Path)
UnionPaths = Union[PathLike, Pathlib, Path]
UnionPathsText = Union[PathLike, Pathlib, Path, Text]
UnionPathText = Union[Path, Text]
OptionalPath = Optional[Path]
OptionalPaths = Optional[UnionPaths]
OptionalPathText = Optional[UnionPathText]
FinalPath = Final[Path]


def paths(file: Text) -> Path:
    package_path = Path(file).resolved.parent
    installed = Frame().installed(package_path)
    work = User.home.mkdir_add(f'.{package_path.name}')
    prefix = f'{package_path.name.upper()}_'
    env = Env(prefix=prefix)

    try:
        package_path.attrs_set(
            package=package_path, repo=package_path.name, project=package_path.parent, installed=installed,
            prefix=prefix, work=work, env=env,
            log=Logr.get_log(name=package_path.name, p=work.mkdir_add('log') / f'{package_path.name}.log',
                             stream=env.log_level, installed=installed),
            git=GitHub(package_path.parent)
        )
    except git.exc.InvalidGitRepositoryError as exc:
        package_path.log.debug(f'Invalid Git Repo: {dbg(exc)}')
    return package_path


@dataclasses.dataclass
class IpPort:
    """
    Open Ports Class.

    Examples:

    """
    down: Path = 'ips_down.txt'
    invalid: Path = 'ips_invalid.txt'
    open: Path = 'ips_open.json'
    sem: Sem = Sem()

    @staticmethod
    def ip_port_tuple(port: UnionTextInt = 27017, ip: typing.Text = LOCALHOST) -> Tuple:
        return ip, port

    @staticmethod
    async def is_global_ip(ip: Text, semaphore: Sem = sem, p: Path = None) -> OptionalBool:
        """
        Checks if Valid and Global IP.

        Args:
            ip: ip.
            semaphore: semaphore.
            p: path to save invalid IP.

        Returns:
            OptionalBool:
        """
        async with semaphore.max:
            async with semaphore.os:
                try:
                    ip_address = await executor(ipaddress.ip_address, ip)
                    if ip_address.is_global:
                        return True
                except ValueError:
                    pass
                if p:
                    p = p.touch_add(IpPort.invalid)
                    p.append_text(f'{ip}\n')
                return None

    @staticmethod
    async def ping(ip: Text, semaphore: Sem = sem, p=None) -> OptionalBool:
        """
        Pings host.

        Args:
            ip: ip.
            semaphore: semaphore.
            p: path to save invalid IPs.

        Returns:
            OptionalBool:
        """
        pings = 3
        rv = None
        if await IpPort.is_global_ip(ip, semaphore, p):
            async with semaphore.max:
                async with semaphore.ping:
                    rc = await aiocmd(f'sudo ping -c {pings} {ip}', False, True)
                    if rc == 0:
                        rv = True
                    elif rc == 2:
                        rv = False
                    else:
                        rv = None
            if p and not rv:
                p = p.touch_add(IpPort.down)
                p.append_text(f'{ip}\n')
        return rv

    @staticmethod
    async def is_port_proto_open(port: UnionTextInt = 27017, ip: Text = LOCALHOST, proto: Text = PROTO_NAME.tcp,
                                 status: Bool = False, semaphore: Sem = sem,
                                 p: Path = None) -> Union[Bool, ProtoStatus]:
        """
        Port Open.

        Args:
            port: port.
            ip: host ip.
            proto: proto.
            status: return only bool or tuple with all values.
            semaphore: semaphore.
            p: path to save invalid IPs and ip down.

        Returns:
            Union[Bool, ProtoStatus]: True if open (process listing on port).
        """

        ip_port = IpPort.ip_port_tuple(port, ip)
        if await IpPort.ping(ip, semaphore, p):
            async with semaphore.max:
                async with semaphore.socket:
                    try:
                        if proto == PROTO_NAME.tcp:
                            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                                res = s.connect_ex(ip_port)
                        else:
                            res = os.system(f'nc -vnzu "{ip}" "{port}" > /dev/null 2>&1')
                        if status:
                            return ProtoStatus(ip, port, proto, not bool(res))
                        return not bool(res)
                    except OSError as exception:
                        await path.log.adebug(fm(ip, port, proto, exception))

    @staticmethod
    async def which_open(ip: Text = LOCALHOST, semaphore: Sem = sem, log: Logr = None, p: Path = None) -> UnionDictList:
        """
        Scan host or hosts.

        Args:
            ip: host or hosts.
            semaphore: semaphore.
            log: logger.
            p: path to store json output, invalid IPs and IPs down.

        Returns:
            UnionDictList:
        """
        import tqdm.asyncio
        if p:
            (p / IpPort.invalid).rm()
            (p / IpPort.down).rm()

        rv = dict()
        if text := isinstance(ip, str):
            ip = list(ip)
            rv = list()

        tcp_task = tuple(IpPort.is_port_proto_open(port, i, status=True, semaphore=semaphore)
                         for i in ip for port in ALL_PORTS)
        udp_task = tuple(IpPort.is_port_proto_open(port, i, PROTO_NAME.udp, True, semaphore)
                         for i in ip for port in ALL_PORTS)

        ip_status = list()
        # FIXME:
        pbar = tqdm.asyncio.tqdm()
        previous_ip = str()
        for f in pbar.as_completed(tcp_task + udp_task):
            port_status = await f
            ip_status.append(port_status)
            if port_status.ip != previous_ip:
                pbar.set_description(port_status)
                if log:
                    log.info(f'Open Completed: {port_status.ip}')
                previous_ip = port_status.ip

        for port_status in ip_status:
            ip_ports = dict()
            if port_status.tcp:
                ip_ports[PROTO_NAME.tcp] = port_status.port
            if port_status.udp:
                ip_ports[PROTO_NAME.udp] = port_status.port
            if ip_ports and text:
                rv.append(ip_ports)
            elif ip_ports and text is False:
                rv.update({port_status.ip: ip_ports})

        p = p.touch_add(IpPort.open)
        with p.open(mode='w') as f:
            f.write(json.dumps(rv, indent=4, sort_keys=True))
        return rv


class PostDevelopCommand(setuptools.command.develop.develop):
    """Post-installation for development mode."""
    function = None

    # Pre Install.

    def run(self):
        # Post Install.
        if self.function:
            self.function()
        setuptools.command.develop.develop.run(self)


class PostInstallCommand(setuptools.command.install.install):
    """Post-installation for installation mode."""
    function = None

    # Pre Install.

    def run(self):
        # Post Install.
        if self.function:
            self.function()
        setuptools.command.install.install.run(self)


@dataclasses.dataclass
class Py:
    """Python Server Information Class."""
    python_version: Tuple[Int] = platform.python_version_tuple()
    PY2: Bool = True if int(python_version[0]) == 2 else False
    PY3: Bool = True if int(python_version[0]) == 3 else False
    PY39: Bool = True if PY3 and int(python_version[1]) == 9 else False
    PY38: Bool = True if PY3 and int(python_version[1]) == 8 else False
    PY37: Bool = True if PY3 and int(python_version[1]) == 7 else False
    exe_path: Path = Path(sys.executable).resolved
    exe_name: Text = exe_path.name
    sys_prefix: Path = Path(sys.base_prefix).resolved
    exe_prefix: Path = Path(sys.prefix).resolved
    sys_site: Path = sys_prefix / 'lib' / exe_name / 'site-packages'
    exe_site: Path = exe_prefix / 'lib' / exe_name / 'site-packages'
    VENV: Bool = True if sys_prefix != exe_prefix else False


class Simple(types.SimpleNamespace):
    @classmethod
    def simple(cls, name: Any, _extend: Extend = Extend.DICT, **kwargs) -> Any:
        """
        Creates a New Simple Namespace Sub Class.

        Default returns a Simple Namespace with `Asdict` base.

        Warnings:
            Call `extend` as positional argument.

        Args:
            name: class name or Namespace Sub Class.
            _extend: add to default bases.
            **kwargs: kwargs

        Raises:
            ValueError: ValueError

        Returns:
            Any:
        """
        if isinstance(name, str):
            if (_extend := kwargs.get('_extend', _extend)) is not _extend:
                del kwargs['_extend']
            name = types.new_class(name, bases=tuple({*Extend.DICT.value, *_extend.value, cls, }))
            if not kwargs:
                return name

        if kwargs:
            return name(**kwargs)
        else:
            raise ValueError(f'kwargs: must be provided for cls: {name}.')


@dataclasses.dataclass
class System(Distro, Executable, Machine, Py):  # type: ignore
    """Distro, Executable/Commands Installed, Server OS, Platform and Python Information Class."""
    pass


class Up:
    """APP/CLI Option."""
    Bump: Any = Literal['patch', 'minor', 'major']

    @classmethod
    def args(cls):
        return cls.Bump.__args__

    @classmethod
    def option(cls):
        return typer.Option(cls.args()[0], help='Version part to be increased.', autocompletion=cls.args)


@app.command()
def up(bump: Text = Up.option()):
    """
    Project Upgrade.

    Args:
        bump: Part of version to increase.
    """
    if Distro.MACOS:
        os.system(f'{path.repo} --version && upload.sh {bump} {path.repo} && '
                  f'{path.repo} --version')
    elif Distro.KALI:
        os.system(f'{path.repo} --version && upgrade.sh {path.repo} && '
                  f'{path.repo} --version')


class Url(furl.furl):
    """
    Furl Class.

    GitHub repositories http
    Github repos ssh
    Go
    Api Rest
    Repo test and prod
    Ports and Docker host

    Examples:
        >>> assert Url.email(os.environ.get('USER')) == Url.email(User.name)
        >>> Url.github()
        Url('https://github.com')
        >>> Url.wiki(number=183238657, page='Hola')
        Url('https://nferx.atlassian.net/wiki/spaces/DevOps/pages/183238657/Hola')
        >>> Url.lumenbiomics(repo='test')
        'org-4379404@github.com:lumenbiomics/test'
        >>> http_url = Url.lumenbiomics(http=True, repo='test', username=User.github_username, password='password')
        >>> url = f'{Url.scheme_default}://{User.github_username}:password@{Url.github().host}/{Url.organization}/test'
        >>> assert http_url.url == url
        >>> repo = Url(host=Url.nferx(), name='repotest', bind=9091)
        >>> repo.url
        'https://repotest.nferx.com'
        >>> url = Url(host=repo, name='nexus', port=8080, bind=3001)
        >>> url.url, url.name, url.bind
        ('https://nexus.repotest.nferx.com:8080', 'nexus', 3001)
    """
    Domain: Any = collections.namedtuple('Domain', 'nference nferxops nferx')
    domain: Domain = Domain('nference.net', 'nferxops.net', 'nferx.com')
    bind: Int = None
    company: Text = domain.nference
    container: Int = None
    group: Text = 'DevOps'
    id: Text = 'org-4379404'
    ops: Text = domain.nferxops
    organization: Text = 'lumenbiomics'
    scheme_default: Text = 'https'
    server: Text = domain.nferx

    def __init__(self, host: Union[Text, furl.furl, Url], name: Text = None, **kwargs):
        if not kwargs.get('scheme', None):
            kwargs.update(scheme=self.scheme_default)
        self.bind, kwargs = pop_default(kwargs, 'bind')
        self.container, kwargs = pop_default(kwargs, 'container')
        host = host.host if isinstance(host, Url) else host
        prefix = f'{name}.' if name else str()
        kwargs.update(host=f'{prefix}{host.host if isinstance(host, Url) else host}')
        super(Url, self).__init__(**kwargs)

    @staticmethod
    @app.command()
    def email(username: Text = str(), stdout: bool = False) -> Text:
        """
        User Email.

        Args:
            username: username.
            stdout: stdout.

        Returns:
            Text:
        """
        username = username if username else User.name
        rv = f'{username}@{Url.nference().host}'
        if stdout:
            console.print(rv)
        return rv

    @staticmethod
    @app.command()
    def github(stdout: Bool = False) -> Url:
        """
        GitHub Url.

        Args:
            stdout: stdout.

        Returns:
            Url:
        """
        rv = Url('github.com')
        if stdout:
            console.print(rv.url)
        return rv

    @staticmethod
    @app.command()
    def lumenbiomics(http: Bool = False, username: Text = None, password: Text = None,
                     repo: Text = None, suffix: Bool = False, stdout: Bool = False) -> Union[Url, Text]:
        """
        Lumenbiomics repos url.

        Args:
            http: http
            username: username
            password: GitHub API token
            repo: repo
            suffix: suffix
            stdout: stdout.

        Returns:
            Any:
        """
        repo = repo if repo else path.repo
        password = password if password else Url.token()
        g = '.git' if suffix else str()
        p = '/'.join((Url.organization, repo)) + g

        if http:
            # https://jose-nferx:<api_token>@github.com/lumenbiomics/configs.git
            rv = Url(Url.github(), **dict(path=f'{p}', **(
                dict(username=username, password=password) if password and username else dict())))
            if stdout:
                console.print(rv.url)
            return rv
        rv = f'{Url.id}@{Url.github().host}:{p}'  # org-4379404@github.com:lumenbiomics/repos.git
        if stdout:
            console.print(rv)
        return rv

    @property  # type: ignore
    def name(self) -> Text:
        """
        Last path or first subdomain.

        Returns:
            Text:
        """
        return self.path.split('/')[-1] if self.path else self.host.split('.')[0]

    @staticmethod
    @app.command()
    def nference(stdout: Bool = False) -> Url:
        """
        Nferx Url.

        Args:
            stdout: stdout.

        Returns:
            Url:
        """
        rv = Url(Url.company)
        if stdout:
            console.print(rv.url)
        return rv

    @staticmethod
    @app.command()
    def nferx(stdout: Bool = False) -> Url:
        """
        Nferx Url.

        Args:
            stdout: stdout.

        Returns:
            Url:
        """
        rv = Url(Url.server)
        if stdout:
            console.print(rv.url)
        return rv

    @staticmethod
    @app.command()
    def nferxops(stdout: Bool = False) -> Url:
        """
        Nferx Url.

        Args:
            stdout: stdout.

        Returns:
            Url:
        """
        rv = Url(Url.ops)
        if stdout:
            console.print(rv.url)
        return rv

    @staticmethod
    @app.command()
    def repo(stdout: Bool = False) -> Url:
        """
        Repo Url.

        Args:
            stdout: stdout.

        Returns:
            Url:
        """
        rv = Url(host=Url.nferx(), name='repo')
        if stdout:
            console.print(rv.url)
        return rv

    @staticmethod
    @app.command()
    def repository(stdout: Bool = False) -> Url:
        """
        Repository repo Url.

        Args:
            stdout: stdout.

        Returns:
            Url:
        """
        rv = Url.repo() / 'repository'
        if stdout:
            console.print(rv.url)
        return rv

    @staticmethod
    @app.command()
    def repotest(stdout: Bool = False) -> Url:
        """
        Repotest Url.

        Args:
            stdout: stdout.

        Returns:
            Url:
        """
        rv = Url(host=Url.nferx(), name='repotest')
        if stdout:
            console.print(rv.url)
        return rv

    @staticmethod
    @app.command()
    def repositorytest(stdout: Bool = False) -> Url:
        """
        Repository repotest Url.

        Args:
            stdout: stdout.

        Returns:
            Url:
        """
        rv = Url.repotest() / 'repository'
        if stdout:
            console.print(rv.url)
        return rv

    @staticmethod
    @app.command()
    def token(stdout: Bool = False) -> Url:
        """
        Repository repotest Url.

        Args:
            stdout: stdout.

        Returns:
            Url:
        """
        rv = os.environ.get('NFERX_GITHUB_PASSWORD', str())
        if stdout:
            console.print(rv)
        return rv

    @staticmethod
    @app.command()
    def wiki(space: Text = group, number: Int = int(), page: Text = str(), stdout: Bool = True) -> Url:
        """
        Confluence Wiki Url.

        https://nferx.atlassian.net/wiki/spaces/DevOps/pages/183238657/Repository+Manager

        Args:
            space: space
            number: number
            page: page
            stdout: stdout

        Returns:
            Any:
        """
        name = Url.nferx().name
        p = f'wiki/spaces/{space}/pages/{number}/{page.replace(" ", "+")}' if number and page else 'wiki'
        rv = Url('atlassian.net', name=name, path=p)
        if stdout:
            console.print(rv.url)
        return rv


@dataclasses.dataclass
class UserActual:
    """User Base."""
    name: Text = Path('/dev/console').owner() if psutil.MACOS else os.getlogin()
    passwd: Any = dataclasses.field(default=pwd.getpwnam(name), init=False)
    gecos: Any = dataclasses.field(default=passwd.default.pw_gecos, init=False)
    gid: Any = dataclasses.field(default=passwd.default.pw_gid, init=False)
    gname: Any = dataclasses.field(default=grp.getgrgid(gid.default).gr_name, init=False)
    home: Any = dataclasses.field(default=Path(passwd.default.pw_dir), init=False)
    id: Any = dataclasses.field(default=passwd.default.pw_uid, init=False)
    shell: Any = dataclasses.field(default=Path(passwd.default.pw_shell), init=False)
    ssh: Any = dataclasses.field(default=home.default / '.ssh', init=False)
    id_rsa: Any = dataclasses.field(default=ssh.default / 'id_rsa', init=False)
    id_rsa_pub: Any = dataclasses.field(default=ssh.default / 'id_rsa.pub', init=False)
    auth_keys: Any = dataclasses.field(default=ssh.default / 'authorized_keys', init=False)
    git_config_path: Any = dataclasses.field(default=home.default / '.gitconfig', init=False)
    git_config: Any = dataclasses.field(default=git.GitConfigParser(git_config_path.default.text), init=False)
    github_username: Any = dataclasses.field(default=git_config.default.get_value(section='user', option='username',
                                                                                  default=str()), init=False)
    GITHUB_USERNAME: Any = True if github_username else False

    def __post_init__(self):
        try:
            self.passwd = pwd.getpwnam(self.name)
        except KeyError:
            red(f'Invalid user: {self.name}')
        else:
            self.gecos = self.passwd.pw_gecos
            self.gid = self.passwd.pw_gid
            self.gname = grp.getgrgid(self.gid).gr_name
            self.home = Path(self.passwd.pw_dir)
            self.id = self.passwd.pw_uid
            self.shell = Path(self.passwd.pw_shell)
            self.ssh = self.home / '.ssh'
            self.id_rsa = self.ssh / 'id_rsa'
            self.id_rsa_pub = self.ssh / 'id_rsa.pub'
            self.auth_keys = self.ssh / 'authorized_keys'
            self.git_config_path = self.home / '.gitconfig'
            self.git_config = git.GitConfigParser(self.git_config_path.text)
            self.github_username = self.git_config.get_value(section='user', option='username', default=str())
            self.GITHUB_USERNAME = True if self.github_username else False


@dataclasses.dataclass
class UserProcess:
    """User Process Class."""
    sudo_user: Text = os.getenv('SUDO_USER')
    SUDO: Bool = True if sudo_user is not None else False
    gid: Int = os.getgid()
    gname: Text = grp.getgrgid(gid).gr_name
    id: Int = os.getuid()
    passwd: pwd.struct_passwd = pwd.getpwuid(id)
    gecos: Text = pwd.getpwuid(id).pw_gecos
    home: Path = Path(pwd.getpwuid(id).pw_dir)
    name: Text = pwd.getpwuid(id).pw_name
    shell: Path = Path(pwd.getpwuid(id).pw_shell)
    ssh: Path = home / '.ssh'
    id_rsa: Path = ssh / 'id_rsa'
    id_rsa_pub: Path = ssh / 'id_rsa.pub'
    auth_keys: Path = ssh / 'authorized_keys'
    ROOT: Bool = True if id == 0 else False
    git_config_path = home / '.gitconfig'
    git_config: git.GitConfigParser = git.GitConfigParser(git_config_path.text)
    github_username: Text = git_config.get_value(section='user', option='username', default=str())
    GITHUB_USERNAME: Bool = True if github_username else False


@dataclasses.dataclass
class User:
    """User Class."""
    username: Text = 'upload'
    admin: Any = collections.namedtuple('UserNamed', 'username password', defaults=(
        'admin', os.environ.get('REPO_DEFAULT_ADMIN_PASSWORD', str())))
    default: Any = admin(username, username)
    actual: Final[UserActual] = UserActual()
    process: Final[UserProcess] = UserProcess()
    ROOT: Bool = process.ROOT
    SUDO: Bool = process.SUDO
    sudo_user: Text = process.sudo_user
    passwd: pwd.struct_passwd = process.passwd if SUDO else actual.passwd
    gecos: Text = process.gecos if SUDO else actual.gecos
    gid: Int = process.gid if SUDO else actual.gid
    gname: Text = process.gname if SUDO else actual.gname
    home: Path = process.home if SUDO else actual.home
    id: Int = process.id if SUDO else actual.id
    name: Text = process.name if SUDO else actual.name
    shell: Path = process.shell if SUDO else actual.shell
    ssh: Path = process.ssh if SUDO else actual.ssh
    id_rsa: Path = process.id_rsa if SUDO else actual.id_rsa
    id_rsa_pub: Path = process.id_rsa_pub if SUDO else actual.id_rsa_pub
    auth_keys: Path = process.auth_keys if SUDO else actual.auth_keys
    git_config_path: Path = process.git_config_path if SUDO else actual.git_config_path
    git_config: git.GitConfigParser = process.git_config if SUDO else actual.github_username
    github_username: Text = process.github_username if SUDO else actual.github_username
    GITHUB_USERNAME: Bool = process.GITHUB_USERNAME if SUDO else actual.GITHUB_USERNAME


path = paths(__file__)

__all__ = [item for item in globals() if not item.startswith('_') and not inspect.ismodule(globals().get(item))]

for global_var, global_value in os.environ.items():
    # noinspection PyStatementEffect
    globals()[global_var] = global_value
    __all__.append(global_var)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        app()
    else:
        app(sys.argv[1:])
