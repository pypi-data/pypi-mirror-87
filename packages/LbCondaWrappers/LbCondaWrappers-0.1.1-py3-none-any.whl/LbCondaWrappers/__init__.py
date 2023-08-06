###############################################################################
# (c) Copyright 2018 CERN                                                     #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
from __future__ import print_function

import argparse
from collections import defaultdict
from datetime import datetime
from io import open
import logging
import pipes
import os
from os.path import basename, isdir, join, relpath
import re
import stat
import subprocess
import sys
import tempfile

INSTALL_ROOT = "/cvmfs/lhcbdev.cern.ch/conda"
TEXLIVE_ROOT = "/cvmfs/lhcbdev.cern.ch/tools/texlive/"
ENVS_ROOT = join(INSTALL_ROOT, "envs")
CONDA_CMD = join(INSTALL_ROOT, "miniconda/linux-64/prod/bin/conda")
LHCB_ETC = "/cvmfs/lhcb.cern.ch/etc/grid-security"
ENV_VAR_WHITELIST = [
    # General unix
    r"DISPLAY",
    r"EDITOR",
    r"HOME",
    r"HOSTNAME",
    r"KRB5.*",
    r"LANG",
    r"LC_.*",
    r"TERM",
    r"TMPDIR",
    r"TZ",
    r"USER",
    r"VISUAL",
    # HEP specific
    r"VOMS_.*",
    r"X509_.*",
    r"XRD_.*",
    # LHCb specific
    r"MYSITEROOT",
]
ENV_VAR_WHITELIST = re.compile(r"^(" + r"|".join(ENV_VAR_WHITELIST) + r")$")

logging.getLogger().setLevel(logging.INFO)


def list_textlive_versions():
    versions = []
    if isdir(TEXLIVE_ROOT):
        for version in os.listdir(TEXLIVE_ROOT):
            try:
                versions.append(int(version))
            except Exception:
                pass
    return sorted(versions)


def list_environments(subdir="linux-64"):
    envs = defaultdict(dict)
    for dirpath, dirnames, filenames in os.walk(ENVS_ROOT, topdown=True):
        if subdir in dirnames:
            split_dirpath = relpath(dirpath, ENVS_ROOT).split(os.sep)
            if len(split_dirpath) < 2:
                sys.stderr.write("ERROR: Invalid environment found (%s)" % dirpath)
                sys.stderr.flush()
                continue
            env_name = "/".join(split_dirpath[:-1])
            env_version = split_dirpath[-1]
            envs[env_name][env_version] = join(dirpath, subdir)
            # Avoid searching any deeper in the tree
            dirnames[:] = []

    # Add the short versions with YYYY-MM-DD instead of YYYY-MM-DD_HH-MM
    display_versions = defaultdict(list)
    for env in envs:
        versions = defaultdict(list)
        for long_version, env_path in sorted(envs[env].items()):
            short_version = datetime.strptime(long_version, "%Y-%m-%d_%H-%M").strftime(
                "%Y-%m-%d"
            )
            envs[env][short_version] = env_path
            versions[short_version].append(long_version)

        for short_version, long_versions in versions.items():
            if len(long_versions) == 1:
                display_versions[env].append(short_version)
            else:
                display_versions[env].extend(long_versions)

    return envs, display_versions


CONDA_ENVIRONMENTS, DISPLAY_VERSIONS = list_environments()


def get_env_prefix(env_string):
    if env_string in CONDA_ENVIRONMENTS:
        env_name = env_string
        env_version = max(CONDA_ENVIRONMENTS[env_string])
    else:
        split_dirpath = env_string.split(os.sep)
        env_name = "/".join(split_dirpath[:-1])
        env_version = split_dirpath[-1]

        if env_name not in CONDA_ENVIRONMENTS:
            sys.stderr.write(
                "ERROR: No environment found named " + env_name + "\n"
                'Did you mean to start the command with "lb-conda default"?\n'
            )
            sys.exit(30)

        env_version = split_dirpath[-1]
        if env_version not in CONDA_ENVIRONMENTS[env_name]:
            sys.stderr.write(
                "ERROR: No version " + env_version + " found for " + env_name + "\n"
            )
            sys.exit(31)

    return CONDA_ENVIRONMENTS[env_name][env_version]


