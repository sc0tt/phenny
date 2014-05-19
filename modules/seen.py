#!/usr/bin/env python
"""
seen.py - Phenny Seen Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import time, os, shelve, datetime
from tools import deprecated

def f_seen(phenny, input): 
    """.seen <nick> - Reports when <nick> was last seen."""
    nick = input.group(2).lower()
    if not hasattr(phenny, 'seen'): 
        return phenny.msg(input.sender, '?')
    if nick in phenny.seen: 
        channel, t = phenny.seen[nick]
        dt = timesince(datetime.datetime.utcfromtimestamp(t))
        t = time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(t))

        msg = "I last saw %s at %s (%s) on %s" % (nick, t, dt, channel)
        phenny.reply(msg)
    else: phenny.reply("Sorry, I haven't seen %s around." % nick)
f_seen.name = 'seen'
f_seen.example = '.seen firespeaker'
f_seen.rule = (['seen'], r'(\S+)')

@deprecated
def f_note(self, origin, match, args): 
    def note(self, origin, match, args): 
        if not hasattr(self.bot, 'seen'): 
            fn = self.nick + '-' + self.config.host + '.seen'
            path = os.path.join(os.path.expanduser('~/.phenny'), fn)
            self.bot.seen = shelve.open(path)
        if origin.sender.startswith('#'): 
            self.seen[origin.nick.lower()] = (origin.sender, time.time())
            self.seen.sync()

    try: note(self, origin, match, args)
    except Exception as e: print(e)
f_note.rule = r'(.*)'
f_note.priority = 'low'

def timesince(td):
    seconds = int(abs(datetime.datetime.utcnow() - td).total_seconds())
    periods = [
        ('year', 60*60*24*365),
        ('month', 60*60*24*30),
        ('day', 60*60*24),
        ('hour', 60*60),
        ('minute', 60),
        ('second', 1)
    ]

    strings = []
    for period_name, period_seconds in periods:
            if seconds > period_seconds and len(strings) < 2:
                    period_value, seconds = divmod(seconds, period_seconds)
                    if period_value == 1:
                        strings.append("%s %s" % (period_value, period_name))
                    else:
                        strings.append("%s %ss" % (period_value, period_name))

    return "just now" if len(strings) < 1 else " and ".join(strings) + " ago"

if __name__ == '__main__': 
    print(__doc__.strip())
