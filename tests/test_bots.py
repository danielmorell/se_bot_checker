from unittest import TestCase
from se_bot_checker.bots import GoogleBot


class TestGoogleBot(TestCase):
    def setUp(self):
        self.googlebot = GoogleBot()
        self.googlebot('66.249.66.1', 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)')
        self.host = self.googlebot.reverse_dns()

    def test_run(self):
        self.assertTupleEqual(self.googlebot.run(), (True, 'googlebot'))

    def test_valid_user_agent(self):
        self.assertTrue(self.googlebot.valid_user_agent())

    def test_valid_domain(self):
        self.assertTrue(self.googlebot.valid_domain(self.host))

    def test_valid_ip(self):
        self.assertTrue(self.googlebot.valid_ip())

    def test_reverse_dns(self):
        self.assertTrue(self.host.endswith('.googlebot.com') or self.host.endswith('.google.com'))

    def test_forward_dns(self):
        self.assertTrue(self.googlebot.forward_dns(self.host))

    def test_not_googlebot_ip(self):
        is_googlebot, name = self.googlebot('127.0.0.1',
                                            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)')
        self.assertTupleEqual((is_googlebot, name), (False, 'unknown'))

    def test_not_googlebot_user_agent(self):
        is_googlebot, name = self.googlebot('66.249.66.1',
                                            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like'
                                            ' Gecko) Chrome/80.0.3987.163 Safari/537.36')
        self.assertTupleEqual((is_googlebot, name), (False, 'unknown'))
