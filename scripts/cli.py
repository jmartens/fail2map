from scripts.types.HostOrIPAddress import HostOrIPAddress
import click
import click_log
import geoip2.database
import glob
import logging
import os
import shutil
import sys
import tempfile
import urllib
if sys.version_info < (3, 0):
    import tarfile

logger = logging.getLogger(__name__)
click_log.basic_config(logger)

supported_dbs = ['city', 'country', 'asn']
HOST_OR_IP = HostOrIPAddress()


@click.group()
@click_log.simple_verbosity_option(logger)
@click.pass_context
def cli(ctx):
    conf = dict()
    conf['db_path'] = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), 'db')
    ctx.obj = conf


def maxmind_geoip2_filename_url(database):
    if database == 'city':
        filename = 'GeoLite2-City'
    elif database == 'country':
        filename = 'GeoLite2-Country'
    elif database == 'asn':
        filename = 'GeoLite2-ASN'

    try:
        base_url = 'http://geolite.maxmind.com/download/geoip/database/%s.tar.gz'
        return '%s.mmdb' % filename, base_url % filename
    except UnboundLocalError:
        pass


@cli.command(name='geoip')
@click_log.simple_verbosity_option(logger)
@click.option('--download', '-d', 'databases',  multiple=True,
              type=click.Choice(supported_dbs),
              is_flag=False,
              expose_value=True,
              is_eager=True)
@click.option('--remove', '-rm', 'databases',  multiple=True,
              type=click.Choice(supported_dbs),
              is_flag=False,
              expose_value=True,
              is_eager=True)
@click.option('--update', '-rm', 'databases',  multiple=True,
              type=click.Choice(supported_dbs),
              is_flag=False,
              expose_value=True,
              is_eager=True)
def geoip(databases):
    for database in databases:
        logger.info('Processing: %s', database)
        filename, url = maxmind_geoip2_filename_url(database)

        urlopener = urllib.URLopener()
        if url:
            logger.info('Downloading: %s', database)
            try:
                temp, headers = urlopener.retrieve(url)
                if temp:
                    logger.info('Extracting: %s', database)
                    target = tempfile.mkdtemp()
                    if sys.version_info >= (3, 0):
                        shutil.unpack_archive(temp, target)
                    else:
                        with tarfile.open(temp, "r:gz") as so:
                            so.extractall(path=target)
                    db = glob.glob(os.path.join(target, '**', filename)).pop()
                    if not os.path.exists('db'):
                        os.makedirs('db')
                    shutil.move(db, os.path.join('db', filename))
            except IOError:
                logger.error('Downloading failed: %s', database)


@cli.command()
@click.pass_context
@click_log.simple_verbosity_option(logger)
@click.argument('host', type=HOST_OR_IP)
@click.option('--database', '-d',  multiple=False,
              type=click.Choice(supported_dbs),
              is_flag=False,
              default='city',
              expose_value=True,
              is_eager=True)
# def lookup(database, ip):
def lookup(ctx, database, host):
    filename, _ = maxmind_geoip2_filename_url(database)
    if filename:
        reader = geoip2.database.Reader(os.path.join(ctx.obj['db_path'], filename))
        result = getattr(reader, database)(host)
        click.echo("(%f, %f)" % (result.location.latitude, result.location.longitude))
