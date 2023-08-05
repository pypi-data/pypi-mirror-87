import os

from functools import wraps
from pathlib import Path

import click
import click_spinner

from click.exceptions import MissingParameter

from .bigquery import BigQueryClient
from .export import export_to_mbtiles, export_to_files
from .http_server import start_http_server
from .mbtiles import MBTilesClient
from .settings import AUTHORS, HELP_CONTEXT_SETTINGS, NAME, VERSION, TILESET_LAST_VERSION, VIEWER_PORT


def main():
    cli(obj={})


def catch_exceptions(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)

        except Exception as e:
            if isinstance(e, (click.ClickException, click.Abort, click.exceptions.Exit)):
                raise e

            else:
                info_message = ('The next {error} has ocurred:\n\n\n{exception}\n\n\nIf it persists, contact us at '
                                '{authors}.').format(
                    error=click.style('error', bold=True), exception=e, authors=click.style(AUTHORS, bold=True)
                )
                click.echo(info_message)
                raise click.exceptions.Exit(1)

    return wrapper


@click.group(context_settings=HELP_CONTEXT_SETTINGS)
@click.option('-p', '--project', help="Google Cloud's project ID, not needed for service account credentials JSON "
              'file. By default it will use the default project set on gcloud.')
@click.option('-c', '--credentials', help="Path to a Google Cloud's service account or authorized user JSON file. "
              'By default it will use the default credentials on gcloud.')
@click.version_option(VERSION, prog_name=NAME, message='%(prog)s v%(version)s')
@click.pass_context
def cli(ctx, project, credentials):
    """
    Python script for management of CARTO tilesets in BigQuery.

    To get help for each command run: carto-bq-tiler COMMAND --help
    """
    # The substring 'carto-bq-tiler' in the multiline string above should be dynamically added :(

    bq_client = BigQueryClient(project, credentials)
    ctx.obj['bq_client'] = bq_client


@cli.command(context_settings=HELP_CONTEXT_SETTINGS)
@click.argument('mbtiles_file_path', required=True, type=click.Path(exists=True))
@click.argument('name', required=True)
@click.pass_context
@catch_exceptions
def load(ctx, mbtiles_file_path, name):
    """
    Create a new tileset from an MBtile file.
    """

    bq_client = ctx.obj['bq_client']

    with click_spinner.spinner():
        tileset_name = bq_client.get_tileset_name(name)
        mb_client = MBTilesClient(mbtiles_file_path)

    info_message = 'Uploading {file_name} to the {project} project.'.format(
        file_name=click.style(mb_client.file_name, bold=True), project=click.style(bq_client.project, bold=True)
    )
    click.echo(info_message)

    with click_spinner.spinner():
        try:
            mb_client.parse_and_clean_metadata()
            metadata = mb_client.get_metadata()
            csv_file_path = mb_client.tileset_to_csv()
            mb_client.close()

            bq_client.upload_tileset_from_csv(csv_file_path, tileset_name, metadata.get('carto_partition'))
            bq_client.upload_tileset_metadata_and_label(tileset_name, metadata)

        except Exception as e:
            if tileset_name:
                bq_client.drop_tilesets([tileset_name])

            raise e

    info_message = 'Tileset uploaded as {tileset}.'.format(tileset=click.style(tileset_name, bold=True))
    click.echo(info_message)


@cli.command('export-mbtiles', context_settings=HELP_CONTEXT_SETTINGS)
@click.argument('tileset', required=True)
@click.option('-f', '--file', help='MBTiles output file.')
@click.pass_context
@catch_exceptions
def export_mbtiles(ctx, tileset, file):
    """
    Export a tileset to a local MBTiles file.
    Only works for last tilesets valid version.
    """

    bq_client = ctx.obj['bq_client']
    bq_client.validate_tileset_name(tileset)
    file = file or '{tileset}.mbtiles'.format(tileset=tileset)

    if not bq_client.exists_tileset(tileset):
        info_message = "{tileset} tileset doesn't exsit in the {project} project or its version it isn't {version}."
        info_message = info_message.format(tileset=click.style(tileset, bold=True),
                                           project=click.style(bq_client.project, bold=True),
                                           version=TILESET_LAST_VERSION)
        click.echo(info_message)
        return

    if os.path.exists(file):
        info_message = '{file} file already exists, delete it or use a different one.'.format(
            file=click.style(file, bold=True)
        )
        click.echo(info_message)
        return

    with click_spinner.spinner():
        export_to_mbtiles(bq_client, tileset, file)

    info_message = 'Tileset {tileset} exported to {file}.'.format(tileset=click.style(tileset, bold=True),
                                                                  file=click.style(file, bold=True))
    click.echo(info_message)


