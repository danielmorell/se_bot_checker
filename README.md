# Search Engine Bot Checker

[![Version](https://flat.badgen.net/badge/PyPI/v1.0.3)](https://pypi.org/project/se-bot-checker/)

This is a simple python library that verifies the validity of a search engine crawler based on it's IP and user agent.

It is designed to assist SEO's and DevOps validate `googlebot` and other search engine bots.

## Installation

```commandline
pip install se-bot-checker
```

## Usage

Using SE Bot Checker to validate a search engine crawler is simple. There are two basic steps.

1. Instantiate the bot class.
2. Call the bot class with IP and user agent arguments.

```python
from se_bot_checker.bots import GoogleBot
googlebot = GoogleBot()
test_one = googlebot(
    '66.249.66.1', 
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
)
test_two = googlebot(
    '127.0.0.1', 
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
)
print(test_one)
print(test_two)
```

**Output:**

```text
(True, 'googlebot')
(False, 'unknown')
```

## Prebuilt Bots

There are several bot definitions that are already created, have been tested and will be maintained. The prebuilt 
crawlers are the most common search engine crawlers.

### Crawler validation methods

| Bot           | User Agent | IP | DNS |
|---------------|------------|----|-----|
| `BaiduSpider` | X          | X* | X** |
| `BingBot`     | X          | X* | X   |
| `DuckDuckBot` | X          | X  |     |
| `GoogleBot`   | X          | X* | X   |
| `YandexBot`   | X          | X* | X   |

\* IP validation is only used on consecutive checks run using the same bot checker instance. This means that in the 
following example there will be only one DNS network request since the IP in `test_two` has already been validated when 
`test_one` was run.

\** BaiduSpider only supports reverse DNS validation not reverse and forward. Although it on first glance it appears
BaiduSpider should support reverse/forward DNS validation I have never had forward success for BaiduSpider. 

```python
from se_bot_checker.bots import GoogleBot
googlebot = GoogleBot()
test_one = googlebot(
    '66.249.66.1', 
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
)
print(test_one)  # (True, 'googlebot')
test_two = googlebot(
    '66.249.66.1', 
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
)
print(test_two)  # (True, 'googlebot')
```

### `BaiduSpider`

BaiduSpider validation only uses reverse DNS lookup not reverse and forward.

- **Name:** `baiduspider`
- **Domains:** `.baidu.com`, `.baidu.jp`
- **User Agents:** `baiduspider`
- **Use RegEx:** `False`


### `BingBot`

- **Name:** `bingbot`
- **Domains:** `.search.msn.com`
- **User Agents:** `bingbot`, `msnbot`, `bingpreview`
- **Use RegEx:** `True`

### `DuckDuckBot`

DuckDuckBot only uses IP validation from the list of valid IPs.

- **Name:** `duckduckbot`
- **IPs:** See list below
- **User Agents:** `duckduckbot`, `duckduckgo`
- **Use RegEx:** `True`

```text
20.191.45.212
40.88.21.235
40.76.173.151
40.76.163.7
20.185.79.47
52.142.26.175
20.185.79.15
52.142.24.149
40.76.162.208
40.76.163.23
40.76.162.191
40.76.162.247
54.208.102.37
107.21.1.8

Updated: January 31, 2022
```

### `GoogleBot`

- **Name:** `googlebot`
- **Domains:** `.googlebot.com`, `.google.com`
- **User Agents:** `googlebot`
- **Use RegEx:** `False`

### `YandexBot`

- **Name:** `bingbot`
- **Domains:** `.search.msn.com`
- **User Agents:** `bingbot`, `msnbot`, `bingpreview`
- **Use RegEx:** `True`

## Creating Your Own Bot Definition

SE Bot Checker was designed to be extensible. The core of SE Bot Checker is the `Bot` class. To create your own 
bot you can simply extend `Bot`.

Here is custom bot that will only validate Googlebot mobile.

```python
from se_bot_checker.bots import Bot

class MobileGoogleBot(Bot):
    """
    Mobile googlebot checker
    """
    name = 'googlebot-mobile'
    domains = ['.googlebot.com', '.google.com']
    user_agent = 'android.*googlebot'
```

That is all there is to it. However, we could simplify this a little by extending the `GoogleBot` class.

```python
from se_bot_checker.bots import GoogleBot

class MobileGoogleBot(GoogleBot):
    """
    Mobile googlebot checker
    """
    name = 'googlebot-mobile'
    user_agent = 'android.*googlebot'
```

Both the desktop and mobile versions of Googlebot use the same domains for the reverse/forward DNS validation. This 
means we can simply extend `GoogleBot`. This is the recommended approach when possible.

### `Bot` API

This class is the core of SE Bot Checker. It handles the validation process. New bot definitions should subclass this 
class.

A single bot class can be instantiated once and called many times. The allows base settings to be configured and 
multiple IP and user agent pairs to be validated simply.

**`Bot.name`:** `str` This is the name the bot will return if it validates to `True`.

**`Bot.ips`:** `iterable` A list of known valid IPs.

**`Bot.domains`:** `iterable` A list of known valid domains. This is used to validate the results of the reverse
DNS lookup. An exact match or a super domain of the DNS lookup results is considered a positive match.

**`Bot.user_agent`:** `str` A substring or RegEx pattern to use to validate the request user agent. For the best
performance and compatibility request user agent string are changed to lowercase prior to matching. the `user_agent` 
string should be lower case. If you need to validate upper or mixed case user agents you can override the 
`Bot.valid_user_agent()` method.

**`Bot.use_regex`:** `bool` Whether the user agent validation should use substring or regex matching. If 
`user_agent` is just a string and not a RegEx pattern this should be `False`. It slightly faster. Defaults to `False`.

## Contributors

[@danielmorell](https://github.com/danielmorell)

Copyright © 2020 [Daniel Morell](https://www.danielmorell.com/)