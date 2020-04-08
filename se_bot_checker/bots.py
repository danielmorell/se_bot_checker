"""
bots.py

Project: SE Bot Checker
Contents: bots
Author: Daniel Morell
Added v1.0.0 -- 4/7/2020
"""
# Standard Library Imports
import re
import socket
from typing import Tuple, List

# Local Imports


class DNSError(OSError):
    pass


class AbstractBot:
    name = ''
    ips = []
    domains = []
    user_agent = ''
    use_regex = False

    use_reverse_dns = True

    request_ip = None
    request_user_agent = None

    def __init__(self, use_reverse_dns: bool = None):
        if use_reverse_dns is not None:
            self.use_reverse_dns = use_reverse_dns

    def __call__(self, ip: str, user_agent: str) -> Tuple[bool, str]:
        self.request_ip = ip
        self.request_user_agent = user_agent.lower()
        return self.run()

    def run(self) -> Tuple[bool, str]:
        """
        Run the bot validation.
        :return: Tuple[bool, str]
        """
        # Test: 1 - User Agent Match
        # Bail early if user agent does not match. Return a negative match
        if not self.valid_user_agent():
            return False, 'unknown'
        # Test 2 - IP Match
        # Bail early if request IP is valid
        if self.valid_ip():
            return True, self.name
        # If DNS look up disabled and we have made it this far return negative match
        if not self.use_reverse_dns:
            return False, 'unknown'
        # Run reverse DNS validation
        # Get the host with a reverse DNS lookup
        host = self.reverse_dns()
        # Validate host domain. If not valid return negative match
        if not self.valid_domain(host):
            return False, 'unknown'
        # Validate forward DNS host matches IP.
        if not self.forward_dns(host):
            return False, 'unknown'
        # All tests passed
        # Add request IP to the list of valid IPs
        self.ips.append(self.request_ip)
        return True, self.name

    def valid_user_agent(self) -> bool:
        if self.use_regex:
            return bool(re.search(self.user_agent, self.request_user_agent))
        return self.user_agent in self.request_user_agent

    def valid_domain(self, host: str) -> bool:
        match = False
        for domain in self.domains:
            if host.endswith(domain):
                match = True
        return match

    def valid_ip(self) -> bool:
        if not self.ips:
            return False
        return self.request_ip in self.ips

    def reverse_dns(self) -> str:
        """

        :return:
        :raises: DNSError
        """
        try:
            host = socket.gethostbyaddr(self.request_ip)[0]
        except OSError:
            raise DNSError('Reverse DNS lookup failed. Server could not be found. Check your network.')
        return host

    def forward_dns(self, host) -> bool:
        """

        :return:
        :raises: DNSError
        """
        try:
            ip = socket.gethostbyname(host)
        except OSError:
            raise DNSError('Forward DNS lookup failed. Server could not be found. Check your network.')
        return ip == self.request_ip


class InstantBot(AbstractBot):
    def __init__(self, name: str, user_agent: str, domains: List[str] = [], use_regex: bool = False,
                 use_reverse_dns: bool = None):
        super().__init__(use_reverse_dns=use_reverse_dns)
        self.name = name
        self.user_agent = user_agent
        self.domains = domains
        self.use_regex = use_regex


class GoogleBot(AbstractBot):
    name = 'googlebot'
    domains = ['googlebot.com', 'google.com']
    user_agent = 'googlebot'


class BingBot(AbstractBot):
    name = 'bingbot'
    domains = ['search.msn.com']
    user_agent = r'bingbot|msnbot|bingpreview'
    use_regex = True


class YandexBot(AbstractBot):
    name = 'yandexbot'
    domains = ['yandex.ru', 'yandex.net', 'yandex.com']
    user_agent = r'yandex|yadirectfetcher'
    use_regex = True


class DuckDuckBot(AbstractBot):
    name = 'duckduckbot'
    ips = [
            '23.21.227.69',
            '50.16.241.113',
            '50.16.241.114',
            '50.16.241.117',
            '50.16.247.234',
            '52.204.97.54',
            '52.5.190.19',
            '54.197.234.188',
            '54.208.100.253',
            '54.208.102.37',
            '107.21.1.8',
        ]
    user_agent = r'duckduckbot|duckduckgo'
    use_regex = True
