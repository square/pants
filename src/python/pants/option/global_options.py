# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)


def register_global_options(register):
  register('-t', '--timeout', type=int, metavar='<seconds>',
           help='Number of seconds to wait for http connections.')
  register('-x', '--time', action='store_true',
           help='Times tasks and goals and outputs a report.')
  register('-e', '--explain', action='store_true',
           help='Explain the execution of goals.')

  # TODO: After moving to the new options system these abstraction leaks can go away.
  register('-k', '--kill-nailguns', action='store_true',
           help='Kill nailguns before exiting')
  register('--ng-daemons', action='store_true', default=True,
           help='Use nailgun daemons to execute java tasks.')

  register('-d', '--logdir', metavar='<dir>',
           help='Write logs to files under this directory.')
  register('-l', '--level', choices=['debug', 'info', 'warn'], default='info',
           help='Set the logging level.')
  register('-q', '--quiet', action='store_true',
           help='Squelches all console output apart from errors.')
  register('-i', '--interpreter', default=[], action='append', metavar='<requirement>',
           help="Constrain what Python interpreters to use.  Uses Requirement format from "
                "pkg_resources, e.g. 'CPython>=2.6,<3' or 'PyPy'. By default, no constraints "
                "are used.  Multiple constraints may be added.  They will be ORed together.")
  register('--no-colors', action='store_true', help='Do not colorize log messages.')
  register('--no-lock', action='store_true',
           help="Don't attempt to grab the global lock. This lock prevents two concurrent pants "
                "instances from stomping on each others data, so only use this if you know what "
                "you're doing.")
  register('--spec-excludes', action='append', default=[register.bootstrap.pants_workdir],
           help='Exclude these target specs when computing the command-line target specs.')
  register('--read-from-artifact-cache', action='store_true', default=True,
           help='Read build artifacts from cache, if available.')
  register('--exclude-target-regexp', action='append', default=[], metavar='<regexp>',
           help='Regex pattern to exclude from the target list (useful in conjunction with ::). '
                'Multiple patterns may be specified by setting this flag multiple times.')
  register('--write-to-artifact-cache', action='store_true', default=True,
           help='Write build artifacts to cache, if possible.')
  register('--overwrite-cache-artifacts', action='store_true',
           help='If writing to build artifacts to cache, overwrite (instead of skip) existing.')
  register('--print-exception-stacktrace', action='store_true',
           help='Print to console the full exception stack trace if encountered.')
  register('--fail-fast', action='store_true',
           help="When parsing specs, will stop on the first erronous BUILD file encountered. "
                "Otherwise, will parse all builds in a spec and then throw an Exception.")
  # This is only registered here so Pants doesn't complain when a user specifies it.
  # It is actually read in rcfile.py directly from the args.
  register('--pantsrc', action='store_true', default=True,
           help="Specifies if pantsrc files should be read or not.")
