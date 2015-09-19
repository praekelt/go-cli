""" Tests for go_cli.send. """

from unittest import TestCase
from StringIO import StringIO
import json
import types

from click.testing import CliRunner

from go_cli.main import cli
from go_cli.send import messages_from_csv, messages_from_json


class TestSendCommand(TestCase):
    def test_send_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['send', '--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(
            "Send messages via an HTTP API (nostream) conversation."
            in result.output)


class TestMessagesFromCsv(TestCase):
    def test_with_session_event(self):
        csv_file = StringIO("\n".join([
            "to_addr,content,session_event",
            "+1234,hello world,resume"
        ]))
        msgs = messages_from_csv(csv_file)
        self.assertTrue(isinstance(msgs, types.GeneratorType))
        self.assertEqual(list(msgs), [{
            'to_addr': '+1234', 'content': 'hello world',
            'session_event': 'resume',
        }])

    def test_without_session_event(self):
        csv_file = StringIO("\n".join([
            "to_addr,content",
            "+1234,hello world"
        ]))
        msgs = messages_from_csv(csv_file)
        self.assertTrue(isinstance(msgs, types.GeneratorType))
        self.assertEqual(list(msgs), [{
            'to_addr': '+1234', 'content': 'hello world',
            'session_event': None,
        }])


class TestMessagesFromJson(TestCase):
    def test_with_session_event(self):
        rows = [
            {"to_addr": "+1234", "content": "hello", "session_event": "new"},
            {"to_addr": "+1235", "content": "bye", "session_event": "close"},
        ]
        json_file = StringIO("\n".join(json.dumps(r) for r in rows))
        msgs = messages_from_json(json_file)
        self.assertTrue(isinstance(msgs, types.GeneratorType))
        self.assertEqual(list(msgs), rows)

    def test_without_session_event(self):
        rows = [
            {"to_addr": "+1234", "content": "hello"},
            {"to_addr": "+1235", "content": "bye"},
        ]
        json_file = StringIO("\n".join(json.dumps(r) for r in rows))
        msgs = messages_from_json(json_file)
        self.assertTrue(isinstance(msgs, types.GeneratorType))
        self.assertEqual(list(msgs), [
            dict(session_event=None, **r) for r in rows
        ])
