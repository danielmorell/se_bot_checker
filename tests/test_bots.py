from unittest import TestCase
from se_bot_checker.bots import Bot, BaiduSpider, BingBot, DuckDuckBot, GoogleBot, YandexBot, DNSError


class TestBot(TestCase):
    def setUp(self):
        self.bot = Bot.bot('dooglebot', 'dooglebot', ['.dooglebot.test'])
        self.bot('127.0.0.1', 'Mozilla/5.0 (compatible; Dooglebot/0.1; +http://www.dooglebot.test/bot.html)')
        self.host = self.bot.reverse_dns()
        self.valid = (True, 'dooglebot')
        self.invalid = (False, 'unknown')

    def test_run(self):
        self.assertTupleEqual(self.bot.run(), self.valid)

    def test_valid_user_agent(self):
        self.assertTrue(self.bot.valid_user_agent())

    def test_valid_domain(self):
        self.assertTrue(self.bot.valid_domain(self.host))

    def test_valid_ip(self):
        self.assertTrue(self.bot.valid_ip())

    def test_reverse_dns(self):
        self.assertTrue(self.host.endswith('.dooglebot.test'))

    def test_forward_dns(self):
        self.assertTrue(self.bot.forward_dns(self.host))

    def test_not_dooglebot_ip(self):
        try:
            is_dooglebot, name = self.bot(
                '0.0.0.0',
                'Mozilla/5.0 (compatible; Dooglebot/0.1; +http://www.dooglebot.test/bot.html)'
            )
        except DNSError:
            is_dooglebot, name = (False, 'unknown')
        self.assertTupleEqual((is_dooglebot, name), self.invalid)

    def test_not_dooglebot_user_agent(self):
        try:
            is_dooglebot, name = self.bot(
                '66.249.66.1',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
            )
        except DNSError:
            is_dooglebot, name = (False, 'unknown')
        self.assertTupleEqual((is_dooglebot, name), self.invalid)


class TestBaiduSpider(TestCase):
    def setUp(self):
        self.baiduspider = BaiduSpider()
        self.baiduspider(
            '220.181.108.120',
            'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'
        )
        self.host = self.baiduspider.reverse_dns()

    def test_run(self):
        self.assertTupleEqual(self.baiduspider.run(), (True, 'baiduspider'))

    def test_valid_user_agent(self):
        self.assertTrue(self.baiduspider.valid_user_agent())

    def test_valid_domain(self):
        self.assertTrue(self.baiduspider.valid_domain(self.host))

    def test_valid_ip(self):
        self.assertTrue(self.baiduspider.valid_ip())

    def test_reverse_dns(self):
        self.assertTrue(self.host.endswith('.baidu.com'))

    def test_not_baiduspider_ip(self):
        try:
            is_baiduspider, name = self.baiduspider(
                '10.10.10.10',
                'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'
            )
        except DNSError:
            is_baiduspider, name = (False, 'unknown')
        self.assertTupleEqual((is_baiduspider, name), (False, 'unknown'))

    def test_not_baiduspider_user_agent(self):
        try:
            is_baiduspider, name = self.baiduspider(
                '220.181.108.120',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
            )
        except DNSError:
            is_baiduspider, name = (False, 'unknown')
        self.assertTupleEqual((is_baiduspider, name), (False, 'unknown'))


class TestBingBot(TestCase):
    def setUp(self):
        self.bingbot = BingBot()
        self.bingbot('157.55.39.250', 'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)')
        self.bingbot_host = self.bingbot.reverse_dns()
        self.msnbot = BingBot()

    def test_run(self):
        self.assertTupleEqual(self.bingbot.run(), (True, 'bingbot'))

    def test_valid_user_agent(self):
        self.assertTrue(self.bingbot.valid_user_agent())

    def test_valid_domain(self):
        self.assertTrue(self.bingbot.valid_domain(self.bingbot_host))

    def test_valid_ip(self):
        self.assertTrue(self.bingbot.valid_ip())

    def test_reverse_dns(self):
        self.assertTrue(self.bingbot_host.endswith('.search.msn.com'))

    def test_forward_dns(self):
        self.assertTrue(self.bingbot.forward_dns(self.bingbot_host))

    def test_not_bingbot_ip(self):
        try:
            is_bingbot, name = self.bingbot(
                '10.10.10.10',
                'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'
            )
        except DNSError:
            is_bingbot, name = (False, 'unknown')
        self.assertTupleEqual((is_bingbot, name), (False, 'unknown'))

    def test_not_bingbot_user_agent(self):
        try:
            is_bingbot, name = self.bingbot(
                '157.55.39.250',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
            )
        except DNSError:
            is_bingbot, name = (False, 'unknown')
        self.assertTupleEqual((is_bingbot, name), (False, 'unknown'))

    def test_is_msnbot(self):
        try:
            is_msnbot, name = self.msnbot('207.46.13.182', 'msnbot/2.0b (+http://search.msn.com/msnbot.htm)')
        except DNSError:
            is_msnbot, name = (False, 'unknown')
        self.assertTupleEqual((is_msnbot, name), (True, 'bingbot'))


