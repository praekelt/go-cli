""" Send messages via an HTTP API (nostream) conversation. """

import click

from go_http.send import HttpApiSender


@click.option(
    '--conversation', '-c',
    help='HTTP API conversation key')
@click.option(
    '--token', '-t',
    help='HTTP API conversation token')
@click.option(
    '--csv', type=click.File('rb'),
    help=('CSV file with columns to_addr, content and, optionally,'
          'session_event.'))
@click.option(
    '--json', type=click.File('rb'),
    help=('JSON objects, one per line with fields to_addr, content and,'
          ' optionally, session_event'))
@click.pass_context
def send(ctx, conversation, token, csv, json):
    """ Send messages via an HTTP API (nostream) conversation.
    """
    http_api = HttpApiSender(ctx.obj.account_key, conversation, token)
    messages = []  # TODO: parse csv or json
    for msg in messages:
        http_api.send_text(**msg)