@cli.command('export-tiles', context_settings=HELP_CONTEXT_SETTINGS)
@click.argument('tileset', required=True)
@click.option('-d', '--directory', help='Viewer output directory.')
@click.pass_context
@catch_exceptions
def export_tiles(ctx, tileset, directory):
    """
    Export a tileset to separated tile files.
    Only works for last tilesets valid version.
    """

    bq_client = ctx.obj['bq_client']
    bq_client.validate_tileset_name(tileset)
    directory = directory or tileset

    if not bq_client.exists_tileset(tileset):
        info_message = "{tileset} tileset doesn't exsit in the {project} project or its version it isn't {version}."
        info_message = info_message.format(tileset=click.style(tileset, bold=True),
                                           project=click.style(bq_client.project, bold=True),
                                           version=TILESET_LAST_VERSION)
        click.echo(info_message)
        return

    if os.path.exists(directory):
        info_message = '{directory} directory already exists, delete it or use a different one.'.format(
            directory=click.style(directory, bold=True)
        )
        click.echo(info_message)
        return

    with click_spinner.spinner():
        export_to_files(bq_client, tileset, directory)

    info_message = 'Tileset {tileset} exported to {directory}.'.format(tileset=click.style(tileset, bold=True),
                                                                       directory=click.style(directory, bold=True))
    click.echo(info_message)


@cli.command('view-local', context_settings=HELP_CONTEXT_SETTINGS)
@click.argument('tileset_directory', required=True)
@click.option('--port', default=VIEWER_PORT, show_default=True, help='Server port.')
@click.pass_context
@catch_exceptions
def view_local(ctx, tileset_directory, port):
    """
    Opens a simple web server to preview a tileset exported locally with the "export-as-local-tiles" command.
    """

    tileset = str(Path(tileset_directory).name)

    if not os.path.isdir(tileset_directory):
        command = '{name} export-tiles {tileset}'.format(name=NAME, tileset=tileset)
        info_message = 'The {tileset} tileset can not be found, run "{command}" for downloading it.'.format(
            tileset=click.style(tileset, bold=True), command=click.style(command, bold=True)
        )
        click.echo(info_message)
        return

    url = 'http://localhost:{port}/'.format(port=port)
    info_message = (
        'Serving local {tileset} tileset at {url}, use {control_c} for stopping the server.'
    ).format(tileset=click.style(tileset, bold=True), url=click.style(url, bold=True),
             control_c=click.style('control+c', bold=True))
    click.echo(info_message)

    index_configuration = {
        'directory_name': tileset_directory
    }
    start_http_server(index_configuration, port)


@cli.command(context_settings=HELP_CONTEXT_SETTINGS)
@click.argument('tileset', required=False)
@click.option('-e', '--empty', default=False, show_default=True, is_flag=True, help='With no tileset set.')
@click.option('-c', '--compare', default=False, show_default=True, is_flag=True, help='Add a second map for comparing.')
@click.option('--port', default=VIEWER_PORT, show_default=True, help='Server port.')
@click.pass_context
@catch_exceptions
def view(ctx, tileset, empty, compare, port):
    """
    Opens a simple web server to preview a tileset stored in BigQuery.
    Only works for last tilesets valid version.
    """

    bq_client = ctx.obj['bq_client']

    if empty:
        index_configuration = {
            'project': bq_client.project,
            'dataset': '',
            'table': '',
            'token': bq_client.token
        }

    else:
        if not tileset:
            raise MissingParameter(param_type="argument 'TILESET' if '--empty' is not set")

        if not bq_client.exists_tileset(tileset):
            info_message = "{tileset} tileset doesn't exsit in the {project} project or its version it isn't {version}."
            info_message = info_message.format(tileset=click.style(tileset, bold=True),
                                               project=click.style(bq_client.project, bold=True),
                                               version=TILESET_LAST_VERSION)
            click.echo(info_message)
            return

        url = 'http://localhost:{port}/'.format(port=port)
        info_message = (
            'Serving {tileset} tileset at {url}, use {control_c} for stopping the server.'
        ).format(tileset=click.style(tileset, bold=True), url=click.style(url, bold=True),
                 control_c=click.style('control+c', bold=True))
        click.echo(info_message)

        dataset, table = tileset.split('.')
        index_configuration = {
            'project': bq_client.project,
            'dataset': dataset,
            'table': table,
            'token': bq_client.token
        }

    start_http_server(index_configuration, port, compare)