class TestDuckDuckBot(TestCase):
    def setUp(self):
        self.duckduckbot = DuckDuckBot()
        self.duckduckbot(
            '54.208.102.37',
            'Mozilla/5.0 (compatible; DuckDuckGo-Favicons-Bot/1.0; +http://duckduckgo.com)'
        )
        self.host = self.duckduckbot.reverse_dns()

    def test_run(self):
        self.assertTupleEqual(self.duckduckbot.run(), (True, 'duckduckbot'))

    def test_valid_user_agent(self):
        self.assertTrue(self.duckduckbot.valid_user_agent())

    def test_valid_ip(self):
        self.assertTrue(self.duckduckbot.valid_ip())

    def test_not_duckduckbot_ip(self):
        try:
            is_duckduckbot, name = self.duckduckbot(
                '10.10.10.10',
                'Mozilla/5.0 (compatible; DuckDuckGo-Favicons-Bot/1.0; +http://duckduckgo.com)'
            )
        except DNSError:
            is_duckduckbot, name = (False, 'unknown')
        self.assertTupleEqual((is_duckduckbot, name), (False, 'unknown'))

    def test_not_duckduckbot_user_agent(self):
        try:
            is_duckduckbot, name = self.duckduckbot(
                '54.208.102.37',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
            )
        except DNSError:
            is_duckduckbot, name = (False, 'unknown')
        self.assertTupleEqual((is_duckduckbot, name), (False, 'unknown'))


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
        try:
            is_googlebot, name = self.googlebot(
                '10.10.10.10',
                'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
            )
        except DNSError:
            is_googlebot, name = (False, 'unknown')
        self.assertTupleEqual((is_googlebot, name), (False, 'unknown'))

    def test_not_googlebot_user_agent(self):
        try:
            is_googlebot, name = self.googlebot(
                '66.249.66.1',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
            )
        except DNSError:
            is_googlebot, name = (False, 'unknown')
        self.assertTupleEqual((is_googlebot, name), (False, 'unknown'))


class TestYandexBot(TestCase):
    def setUp(self):
        self.yandexbot = YandexBot()
        self.yandexbot('77.88.5.141', 'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)')
        self.host = self.yandexbot.reverse_dns()

    def test_run(self):
        self.assertTupleEqual(self.yandexbot.run(), (True, 'yandexbot'))

    def test_valid_user_agent(self):
        self.assertTrue(self.yandexbot.valid_user_agent())

    def test_valid_domain(self):
        self.assertTrue(self.yandexbot.valid_domain(self.host))

    def test_valid_ip(self):
        self.assertTrue(self.yandexbot.valid_ip())

    def test_reverse_dns(self):
        self.assertTrue(
            self.host.endswith('.yandex.ru')
            or self.host.endswith('.yandex.net')
            or self.host.endswith('.yandex.com')
        )

    def test_forward_dns(self):
        self.assertTrue(self.yandexbot.forward_dns(self.host))

    def test_not_yandexbot_ip(self):
        try:
            is_yandexbot, name = self.yandexbot(
                '10.10.10.10',
                'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)'
            )
        except DNSError:
            is_yandexbot, name = (False, 'unknown')
        self.assertTupleEqual((is_yandexbot, name), (False, 'unknown'))

    def test_not_yandexbot_user_agent(self):
        try:
            is_yandexbot, name = self.yandexbot(
                '77.88.5.141',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
            )
        except DNSError:
            is_yandexbot, name = (False, 'unknown')
        self.assertTupleEqual((is_yandexbot, name), (False, 'unknown'))
