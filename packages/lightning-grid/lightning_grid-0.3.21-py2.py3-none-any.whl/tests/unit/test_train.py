import click
import unittest

from grid.cli.grid_train import (_check_run_name_is_valid,
                                 _check_is_valid_extension,
                                 _check_description_isnt_too_long)


class TrainCallbacksTestCase(unittest.TestCase):
    """Tests callbacks in train."""
    def test_name_callback(self):
        # Run name needs to be alphanumeric
        with self.assertRaises(click.ClickException):
            _check_run_name_is_valid(None, None, '$')

        # Run name can't start or end with a dash
        with self.assertRaises(click.ClickException):
            _check_run_name_is_valid(None, None, '-run')

        with self.assertRaises(click.ClickException):
            _check_run_name_is_valid(None, None, 'run-')

        # Run name can't contain upper case letters
        with self.assertRaises(click.ClickException):
            _check_run_name_is_valid(None, None, 'Run')

        # Run name can't end with exp[0-9]
        with self.assertRaises(click.ClickException):
            _check_run_name_is_valid(None, None, 'run-exp0')

        with self.assertRaises(click.ClickException):
            _check_run_name_is_valid(None, None, 'run-exp100')

        # Besides that, run name should work
        assert _check_run_name_is_valid(None, None, 'run')

    def test_valid_extension_callback(self):
        """
        _check_is_valid_extension() raises exception if file isn't valid extension
        """
        f = 'foo.txt'
        with self.assertRaises(click.BadParameter):
            _check_is_valid_extension(None, None, f)

    def test_check_description_isnt_too_long(self):
        """
        _check_description_isnt_too_long() checks that description isn't
        too long
        """
        d = 'a' * 201
        with self.assertRaises(click.BadParameter):
            _check_description_isnt_too_long(None, None, d)
