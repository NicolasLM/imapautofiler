#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import email.parser
import logging
from email.header import Header
from email.message import Message
import fixtures
import testtools
from email.utils import format_datetime
import datetime


def construct_message(headers):
    msg = Message()
    encoding = 'utf-8'

    for header, value in headers.items():
        msg[header] = Header(value, encoding)

    return msg.as_string()


date = format_datetime(datetime.datetime.now())
past_date = format_datetime(
    datetime.datetime.now() - datetime.timedelta(days=90)
)
MESSAGE = {
    'From': 'Sender Name <sender@example.com>',
    'Content-Type':
        'multipart/alternative; '
        'boundary="Apple-Mail=_F10D7C06-52F7-4F60-BEC9-4D5F29A9BFE1"',
    'Message-Id': '<4FF56508-357B-4E73-82DE-458D3EEB2753@example.com>',
    'Mime-Version': '1.0 (Mac OS X Mail 9.2 \(3112\))',
    'X-Smtp-Server': 'AE35BF63-D70A-4AB0-9FAA-3F18EB9802A9',
    'Subject': 'Re: reply to previous message',
    'Date': '{}'.format(past_date),
    'X-Universally-Unique-Identifier': 'CC844EE1-C406-4ABA-9DA5-685759BBC15A',
    'References': '<33509d2c-e2a7-48c0-8bf3-73b4ba352b2f@example.com>',
    'To': 'recipient1@example.com',
    'CC': 'recipient2@example.com',
    'In-Reply-To': '<33509d2c-e2a7-48c0-8bf3-73b4ba352b2f@example.com>'

}

I18N_MESSAGE = MESSAGE.copy()
I18N_MESSAGE.update({
    'From': 'Иванов Иван <sender@example.com>',
    'To': 'Иванов Иван <recipient3@example.com>',
    'Subject': 'Re: ответ на предыдущее сообщение',
})

RECENT_MESSAGE = MESSAGE.copy()
RECENT_MESSAGE.update({
    'Date': '{}'.format(date),
})


class TestCase(testtools.TestCase):
    _msg = None
    _recent_msg = None
    _i18n_msg = None

    def setUp(self):
        super().setUp()
        # Capture logging
        self.useFixture(fixtures.FakeLogger(level=logging.DEBUG))
        # Capturing printing
        stdout = self.useFixture(fixtures.StringStream('stdout')).stream
        self.useFixture(fixtures.MonkeyPatch('sys.stdout', stdout))

    @property
    def msg(self):
        if self._msg is None:
            self._msg = email.parser.Parser().parsestr(
                construct_message(MESSAGE)
            )
        return self._msg

    @property
    def i18n_msg(self):
        if self._i18n_msg is None:
            self._i18n_msg = email.parser.Parser().parsestr(
                construct_message(I18N_MESSAGE)
            )
        return self._i18n_msg

    @property
    def recent_msg(self):
        if self._recent_msg is None:
            self._recent_msg = email.parser.Parser().parsestr(
                construct_message(RECENT_MESSAGE)
            )
        return self._recent_msg


def pytest_generate_tests(metafunc):
    # from https://docs.pytest.org/en/latest/example/parametrize.html#a-quick-port-of-testscenarios  # noqa
    idlist = []
    argvalues = []
    for scenario in metafunc.cls.scenarios:
        idlist.append(scenario[0])
        items = scenario[1].items()
        argnames = [x[0] for x in items]
        argvalues.append(([x[1] for x in items]))
    metafunc.parametrize(argnames, argvalues, ids=idlist, scope="class")
