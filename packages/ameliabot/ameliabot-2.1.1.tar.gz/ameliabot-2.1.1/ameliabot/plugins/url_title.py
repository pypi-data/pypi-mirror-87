"""
Overview
========

Used to extract url titles from links.

"""

from quickirc import send_msg
from re import search, compile, sub
import requests
from ehp import *

STR_LINK  = '(?P<address>http[s]?://[^ ]*)'
REG_LINK  = compile(STR_LINK)

class UrlTitle(object):
    def __init__(self, server):
        server.add_map('CMSG', self.check)
    
    def check(self, server, nick, user, host, target, msg):
        struct = search(REG_LINK, msg)
        if not struct: 
            return
        req   = requests.get(struct.group('address'))
        html  = Html()
        dom   = html.feed(req.text)
        title = dom.fst('title').text()
        send_msg(server, target, title)

install = UrlTitle







