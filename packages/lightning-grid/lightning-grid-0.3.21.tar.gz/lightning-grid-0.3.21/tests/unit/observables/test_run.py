import click
import pytest
import tests.resolvers as resolvers
from datetime import datetime
from gql.transport.exceptions import TransportQueryError

import grid.client as grid
import grid.observables.run as run_observable
from tests.utilities import (create_test_credentials, monkey_patch_client,
                             monkeypatched)


def mp_execute(*args, **kwargs):
    raise Exception("{'message':'not found'}")


class TestRunObservable:
    @classmethod
    def setup_class(cls):
        create_test_credentials()

        grid.Grid._init_client = monkey_patch_client
        run_observable.gql = lambda x: x

        cls.grid = grid.Grid(load_local_credentials=False)
        cls.grid._init_client()

    def test_get(self):
        run_observable.env.DEBUG = True
        obsevable = run_observable.Run(client=self.grid.client)
        result = obsevable.get()
        assert len(result) > 0

    def test_get_handles_transport_error(self):
        def mp_execute_transport(*args, **kwargs):
            raise TransportQueryError('test')

        with monkeypatched(self.grid.client, 'execute', mp_execute_transport):
            obsevable = run_observable.Run(client=self.grid.client)
            with pytest.raises(click.ClickException):
                obsevable.get()

    def test_get_with_id(self, capsys):
        run_observable.env.DEBUG = True
        obsevable = run_observable.Run(client=self.grid.client,
                                       identifier='test-run')
        result = obsevable.get()
        assert len(result) > 0

        # captured = capsys.readouterr()
        # assert 'nExperiments' in captured.out

    def test_get_history(self, capsys):
        run_observable.env.DEBUG = True
        obsevable = run_observable.Run(client=self.grid.client,
                                       identifier='test-run')
        result = obsevable.get_history()

        assert len(result) > 0
        assert 'createdAt' in result['getRuns'][0]

        captured = capsys.readouterr()
        assert 'Created At' in captured.out

    def test_get_shows_empty_table(self, capsys):
        def mp_get_runs(*args, **kwargs):
            return [{
                'name': 'test-run-0',
                'createdAt': resolvers.now,
                'experiments': [{
                    'experimentId': 'test-run-exp0'
                }],
                'nExperiments': 2,
                'nFailed': 2,
                'nCancelled': 0,
                'nRunning': 0,
                'nCompleted': 0,
                'nQueued': 0,
                'projectId': 'test/project',
                'resourceUrls': {
                    'tensorbaord': 'http://localhost/'
                }
            }]

        with monkeypatched(resolvers, 'get_runs', mp_get_runs):
            obsevable = run_observable.Run(client=self.grid.client)
            obsevable.get()
            captured = capsys.readouterr()
            assert 'Run' in captured.out

    def test_get_shows_empty_history_table(self, capsys):
        def mp_get_runs(*args, **kwargs):
            return []

        with monkeypatched(resolvers, 'get_runs', mp_get_runs):
            obsevable = run_observable.Run(client=self.grid.client)
            obsevable.get_history()
            captured = capsys.readouterr()
            assert 'No History' in captured.out
