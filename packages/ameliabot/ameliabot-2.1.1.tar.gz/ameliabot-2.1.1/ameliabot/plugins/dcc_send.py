"""
Overview
========

Used to download files from the bot.

Commands
========

Command: @dcc-send filename port
Description: Send file whose name is filename to the nick that issued the command.

See: booklist plugin for listing shared files.
"""

from quickirc import DccServer, send_msg
from untwisted.iputils import ip_to_long
from untwisted.event import DONE, TIMEOUT, CLOSE
from os.path import getsize, join
from socket import error
from ameliabot.cmd import command

HEADER = '\001DCC SEND %s %s %s %s\001' 

class Send(object):
    def __init__(self, server, folder):
        self.folder = folder
        server.add_map('CMSG', self.dcc_send)

    @command('@dcc-send filename port')
    def dcc_send(self, server, nick, user, host, target, msg, filename, port):
    
        path = join(self.folder, filename)
        size = getsize(path)
        fd   = open(path, 'rb')
    
        try:
            dccserv = DccServer(fd, int(port))
        except error:
            send_msg(server, nick, "It couldn't listen on the port")
        else:
            request = HEADER % (filename, ip_to_long(server.myaddr), port, size)

            send_msg(server, nick, request)
        
            def is_done(dccserv, client, msg):
                send_msg(server, nick, msg)
                fd.close()
        
            dccserv.add_map(DONE, is_done, 'Done.')
            dccserv.add_map(CLOSE, lambda dccserv, client, err: is_done(dccserv, client, 'Failed.'))
        
            # TIMEOUT is an event that occurs in the dccsev ssock
            # instance not in the client instance.
            # The client instance is the ssock instance that
            # corresponds to the client socket. So, we need to pass
            # None otherwise we get an exception. The None would correspond
            # to client in the position at is_done.
            dccserv.add_map(TIMEOUT, is_done, None, "TIMEOUT. Server is down.")
        
        
install = Send








