#!/usr/bin/python3
"""
botfun.py - activities that bots do
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import random

otherbot = "The_Pacifist"

def botfight(phenny, input):
    usr = input.group(2)
    if not usr:
        usr = input.nick
    messages = ["hits %s", "punches %s", "kicks %s", "hits %s with a rubber hose", "stabs %s with a clean kitchen knife"]
    response = random.choice(messages)

    phenny.do(response % usr)
botfight.commands = ['botfight']
botfight.priority = 'low'

def bothug(phenny, input):
    usr = input.group(2)
    if not usr:
        usr = input.nick
    phenny.do("hugs %s" % usr)
bothug.commands = ['bothug']
bothug.priority = 'low'

if __name__ == '__main__':
    print(__doc__.strip())
