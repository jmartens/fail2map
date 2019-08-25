from click.testing import CliRunner
from scripts.cli import cli
import socket
import pytest

HOSTNAME = 'www.snetram.nl'


@pytest.fixture(scope='function')
def runner(request):
    return CliRunner()


def test_lookup_hostname(runner):
    result = runner.invoke(cli, ['lookup', HOSTNAME])
    assert result.exit_code == 0
    assert '(50.849000, 5.659000)' in result.output


def test_lookup_ip(runner):
    result = runner.invoke(cli, ['lookup', socket.gethostbyname(HOSTNAME)])
    assert result.exit_code == 0
    assert '(50.849000, 5.659000)' in result.output
