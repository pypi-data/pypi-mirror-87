import json
import os

import click
import yaml

from . import from_collection
from .mock import Mock
from .parser import CollectionParser
from .spec import Spec
from .test_regex import place_holder_check_replace

@click.group(help="Convert or mock your postman collection to openapi schema")
@click.pass_context
def cli(ctx):
    pass


@cli.command()
@click.option("--format", '-f', default='yaml', help="Format to output. One of json or yaml. Defaults to yaml")
@click.option("--ignore", '-i', help="Ignore file in yaml or json")
@click.option("--placeholder", "-p", help ="Provide list for placeholder", default=None)
@click.argument('POSTMANFILE', required=True)
@click.argument('OUTFILE', required=True)
def convert(format, ignore, placeholder, postmanfile, outfile):
    collection_file = os.path.join(postmanfile)
    try:
        ignore_file = os.path.join(ignore)
    except TypeError:
        ignore_file = None
    if placeholder:
        placeholder=json.loads(placeholder)
    
    collection = CollectionParser(place_holder_check_replace(from_collection(collection_file), placeholder))

    spec = Spec(collection)
    converted, server = spec.convert(ignorespec=ignore_file, yaml=(format == 'yaml'))
    converted = yaml.load(converted)
    converted.update(server)
    if outfile:
        with open(outfile, 'w') as f:
            yaml.dump(converted, f, default_flow_style=False)
            # f.write(converted)

    click.echo(click.style('Schema converted successfully!', fg='green'))
    return json.dumps(converted) if format == 'json' else converted


@cli.command()
@click.option("--host", '-h', default='127.0.0.1', help="Host Default: 127.0.0.1")
@click.option("--port", '-p', default=8080, help="Port Default: 8080")
@click.option("--debug", '-D', default=False, help="Debug", is_flag=True)
@click.argument('SPECFILE', required=True)
def mock(host, port, debug, specfile):
    mock = Mock(specfile, spec_dir=os.path.abspath('.'))
    mock.start(port=port, host=host, debug=debug)


if __name__ == '__main__':
    cli()
