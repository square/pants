# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from textwrap import dedent
import unittest2 as unittest

from pants.base.config import Config
from pants.option.bootstrap_options import get_bootstrap_option_values, create_bootstrapped_options
from pants.util.contextutil import temporary_file
from pants_test.option.fake_config import FakeConfig


class BootstrapOptionsTest(unittest.TestCase):
  def tearDown(self):
    Config.reset_default_bootstrap_option_values()

  def _do_test(self, expected_vals, config, env, args):
    expected_vals_dict = {
      'pants_workdir': expected_vals[0],
      'pants_supportdir': expected_vals[1],
      'pants_distdir': expected_vals[2]
    }

    config_obj = FakeConfig({ 'DEFAULT': config }) if config else None
    vals = get_bootstrap_option_values(env, config_obj, args, buildroot='/buildroot')

    vals_dict = {k: getattr(vals, k) for k in expected_vals_dict }
    self.assertEquals(expected_vals_dict, vals_dict)

  def test_bootstrap_option_values(self):
    # Check all defaults.
    self._do_test(['/buildroot/.pants.d', '/buildroot/build-support', '/buildroot/dist'],
                  config=None, env={}, args=[])

    # Check getting values from config, env and args.
    self._do_test(['/from_config/.pants.d', '/buildroot/build-support', '/buildroot/dist'],
                  config={'pants_workdir': '/from_config/.pants.d'}, env={}, args=[])
    self._do_test(['/buildroot/.pants.d', '/from_env/build-support', '/buildroot/dist'],
                  config=None,
                  env={'PANTS_DEFAULT_PANTS_SUPPORTDIR': '/from_env/build-support'}, args=[])
    self._do_test(['/buildroot/.pants.d', '/buildroot/build-support', '/from_args/dist'],
                  config={}, env={}, args=['--pants-distdir=/from_args/dist'])

    # Check that args > env > config.
    self._do_test(['/from_config/.pants.d', '/from_env/build-support', '/from_args/dist'],
                  config={
                    'pants_workdir': '/from_config/.pants.d',
                    'pants_supportdir': '/from_config/build-support',
                    'pants_distdir': '/from_config/dist'
                  },
                  env={
                    'PANTS_DEFAULT_PANTS_SUPPORTDIR': '/from_env/build-support',
                    'PANTS_DEFAULT_PANTS_DISTDIR': '/from_env/dist'
                  },
                  args=['--pants-distdir=/from_args/dist'])

    # Check that unrelated args and config don't confuse us.
    self._do_test(['/from_config/.pants.d', '/from_env/build-support', '/from_args/dist'],
                  config={
                    'pants_workdir': '/from_config/.pants.d',
                    'pants_supportdir': '/from_config/build-support',
                    'pants_distdir': '/from_config/dist',
                    'unrelated': 'foo'
                  },
                  env={
                    'PANTS_DEFAULT_PANTS_SUPPORTDIR': '/from_env/build-support',
                    'PANTS_DEFAULT_PANTS_DISTDIR': '/from_env/dist'
                  },
                  args=['--pants-distdir=/from_args/dist', '--foo=bar', '--baz'])

  def test_create_bootstrapped_options(self):
    # Check that we can set a bootstrap option from a cmd-line flag and have that interpolate
    # correctly into regular config.
    with temporary_file() as fp:
      fp.write(dedent("""
      [foo]
      bar: %(pants_workdir)s/baz

      [fruit]
      apple: %(pants_supportdir)s/banana
      """))
      fp.close()
      opts = create_bootstrapped_options(known_scopes=['', 'foo', 'fruit'],
                                         env={
                                           'PANTS_DEFAULT_PANTS_SUPPORTDIR': '/pear'
                                         },
                                         configpath=fp.name,
                                         args=['--pants-workdir=/qux'])
      opts.register('foo', '--bar')
      opts.register('fruit', '--apple')
    self.assertEquals('/qux/baz', opts.for_scope('foo').bar)
    self.assertEquals('/pear/banana', opts.for_scope('fruit').apple)