@cli.command(context_settings=HELP_CONTEXT_SETTINGS)
@click.pass_context
@catch_exceptions
def list(ctx):
    """
    List all CARTO tilesets already created on the project.
    """

    bq_client = ctx.obj['bq_client']
    with click_spinner.spinner():
        tilesets = bq_client.list_tilesets(tileset_last_version=False)

    if not tilesets:
        click.echo("You don't have any CARTO tilesets.")
        return

    tileset_table = [[click.style('Tileset name', bold=True), click.style('Created at', bold=True),
                      click.style('Tileset version', bold=True)]]
    for tileset in tilesets:
        tileset_table.append([tileset['tileset_name'], tileset['created_at'], tileset['version']])

    column_0_width = max([len(tileset[0]) for tileset in tileset_table]) + 1
    column_1_width = max([len(tileset[1]) for tileset in tileset_table]) + 1

    for tileset in tileset_table:
        info_message = '{tileset} {datetime} {version}'.format(
            tileset=tileset[0].ljust(column_0_width), datetime=tileset[1].ljust(column_1_width), version=tileset[2])
        click.echo(info_message)


@cli.command(context_settings=HELP_CONTEXT_SETTINGS)
@click.argument('names', nargs=-1, required=True)
@click.pass_context
@catch_exceptions
def remove(ctx, names):
    """
    Remove CARTO tilesets.
    NAMES can be one or more tileset names separated by spaces.
    """

    bq_client = ctx.obj['bq_client']
    [bq_client.validate_tileset_name(name) for name in names]

    with click_spinner.spinner():
        actual_tilesets, not_tilesets = bq_client.exist_tilesets(names, tileset_last_version=False)

    if not_tilesets:
        info_message = "The tileset/s {not_tilesets} do/es/n't exist in the {project} project.".format(
            not_tilesets=click.style(', '.join(not_tilesets), bold=True), project=bq_client.project
        )
        click.echo(info_message)

    if not actual_tilesets:
        return

    while True:
        info_message = 'Remove {actual_tilesets} tileset/s? [y/n] '.format(
            actual_tilesets=click.style(', '.join(actual_tilesets), bold=True)
        )
        click.echo(info_message, nl=False)
        response = click.getchar()
        click.echo()

        if response == 'y':
            with click_spinner.spinner():
                bq_client.drop_tilesets(actual_tilesets)
            info_message = 'Tileset/s {actual_tilesets} removed.'.format(
                actual_tilesets=click.style(','.join(actual_tilesets), bold=True)
            )
            click.echo(info_message)
            break

        elif response == 'n':
            click.echo('Aborted removing.')
            break

        else:
            click.echo('Invalid input {response}.'.format(response=click.style(response, bold=True)))


@cli.command(context_settings=HELP_CONTEXT_SETTINGS)
@click.pass_context
@catch_exceptions
def info(ctx):
    """
    Get the current Google Cloud project, a valid token and last tilesets valid version.
    """

    bq_client = ctx.obj['bq_client']
    with click_spinner.spinner():
        bq_client.populate_credentials()

    click.echo('Current project: {project}'.format(project=click.style(bq_client.project, bold=True)))
    click.echo('Valid token: {token}'.format(token=click.style(bq_client.token, bold=True)))
    click.echo('Last tilesets valid version: {version}'.format(version=click.style(
        str(TILESET_LAST_VERSION), bold=True
    )))


if __name__ == '__main__':
    main()
