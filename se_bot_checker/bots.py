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


class Bot:
    """
    This class is the core of SE Bot Checker. It handles the validation process. All
    bot definitions should subclass this class.

    A single bot class can be instantiated once and called many times. The allows
    base settings to be configured and multiple IP and user agent pairs to be
    validated simply.
    """
    name = ''
    ips = []
    domains = []
    user_agent = ''
    use_regex = False

    use_reverse_dns = True

    request_ip = None
    request_user_agent = None

    def __init__(self, name: str, user_agent: str, domains: List[str] = [], use_regex: bool = False,
                 use_reverse_dns: bool = None):
        """
        The bot class constructor method.

        :param name: The name of the new bot to return if valid.
        :type name: str
        :param user_agent: The user agent signature to match ``request_user_agent``
            strings against.
        :type user_agent: str
        :param domains: A list of valid domains that the reverse DNS host can match.
            Defaults to an empty list.
        :type domains: List[str]
        :param use_regex: ``True`` if you want to use RegEx to match the user agent.
            Defaults to ``False``.
        :type use_regex: bool
        :param use_reverse_dns: ``True`` if DNS requests should be made. This can slow
            down the validation. However, for most crawlers this is the only way to
            verify the validity of a crawler IP. You can turn this off if you want to
            quickly match against a list of known valid IPs.
        :type use_reverse_dns: bool
        """
        if use_reverse_dns is not None:
            self.use_reverse_dns = use_reverse_dns
        self.name = name
        self.user_agent = user_agent
        self.domains = domains
        self.use_regex = use_regex

    def __call__(self, ip: str, user_agent: str) -> Tuple[bool, str]:
        """
        This method runs the validation.

        :param ip: This is the IP of the crawler to validate.
        :type ip: str
        :param user_agent: This is the user agent string of the crawler.
        :type user_agent: str
        :return: Tuple[bool, str] --
        """
        self.request_ip = ip
        self.request_user_agent = user_agent
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
        """
        Checks if the ``request_user_agent`` matches the bot ``user_agent`` signature.

        If ``use_regex`` is ``True``, a RegEx search will be performed. Otherwise
        simple substring matching will be used.

        :return: bool -- True if ``request_user_agent`` matches the signature.
        """
        if self.use_regex:
            return bool(re.search(self.user_agent, self.request_user_agent.lower()))
        return self.user_agent in self.request_user_agent.lower()

    def valid_domain(self, host: str) -> bool:
        """
        Checks if the ``host`` is matches a valid domain or super domain.

        :param host: The host name form :func:`reverse_dns`.
        :type host: str
        :return:
        """
        match = False
        for domain in self.domains:
            if host.endswith(domain):
                match = True
        return match

    def valid_ip(self) -> bool:
        """
        Checks if the ``request_ip`` is in the list of valid IPs, ``ips``.

        :return: bool -- True if ``request_ip`` is in ``ips``
        """
        if not self.ips:
            return False
        return self.request_ip in self.ips

    def reverse_dns(self) -> str:
        """
        Performs a reverse DNS query based on the ``request_ip``

        If there is a network error or the server IP is unreachable a :class:`DNSError`
        error will be raised.

        :return: str -- The host for the ``request_ip``
        :raises: DNSError
        """
        try:
            host = socket.gethostbyaddr(self.request_ip)[0]
        except OSError:
            raise DNSError('Reverse DNS lookup failed. Server could not be found. Check your network.')
        return host

    def forward_dns(self, host) -> bool:
        """
        Performs a forward DNS query based on the ``host``

        If there is a network error or the server IP is unreachable a :class:`DNSError`
        error will be raised.

        :return: bool -- ``True`` if the forward DNS IP and ``request_ip`` match.
        :raises: DNSError
        """
        try:
            ip = socket.gethostbyname(host)
        except OSError:
            raise DNSError('Forward DNS lookup failed. Server could not be found. Check your network.')
        return ip == self.request_ip


class GoogleBot(Bot):
    """
    A prebuilt GoogleBot bot checker class.
    """
    name = 'googlebot'
    domains = ['.googlebot.com', '.google.com']
    user_agent = 'googlebot'


class BingBot(Bot):
    """
    A prebuilt BingBot bot checker class.
    """
    name = 'bingbot'
    domains = ['.search.msn.com']
    user_agent = r'bingbot|msnbot|bingpreview'
    use_regex = True


class YandexBot(Bot):
    """
    A prebuilt YandexBot bot checker class.
    """
    name = 'yandexbot'
    domains = ['yandex.ru', 'yandex.net', 'yandex.com']
    user_agent = r'yandex|yadirectfetcher'
    use_regex = True


class DuckDuckBot(Bot):
    """
    A prebuilt DuckDuckBot bot checker class.
    """
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
