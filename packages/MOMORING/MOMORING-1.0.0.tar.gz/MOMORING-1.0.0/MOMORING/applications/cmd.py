import click
from MOMORING.api.create_project import create_project_dir


@click.group()
def cmd1():
    pass


@cmd1.command()
@click.option('-p', '--project', default=None, help='Project name.')
def init(project):
    create_project_dir(project)


def run():
    cli = click.CommandCollection(sources=[cmd1])
    cli()
