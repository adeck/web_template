#!/usr/bin/env python

import click
import yaml
import sh
from logbook import Logger
from staticjinja import make_site
import markdown

log = Logger('sitebuilder')

@click.group()
def cli():
    log.notice('Loading the filthcannon.')

@cli.command()
def build():
    log.critical('filthbuilding...')
    try: sh.rm('-r', 'build')
    except: pass
    sh.mkdir('build')
    site = make_site(searchpath='src', outpath='build',
                filters={'markdown': markdown.markdown})
    site.render(use_reloader=False)

@cli.command()
def deploy():
    config = get_config()
    log.info('deploying the filth...')
    url = 's3://%s' % config['domain']
    sh.aws('s3', 'rm', url + '/', '--recursive')
    sh.aws('s3', 'sync', 'build/site', url)

def get_config():
    log.info('loading the config file')
    with open('conf.d/main.yml', 'r') as f:
        return yaml.safe_load(f.read())

cli()

