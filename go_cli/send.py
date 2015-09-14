""" Send messages via an HTTP API (nostream) conversation. """

import csv
import json

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
    if not any((csv, json)):
        click.echo("Please specify either --csv or --json.")
        ctx.abort()
    http_api = HttpApiSender(ctx.obj.account_key, conversation, token)
    if csv:
        for msg in messages_from_csv(csv):
            http_api.send_text(**msg)
    if json:
        for msg in messages_from_json(json):
            http_api.send_text(**msg)


def messages_from_csv(csv_file):
    reader = csv.DictReader(csv_file)
    for data in reader:
        yield {
            "to_addr": data["to_addr"],
            "content": data["content"],
            "session_event": data.get("session_event")
        }


def messages_from_json(json_file):
    for line in json_file:
        data = json.loads(line.rstrip("\n"))
        yield {
            "to_addr": data["to_addr"],
            "content": data["content"],
            "session_event": data.get("session_event")
        }
