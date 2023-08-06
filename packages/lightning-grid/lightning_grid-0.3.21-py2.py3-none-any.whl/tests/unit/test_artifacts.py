import click
import unittest

from grid.cli.grid_artifacts import _check_is_experiment


class ArtifactCallbacksTestCase(unittest.TestCase):
    """Tests callbacks in grid artifacts."""
    def test_callbacks(self):
        # Test that incorrect experiment names fail.
        value_a = ['foo-bar']
        value_b = ['foo-bar', 'foo-bar-exp0']
        with self.assertRaises(click.BadArgumentUsage):
            _check_is_experiment(None, None, value_a)
            _check_is_experiment(None, None, value_b)

        # Test that correct experiment names work.
        value_c = ['foo-bar-exp1', 'foo-bar-exp0']
        _check_is_experiment(None, None, value_c)
