""" Command line interface to Vumi Go HTTP APIs. """

import click


@click.group()
@click.version_option()
@click.option('--account', '-a', help='Vumi Go account key')
def cli(account):
    pass


@cli.command('send')
@click.option('--conversation', '-c', help='HTTP API conversation key')
@click.option('--token', '-t', help='HTTP API conversation token')
def source_archive_dot_org(conversation, token):
    """ Send messages via an HTTP API (nostream) conversation.
    """
    pass


if __name__ == "__main__":
    cli()
