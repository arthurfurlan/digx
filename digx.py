#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2016 Arthur Furlan <afurlan@configr.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# On Debian systems, you can find the full text of the license in
# /usr/share/common-licenses/GPL-2

from dns import resolver, reversename
import socket
import re


class UsageError(Exception):
    pass


# make it easier to resolve website hosts and its reverse addresses
class Digx(object):

    RETVAL_ERROR_USAGE = 1

    def __init__(self):
        self.retrieve_name = False
        self.retrieve_mail = False
        self.retrieve_text = False
        self.retrieve_serv = False
        self.lookup_domain = ''

    def run(self, args):
        retval = self.parse_args(args)
        self.do_lookup()

    def display_usage(self):
        print 'USAGE: @TODO'

    def parse_args(self, args):

        # retrieve domain name entries
        if 'ns' in args:
            self.retrieve_name = True
            args.remove('ns')

        # retrieve domain mail entries
        if 'mx' in args:
            self.retrieve_mail = True
            args.remove('mx')

        # retrieve domain text entries
        if 'txt' in args:
            self.retrieve_text = True
            args.remove('txt')

        # empty and/or missing arguments
        if not args:
            raise UsageError('empty and/or missing arguments.')

        # extract domain if it's an URL
        domain = re.sub('^https?://([^/]*).*$', '\\1', args[0])
        self.lookup_domain = domain

    def do_lookup(self):

        # lookup sequence of all domain names
        query = resolver.query(self.lookup_domain)
        hosts = []
        for rdata in query.response.answer:
            hosts.append(str(rdata.name).rstrip('.'))

        # lookup final address and reverse dns
        addr = []
        rdns = []
        query = resolver.query(hosts[-1], 'a')
        for rdata in query.response.answer[0].items:
            value = str(rdata).rstrip('.')
            addr.append(value)
            value = reversename.from_address(value)
            rdns.append(str(resolver.query(value, 'PTR')[0]).rstrip('.'))

        # do retrieve domain name entries
        if self.retrieve_name:
            query = resolver.query(hosts[-1], 'ns')
            for rdata in query.response.answer[0].items:
                print 'name: %s' % str(rdata).rstrip('.')
            print '--'

        # do retrieve domain mail entries
        if self.retrieve_mail:
            query = resolver.query(hosts[-1], 'mx')
            for rdata in query.response.answer[0].items:
                print 'mail: %s' % str(rdata).rstrip('.').split(' ')[1]
            print '--'

        # do retrieve domain serv entries
        if self.retrieve_text:
            query = resolver.query(hosts[-1], 'txt')
            for rdata in query.response.answer[0].items:
                print 'text: %s' % str(rdata).rstrip('.')
            print '--'

        # print hosts, address and reverse dns
        hosts.extend(addr)
        for host in hosts:
            print 'host: %s' % host
        print '--'
        for k, v in enumerate(rdns):
            if len(rdns) > 1:
                print 'rnds: %s (%s)' % (v, addr[k])
            else:
                print 'rnds: %s' % v


if __name__ == '__main__':
    import sys

    args = sys.argv[1:]
    digx = Digx()

    try:
        digx.run(args)
    except UsageError, ex:
        digx.display_usage()
        sys.exit(Digx.RETVAL_ERROR_USAGE)
