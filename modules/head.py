#!/usr/bin/env python
"""
head.py - Phenny HTTP Metadata Utilities
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import re
import urllib.parse
import time
from html.entities import name2codepoint
import web
from tools import deprecated
from modules.linx import get_title as linx_gettitle


def head(phenny, input):
    """Provide HTTP HEAD information."""
    uri = input.group(2)
    uri = (uri or '')
    if ' ' in uri:
        uri, header = uri.rsplit(' ', 1)
    else:
        uri, header = uri, None

    if not uri and hasattr(phenny, 'last_seen_uri'):
        try:
            uri = phenny.last_seen_uri[input.sender]
        except KeyError:
            return phenny.say('?')

    if not uri.startswith('htt'):
        uri = 'http://' + uri
    # uri = uri.replace('#!', '?_escaped_fragment_=')
    start = time.time()

    try:
        info = web.head(uri)
        info['status'] = '200'
    except web.HTTPError as e:
        if hasattr(e, 'code'):
            return phenny.say(str(e.code))
        else:
            return phenny.say(str(e.response.status_code))
    except web.ConnectionError:
        return phenny.say("Can't connect to %s" % uri)

    resptime = time.time() - start

    if header is None:
        data = []
        if 'Status' in info:
            data.append(info['Status'])
        if 'content-type' in info:
            data.append(info['content-type'].replace('; charset=', ', '))
        if 'last-modified' in info:
            modified = info['last-modified']
            modified = time.strptime(modified, '%a, %d %b %Y %H:%M:%S %Z')
            data.append(time.strftime('%Y-%m-%d %H:%M:%S UTC', modified))
        if 'content-length' in info:
            data.append(info['content-length'] + ' bytes')
        data.append('{0:1.2f} s'.format(resptime))
        phenny.reply(', '.join(data))
    else:
        headerlower = header.lower()
        if headerlower in info:
            phenny.say(header + ': ' + info.get(headerlower))
        else:
            msg = 'There was no %s header in the response.' % header
            phenny.say(msg)
head.commands = ['head']
head.example = '.head http://www.w3.org/'


r_title = re.compile(r'(?ims)<title[^>]*>(.*?)</title\s*>')
r_entity = re.compile(r'&[A-Za-z0-9#]+;')


def noteuri(phenny, input):
    uri = input.group(1)
    if not hasattr(phenny.bot, 'last_seen_uri'):
        phenny.bot.last_seen_uri = {}
    phenny.bot.last_seen_uri[input.sender] = uri
noteuri.rule = r'.*(http[s]?://[^<> "\x01]+)[,.]?'
noteuri.priority = 'low'



def snarfuri(phenny, input):
    uri = input.group(1)

    if phenny.config.linx_api_key != "":
        title = linx_gettitle(phenny, uri, input.sender)
    else:
        title = gettitle(phenny, uri)

    if title:
        phenny.msg(input.sender, title)
snarfuri.rule = r'.*(http[s]?://[^<> "\x01]+)[,.]?'
snarfuri.priority = 'low'
snarfuri.thread = True


def gettitle(phenny, uri):
    if not ':' in uri:
        uri = 'http://' + uri
    uri = uri.replace('#!', '?_escaped_fragment_=')

    title = None
    localhost = [
        'http://localhost/', 'http://localhost:80/',
        'http://localhost:8080/', 'http://127.0.0.1/',
        'http://127.0.0.1:80/', 'http://127.0.0.1:8080/',
        'https://localhost/', 'https://localhost:80/',
        'https://localhost:8080/', 'https://127.0.0.1/',
        'https://127.0.0.1:80/', 'https://127.0.0.1:8080/',
    ]
    for s in localhost:
        if uri.startswith(s):
            return phenny.reply('Sorry, access forbidden.')

    try:
        redirects = 0
        while True:
            info = web.head(uri)

            if not isinstance(info, list):
                status = '200'
            else:
                status = str(info[1])
                info = info[0]
            if status.startswith('3'):
                uri = urllib.parse.urljoin(uri, info['Location'])
            else:
                break

            redirects += 1
            if redirects >= 25:
                return None

        try:
            mtype = info['content-type']
        except:
            return None

        if not (('/html' in mtype) or ('/xhtml' in mtype)):
            return None

        bytes = web.get(uri)
        #bytes = u.read(262144)
        #u.close()

    except:
        return

    m = r_title.search(bytes)
    if m:
        title = m.group(1)
        title = title.strip()
        title = title.replace('\t', ' ')
        title = title.replace('\r', ' ')
        title = title.replace('\n', ' ')
        while '  ' in title:
            title = title.replace('  ', ' ')
        if len(title) > 200:
            title = title[:200] + '[...]'

        def e(m):
            entity = m.group(0)
            if entity.startswith('&#x'):
                cp = int(entity[3:-1], 16)
                return chr(cp)
            elif entity.startswith('&#'):
                cp = int(entity[2:-1])
                return chr(cp)
            else:
                char = name2codepoint[entity[1:-1]]
                return chr(char)
        title = r_entity.sub(e, title)

        if title:
            title = title.replace('\n', '')
            title = title.replace('\r', '')
            title = "[ {0} ]".format(title)
        else:
            title = None
    return title


if __name__ == '__main__':
    print(__doc__.strip())
