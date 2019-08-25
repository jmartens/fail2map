from click.testing import CliRunner
from scripts.cli import cli
import os
import pytest

HOSTNAME = 'www.snetram.nl'


@pytest.fixture(scope='function')
def runner():
    return CliRunner()


def test_geoip2_download_city_db(runner):
    for flag in ['-d', '--download']:
        with runner.isolated_filesystem():
            result = runner.invoke(cli, ['geoip', flag, 'city'])
            assert result.exit_code == 0
            assert os.path.exists(os.path.join('db', 'GeoLite2-City.mmdb')) is True


def test_geoip2_download_country(runner):
    for flag in ['-d', '--download']:
        with runner.isolated_filesystem():
            result = runner.invoke(cli, ['geoip', flag, 'country'])
            assert result.exit_code == 0
            assert os.path.exists(os.path.join(os.getcwd(), 'db', 'GeoLite2-Country.mmdb')) is True


def test_geoip2_download_asn_db(runner):
    for flag in ['-d', '--download']:
        with runner.isolated_filesystem():
            result = runner.invoke(cli, ['geoip', flag, 'asn'])
            assert result.exit_code == 0
            assert os.path.exists(os.path.join('db', 'GeoLite2-ASN.mmdb')) is True
