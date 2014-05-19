#!/usr/bin/python3
"""
hs.py - hokie stalker module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

from tools import GrumbleError
import web
import lxml.etree

SEARCH_URL = "https://webapps.middleware.vt.edu/peoplesearch/PeopleSearch?query={0}&dsml-version=2"
RESULTS_URL = "http://search.vt.edu/search/people.html?q={0}"
PERSON_URL = "http://search.vt.edu/search/person.html?person={0:d}"
NS = '{http://www.dsml.org/DSML}'

"""Search the people search database using the argument as a query."""
def search(query):
    query = web.quote(query)
    try:
        r = web.get(SEARCH_URL.format(query), verify=False)
    except (web.ConnectionError, web.HTTPError):
        raise GrumbleError("THE INTERNET IS FUCKING BROKEN. Please try again later.")

    # apparently the failure mode if you search for <3 characters is a blank
    # XML page...
    if len(r) <= 0:
        return False

    xml = lxml.etree.fromstring(r.encode('utf-8'))
    results = xml.findall('{0}directory-entries/{0}entry'.format(NS))
    if len(results) <= 0:
        return False

    ret = []
    for entry in results:
        entry_data = {}
        for attr in entry.findall('{0}attr'.format(NS)):
            entry_data[attr.attrib['name']] = attr[0].text
        ret.append(entry_data)

    return ret

def hs(phenny, input):
    """.hs <pid/name/email> - Search for someone on Virginia Tech People Search."""

    q = input.group(2)
    if q is None:
        return
    q = q.strip()
    results = RESULTS_URL.format(web.quote(q))

    s = search(q)
    if s:
        if len(s) >1:
            phenny.reply("Multiple results found; try {0}".format(results))
        else:
            for entry in s:
                person = PERSON_URL.format(int(entry['uid']))
                phenny.reply("{0} - {1}".format(entry['cn'], person))
    else:
        phenny.reply("No results found")
hs.rule = (['hs'], r'(.*)')

if __name__ == '__main__':
    print(__doc__.strip())