def call_in_conda(command, env_prefix, *, with_venv=None, texlive=None):
    """Replace the current process with a command in the conda environment

    If the command is successfully executed this function will never return.
    """
    env = {k: v for k, v in os.environ.items() if ENV_VAR_WHITELIST.match(k)}
    with tempfile.NamedTemporaryFile(mode="wt", delete=False) as bashrc:
        logging.debug("Writing bashrc to %s", bashrc.name)
        if texlive:
            bashrc.write(
                "\n".join(
                    [
                        f"export PATH={TEXLIVE_ROOT}/{texlive}/bin/x86_64-linux${{PATH+:${{PATH}}}}",
                        f"export MANPATH={TEXLIVE_ROOT}/{texlive}/texmf-dist/doc/man${{MANPATH+:${{MANPATH}}}}",
                        f"export INFOPATH={TEXLIVE_ROOT}/{texlive}/texmf-dist/doc/info${{INFOPATH+:${{INFOPATH}}}}",
                        # Always end with a new line
                        "",
                    ]
                )
            )

        bashrc.write(
            "\n".join(
                [
                    'eval "$({} shell.bash hook)"'.format(pipes.quote(CONDA_CMD)),
                    "conda activate {}".format(pipes.quote(env_prefix)),
                    "unset BASH_ENV",
                    'source "{}"'.format(with_venv) if with_venv else "",
                    "rm {}".format(pipes.quote(bashrc.name)),
                    # Always end with a new line
                    "",
                ]
            )
        )

    env["BASH_ENV"] = bashrc.name
    if isdir(LHCB_ETC):
        env["VOMS_USERCONF"] = env.get("VOMS_USERCONF", join(LHCB_ETC, "vomses"))
        env["X509_CERT_DIR"] = env.get("X509_CERT_DIR", join(LHCB_ETC, "certificates"))
        env["X509_VOMS_DIR"] = env.get("X509_VOMS_DIR", join(LHCB_ETC, "vomsdir"))
        env["X509_VOMSES"] = env.get("X509_VOMSES", join(LHCB_ETC, "vomses"))

    if basename(command[0]) == "bash":
        exec_command = "exec bash --norc --noprofile"
        for c in command[1:]:
            exec_command += " " + pipes.quote(c)
    elif basename(command[0]) in ["sh", "ksh", "csh", "tcsh", "zsh", "fish"]:
        raise NotImplementedError(
            "Unable to launch %s as only bash is supported for now"
            % basename(command[0]),
        )
    else:
        exec_command = " ".join(pipes.quote(x) for x in command)

    logging.debug("Running command %s", exec_command)
    sys.stdout.flush()
    sys.stderr.flush()
    os.execvpe("bash", ["bash", "--norc", "--noprofile", "-c", exec_command], env)


def lb_conda():
    """Invoke a commands in the correct environment"""
    parser = argparse.ArgumentParser(
        usage="lb-conda [-h] [--list] [--texlive] [--texlive-version=2020] [--export] env_name[/version] [command] ...",
        description="Run a command in a conda based environment",
    )
    parser.add_argument("--list", action="store_true", help="List available versions")
    parser.add_argument(
        "--export",
        action="store_true",
        help="List installed packages in conda's environment.yaml format",
    )
    parser.add_argument(
        "--texlive",
        action="store_true",
        help="Layer the latest available texlive into the environment",
    )
    parser.add_argument(
        "--texlive-version",
        type=int,
        choices=list_textlive_versions(),
        help="The version of texlive to use, implies --texlive.",
    )
    # argparse doesn't support optional positional arguments so use metavar to
    # set the help text
    positional_help_text = (
        "env_name  required, the name of the environment run\n  "
        "command   optional, the command to run (default: bash)\n  "
        "...       optional, any additional arguments"
    )
    parser.add_argument(
        "command",
        metavar=positional_help_text,
        default=["bash"],
        nargs=argparse.REMAINDER,
    )
    args = parser.parse_args()

    if args.command:
        env_prefix = get_env_prefix(args.command[0])
        command = args.command[1:] or ["bash"]
    else:
        env_prefix = None
        command = None

    if args.texlive_version:
        texlive = args.texlive_version
    elif args.texlive:
        if list_textlive_versions():
            texlive = max(list_textlive_versions())
        else:
            parser.error("There are no versions of texlive available on this host")
    else:
        texlive = None

    if args.list or (len(args.command) >= 2 and args.command[1] == "--list"):
        # Handle --list
        if args.command:
            try:
                print(*sorted(DISPLAY_VERSIONS[args.command[0]]), sep="\n")
                sys.exit(0)
            except KeyError:
                sys.exit(2)
        else:
            print(*DISPLAY_VERSIONS, sep="\n")
            sys.exit(0)

    if env_prefix is None:
        sys.stderr.write(
            "ERROR: No environment name specified\n"
            'Did you mean "lb-conda default"?\n'
        )
        sys.exit(3)

    if args.export or (len(args.command) >= 2 and args.command[1] == "--export"):
        with open(env_prefix + ".yaml", "rt", encoding="utf-8") as fp:
            print(fp.read())
            sys.exit(0)
        sys.exit(0)

    # Try to replace the current process with the desired command
    try:
        call_in_conda(command, env_prefix, texlive=texlive)
    except Exception as e:
        sys.stderr.write("ERROR: %s\n" % e)
        sys.exit(1)


