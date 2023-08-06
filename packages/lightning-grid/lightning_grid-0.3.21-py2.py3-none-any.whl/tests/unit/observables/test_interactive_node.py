import click
import pytest
from gql.transport.exceptions import TransportQueryError

import grid.client as grid
import grid.observables.interactive_node as interactive_node_observable
from tests.utilities import (create_test_credentials, monkey_patch_client,
                             monkeypatched)


def mp_execute(*args, **kwargs):
    raise Exception("{'message':'not found'}")


class TestIneteractiveObservable:
    @classmethod
    def setup_class(cls):
        create_test_credentials()

        grid.Grid._init_client = monkey_patch_client
        interactive_node_observable.gql = lambda x: x

        cls.grid = grid.Grid(load_local_credentials=False)
        cls.grid._init_client()

    def test_get(self, capsys):
        interactive_node_observable.env.SHOW_PROCESS_STATUS_DETAILS = False
        interactive_node_observable.env.DEBUG = True
        obsevable = interactive_node_observable.InteractiveNode(
            client=self.grid.client)

        obsevable.get()
        captured = capsys.readouterr()

        expected_columns = ['Project', 'Name', 'Status']
        for column in expected_columns:
            assert column in captured.out

    def tets_get_handles_error(self):
        def mp_transport_error(*args, **kwargs):
            raise TransportQueryError('test')

        with monkeypatched(self.grid.client, 'execute', mp_transport_error):
            obsevable = interactive_node_observable.InteractiveNode(
                client=self.grid.client)
            with pytest.raises(click.ClickException):
                obsevable.get()
