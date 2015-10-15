# -*- coding: utf-8 -*-

""" Tests for go_cli.export_contacts. """

from unittest import TestCase
from StringIO import StringIO
import json

from click.testing import CliRunner

import go_cli.export_contacts
from go_cli.main import cli
from go_cli.export_contacts import (
    contact_to_csv_dict, csv_contact_writer, json_contact_writer)
from go_cli.tests.utils import ApiHelper


class TestExportContactsCommand(TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.api_helper = ApiHelper(self)
        self.api_helper.patch_api(go_cli.export_contacts, 'ContactsApiClient')

    def tearDown(self):
        self.api_helper.tearDown()

    def invoke_export_contacts(self, args, account="acc-1", token="tok-1"):
        return self.runner.invoke(cli, [
            '--account', account, 'export-contacts',
            '--token', token,
        ] + args)

    def test_help(self):
        result = self.runner.invoke(cli, ['export-contacts', '--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(
            "Export contacts from the contacts API."
            in result.output)

    def test_export_no_api_details(self):
        result = self.runner.invoke(cli, ['export-contacts'])
        self.assertEqual(result.exit_code, 2)
        self.assertTrue(
            "Please specify both the account key and the contacts API"
            " authentication token. See --help."
            in result.output)

    def test_export_no_output_specified(self):
        result = self.invoke_export_contacts([])
        self.assertEqual(result.exit_code, 2)
        self.assertTrue("Please specify either --csv or --json (but not both)."
                        in result.output)

    def test_export_to_csv(self):
        response = self.api_helper.add_contacts(
            "tok-1",
            contacts=[
                {"msisdn": "1234"},
                {"msisdn": "5678"},
            ])
        with self.runner.isolated_filesystem():
            result = self.invoke_export_contacts(['--csv', 'contacts.csv'])
            self.assertEqual(result.output, "")
            self.api_helper.check_response(response, 'GET')
            with open('contacts.csv') as f:
                self.assertEqual(
                    f.read(),
                    "msisdn\r\n1234\r\n5678\r\n")

    def test_export_to_json(self):
        response = self.api_helper.add_contacts(
            "tok-1",
            contacts=[
                {"msisdn": "1234"},
                {"msisdn": "5678"},
            ])
        with self.runner.isolated_filesystem():
            result = self.invoke_export_contacts(['--json', 'contacts.json'])
            self.assertEqual(result.output, "")
            self.api_helper.check_response(response, 'GET')
            with open('contacts.json') as f:
                self.assertEqual(
                    f.read(),
                    '{"msisdn": "1234"}\n{"msisdn": "5678"}\n')


class TestContactToCsvDict(TestCase):
    def test_unicode_keys(self):
        self.assertEqual(
            contact_to_csv_dict({u"éł": "123"}),
            {u"éł".encode("utf-8"): "123"})

    def test_unicode_value(self):
        self.assertEqual(
            contact_to_csv_dict({"123": u"éł"}),
            {"123": u"éł".encode("utf-8")})

    def test_non_string_values(self):
        self.assertEqual(
            contact_to_csv_dict({"abc": [1, 2, 3]}),
            {"abc": json.dumps([1, 2, 3])})


class TestCsvContactWriter(TestCase):
    def test_new_file(self):
        f = StringIO()
        writer = csv_contact_writer(f)
        writer({"msisdn": "1234"})
        writer({"msisdn": "5678"})
        self.assertEqual(f.getvalue(), "msisdn\r\n1234\r\n5678\r\n")


class TestJsonContactWriter(TestCase):
    def test_new_file(self):
        f = StringIO()
        writer = json_contact_writer(f)
        writer({"msisdn": "1234"})
        writer({"msisdn": "5678"})
        self.assertEqual(
            f.getvalue(), '{"msisdn": "1234"}\n{"msisdn": "5678"}\n')