def lb_conda_dev():
    """Invoke a commands in the correct environment"""
    parser = argparse.ArgumentParser(
        usage="lb-conda-dev [-h] [--texlive] [--texlive-version=2020] [--prefix] "
        "[virtual-env|clone] env_name[/version] [directory]",
        description="Created an editable copy of one of the LHCb conda environments",
    )
    parser.add_argument(
        "--texlive",
        action="store_true",
        help="Layer the latest available texlive into the environment",
    )
    parser.add_argument(
        "--texlive-version",
        type=int,
        choices=list_textlive_versions(),
        help="The version of texlive to use, implies --texlive.",
    )

    subparsers = parser.add_subparsers(help="sub-command help")
    venv_parser = subparsers.add_parser(
        "virtual-env",
        help="Create an copy of the environment for use with pip "
        "(recommended, minimal disk requirements)",
    )
    venv_parser.set_defaults(func=_lb_conda_dev_venv)

    clone_parser = subparsers.add_parser(
        "clone",
        help="Create a full clone of the conda environment "
        "(requires a significant amount of disk space)",
    )
    clone_parser.set_defaults(func=_lb_conda_dev_clone)

    for subparser in [venv_parser, clone_parser]:
        subparser.add_argument(
            "env_name",
            help="The name (and optionally version) of the environment to copy",
        )
        subparser.add_argument(
            "directory",
            nargs="?",
            help="The directory to create the environment in",
        )

    parser.add_argument("--with-venv", help=argparse.SUPPRESS)
    parser.add_argument("--execute", nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    args = parser.parse_args()

    if args.texlive_version:
        texlive = args.texlive_version
    elif args.texlive:
        texlive = max(list_textlive_versions())
    else:
        texlive = None

    if args.execute:
        # Try to replace the current process with the desired command
        try:
            call_in_conda(
                args.execute[1:] or ["bash"],
                args.execute[0],
                with_venv=args.with_venv,
                texlive=texlive,
            )
        except Exception as e:
            sys.stderr.write("ERROR: %s\n" % e)
            sys.exit(20)
    elif hasattr(args, "func"):
        env_name = args.env_name
        env_prefix = get_env_prefix(args.env_name)

        directory = args.directory
        if directory is None:
            directory = env_name.replace("/", "-") + "_dev"
        directory = os.path.abspath(directory)

        if isdir(directory):
            sys.stderr.write("ERROR: Directory %s already exists\n\n" % directory)
            sys.exit(10)

        try:
            python_version = int(
                subprocess.check_output(
                    [
                        "lb-conda",
                        env_name,
                        "python",
                        "-c",
                        "import sys; print(sys.version_info.major)",
                    ],
                    universal_newlines=True,
                )
            )
        except Exception:
            sys.stderr.write(
                "ERROR: Failed to find a Python version from %s\n" % env_name
            )
            sys.exit(11)
        else:
            if python_version < 3:
                sys.stderr.write(
                    "ERROR: Python 2 is not supported but was found in %s\n" % env_name
                )
                sys.exit(12)
        args.func(env_name, env_prefix, directory, texlive=texlive)
        sys.stderr.write("Environment created in %s\n" % directory)
        sys.stderr.write(
            '   Execute "%s/run" to launch a shell inside the environment\n' % directory
        )
        sys.stderr.write(
            '   Execute "%s/run my_command" to launch "my_command" inside the environment\n'
            % directory
        )
    else:
        parser.error('Either "virtual-env" or "clone" must be specified')


def _lb_conda_dev_venv(env_name, env_prefix, directory, *, texlive=None):
    subprocess.check_output(
        [
            "lb-conda",
            env_name,
            "python",
            "-m",
            "venv",
            "--system-site-packages",
            directory,
        ],
        universal_newlines=True,
    )
    write_run_script(
        join(directory, "run"),
        env_prefix,
        with_venv=join(directory, "bin", "activate"),
        texlive=texlive,
    )


def _lb_conda_dev_clone(env_name, env_prefix, directory, *, texlive=None):
    subprocess.check_output(
        [
            "lb-conda",
            env_name,
            "conda",
            "create",
            "--clone",
            env_prefix,
            "--prefix",
            directory,
        ],
        universal_newlines=True,
    )
    write_run_script(join(directory, "run"), env_prefix, texlive=texlive)


def write_run_script(fn, env_prefix, *, with_venv=None, texlive=None):
    lb_conda_dev_executable = sys.argv[0]
    if basename(lb_conda_dev_executable) != "lb-conda-dev":
        raise NotImplementedError(sys.argv)

    cmd = ["exec"]
    cmd += [lb_conda_dev_executable]
    if with_venv:
        cmd += ["--with-venv", with_venv]
    if texlive:
        cmd += ["--texlive-version", str(texlive)]
    cmd += ["--execute", env_prefix]
    cmd = " ".join([pipes.quote(s) for s in cmd])
    with open(fn, "wt") as fp:
        fp.write('#!/usr/bin/env bash\n{} "$@"'.format(cmd))
    os.chmod(fn, os.stat(fn).st_mode | stat.S_IEXEC)
