"""System utility functions."""

import errno
import logging
import os
import shutil
import subprocess
import sys
from typing import Optional, Union

import sparv.core.paths as paths

log = logging.getLogger(__name__)


def kill_process(process):
    """Kill a process, and ignore the error if it is already dead."""
    try:
        process.kill()
    except OSError as exc:
        if exc.errno == errno.ESRCH:  # No such process
            pass
        else:
            raise


def clear_directory(path):
    """Create a new empty dir.

    Remove it's contents if it already exists.
    """
    shutil.rmtree(path, ignore_errors=True)
    os.makedirs(path, exist_ok=True)


def call_java(jar, arguments, options=[], stdin="", search_paths=(),
              encoding=None, verbose=False, return_command=False):
    """Call java with a jar file, command line arguments and stdin.

    Returns a pair (stdout, stderr).
    If the verbose flag is True, pipes all stderr output to stderr,
    and an empty string is returned as the stderr component.

    If return_command is set, then the process is returned.
    """
    assert isinstance(arguments, (list, tuple))
    assert isinstance(options, (list, tuple))
    jarfile = find_binary(jar, search_paths, executable=False)
    # For WSD: use = instead of space in arguments
    # TODO: Remove when fixed!
    if isinstance(arguments[0], tuple):
        arguments = ["{}={}".format(x, y) for x, y in arguments]
    java_args = list(options) + ["-jar", jarfile] + list(arguments)
    return call_binary("java", arguments=java_args, stdin=stdin,
                       search_paths=search_paths, encoding=encoding,
                       verbose=verbose, return_command=return_command)


def call_binary(name, arguments=(), stdin="", raw_command=None, search_paths=(), encoding=None, verbose=False,
                use_shell=False, allow_error=False, return_command=False):
    """Call a binary with arguments and stdin, return a pair (stdout, stderr).

    If the verbose flag is True, pipes all stderr output from the subprocess to
    stderr in the terminal, and an empty string is returned as the stderr component.

    If return_command is set, then the process is returned.
    """
    from subprocess import Popen, PIPE
    assert isinstance(arguments, (list, tuple))
    assert isinstance(stdin, (str, list, tuple))

    binary = find_binary(name, search_paths)
    if raw_command:
        use_shell = True
        command = raw_command % binary
        if arguments:
            command = " ".join([command] + arguments)
    else:
        command = [binary] + [str(a) for a in arguments]
    if isinstance(stdin, (list, tuple)):
        stdin = "\n".join(stdin)
    if encoding is not None and isinstance(stdin, str):
        stdin = stdin.encode(encoding)
    log.info("CALL: %s", " ".join(str(c) for c in command) if not raw_command else command)
    command = Popen(command, shell=use_shell,
                    stdin=PIPE, stdout=PIPE,
                    stderr=(None if verbose else PIPE),
                    close_fds=False)
    if return_command:
        return command
    else:
        stdout, stderr = command.communicate(stdin)
        if not allow_error and command.returncode:
            if stdout:
                log.info(stdout.decode())
            if stderr:
                log.warning(stderr.decode())
            raise OSError("%s returned error code %d" % (binary, command.returncode))
        if encoding:
            stdout = stdout.decode(encoding)
            if stderr:
                stderr = stderr.decode(encoding)
        return stdout, stderr


def find_binary(name: Union[str, list], search_paths=(), executable: bool = True, allow_dir: bool = False,
                raise_error: bool = False) -> Optional[str]:
    """Search for the binary for a program.

    Args:
        name: Name of the binary, either a string or a list of strings with alternative names.
        search_paths: List of paths where to look, in addition to the environment variable PATH.
        executable: Set to False to not fail when binary is not executable.
        allow_dir: Set to True to allow the target to be a directory instead of a file.
        raise_error: Raise error if binary could not be found.

    Returns:
        Path to binary, or None if not found.
    """
    if isinstance(name, str):
        name = [name]
    name = list(map(os.path.expanduser, name))
    search_paths = list(search_paths) + ["."] + [paths.bin_dir] + os.getenv("PATH").split(":")
    search_paths = list(map(os.path.expanduser, search_paths))

    # Use 'which' first
    for binary in name:
        if not os.path.dirname(binary) == "":
            continue
        path_to_bin = shutil.which(binary)
        if path_to_bin:
            return path_to_bin

    # Look for file in paths
    for directory in search_paths:
        for binary in name:
            path_to_bin = os.path.join(directory, binary)
            if os.path.isfile(path_to_bin) or (allow_dir and os.path.isdir(path_to_bin)):
                if executable and not allow_dir:
                    assert os.access(path_to_bin, os.X_OK), "Binary is not executable: %s" % path_to_bin
                return path_to_bin

    if raise_error:
        raise LookupError("Couldn't find binary: %s\nSearched in: %s\nFor binary names: %s" %
                          (name[0], ", ".join(search_paths), ", ".join(binary)))
    else:
        return None


def rsync(local, host, remote=None):
    """Transfer files and/or directories using rsync.

    When syncing directories, extraneous files in destination dirs are deleted.
    """
    if remote is None:
        remote = local
    if os.path.isdir(local):
        remote_dir = os.path.dirname(remote)
        log.info("Copying directory: %s => %s", local, remote)
        args = ["--recursive", "--delete", "%s/" % local]
    else:
        remote_dir = os.path.dirname(remote)
        log.info("Copying file: %s => %s", local, remote)
        args = [local]
    subprocess.check_call(["ssh", host, "mkdir -p '%s'" % remote_dir])
    subprocess.check_call(["rsync"] + args + ["%s:%s" % (host, remote)])
