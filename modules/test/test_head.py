"""
test_head.py - tests for the HTTP metadata utilities module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import re
import unittest
from mock import MagicMock, Mock
from modules.head import head, snarfuri

class TestHead(unittest.TestCase):
    def setUp(self):
        self.phenny = MagicMock()

    def test_head(self):
        input = Mock(group=lambda x: 'http://vtluug.org')
        head(self.phenny, input)

        out = self.phenny.reply.call_args[0][0]
        m = re.match('^200, text/html, utf-8, \d{4}\-\d{2}\-\d{2} '\
                '\d{2}:\d{2}:\d{2} UTC, [0-9\.]+ s$', out, flags=re.UNICODE)
        self.assertTrue(m)

    def test_head_404(self):
        input = Mock(group=lambda x: 'http://vtluug.org/trigger_404')
        head(self.phenny, input)

        out = self.phenny.say.call_args[0][0]
        self.assertEqual(out, '404')

    def test_header(self):
        input = Mock(group=lambda x: 'http://vtluug.org Server')
        head(self.phenny, input)

        self.phenny.say.assert_called_once_with("Server: nginx")

    def test_header_bad(self):
        input = Mock(group=lambda x: 'http://vtluug.org truncatedcone')
        head(self.phenny, input)

        self.phenny.say.assert_called_once_with("There was no truncatedcone "\
                "header in the response.")

    def test_snarfuri(self):
        self.phenny.config.prefix = '.'
        self.phenny.config.linx_api_key = ""
        input = Mock(group=lambda x=0: 'http://google.com',
                sender='#phenny')
        snarfuri(self.phenny, input)

        self.phenny.msg.assert_called_once_with('#phenny', "[ Google ]")

    def test_snarfuri_405(self):
        self.phenny.config.prefix = '.'
        self.phenny.config.linx_api_key = ""
        input = Mock(group=lambda x=0: 'http://ozuma.sakura.ne.jp/httpstatus/405',
                sender='#phenny')
        snarfuri(self.phenny, input)

        self.assertEqual(self.phenny.msg.called, False)
