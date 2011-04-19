#!/usr/bin/env python

import urllib

BASEURL = "http://bases.bireme.br/cgi-bin/mxlindG4.exe/cgi=@cid10/cid10"


def wordsSearch(words=""):
    params = {'words': words.strip()}
    return getContent(BASEURL, params)


def boolSearch(bool_="", index=""):
    params = {'bool' : index.strip() + " " + bool_.strip()}
    return getContent(BASEURL, params)


def tree_idSearch(tree_id=""):
    params = {'tree_id': tree_id.strip(), 'lang':'pt'}
    return getContent(BASEURL, params)


def getContent(url, params):
    parameters = urllib.urlencode(params)
    handle = urllib.urlopen("%s?%s" %(url,parameters))
    content = handle.read()
    handle.close()
    return content

print tree_idSearch('S05.1')
