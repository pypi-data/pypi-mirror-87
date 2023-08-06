# Ansible roles management

The goal of this tool is to manage installation and upgrade of Ansible
roles using git tags and branches.

This tool uses the `requirements.yml` configuration file used by Ansible
Galaxy. The syntax is unchanged and the ansible-galaxy tool can be used
by people not involved in playbooks development.

This tool assumes a **role version** follows [semantic versioning](http://semver.org/spec/v2.0.0.html)
and is labelled with a git tag of the form _vX.Y_ or _vX.Y.Z_ (examples: v1.0 or v2.3.1). In fact the _v_ is optional but recommended for clarity.

Roles managed manually, bare, or in a bad shape are ignored (with proper
warning).

## Installation

You can install it using PyPI:

    pip install ansible-roles-ctl

Or you can run it in-place since it has very few dependencies (you only
need the ansible-roles-ctl script, version.py is only used in the build
process).

You need the following dependencies:
* Ansible (probably starting from 2.7)
* [GitPython](https://gitpython.readthedocs.io/) (package 'python3-git' on Debian systems, or using pip)

## Usage

Syntax is as follow:

    ansible-roles-ctl [global options] [subcommand] [subcommand options]

You can use -h/--help option to list all available options at command
and subcommand level, as well as all available subcommands.

Follows documentation about the various subcommands.

### Status

    ansible-roles-ctl status

This subcommand display a status report about all required roles.

You can limit output to a selection of roles:

    ansible-roles-ctl status mailman3 httpd

The -c/--changelog option displays changelog entries if available.

### Install

    ansible-roles-ctl install

This subcommand install all roles listed in the requirements.

You can limit this action to a selection of roles:

    ansible-roles-ctl install bind9 postfix

### Update

    ansible-roles-ctl update

This subcommand update all roles listed in the requirements to the
latest version.

You can limit this action to a selection of roles:

    ansible-roles-ctl update bind9 postfix

It is possible to update roles to a particular version and update the
requirements (downgrade is possible):

    ansible-roles-ctl update bind9=1.1

The -r/--req-update option regenerates the requirements file according
to the requested updates. You need to check the result before
commiting; in particular, invalid roles cannot be loaded properly and
would thus be skipped (we hope this limitation to be lifted in a future
version).

