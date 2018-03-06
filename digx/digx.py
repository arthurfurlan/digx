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

'''
Digx is command line script used as a smarter wrapper to "dig" command that
uses the same syntax of the original command but automatically does additional
DNS queries in order to save time and give a more contextual answer.
'''

import re
import socket
from dns import resolver, reversename


class UsageError(Exception):
    ''' Exception used to detect an invalid usage error. '''

    pass


class Digx(object):
    ''' Below you can find all the logic behind "digx" command. '''

    RETVAL_ERROR_USAGE = 1

    def __init__(self):
        self.retrieve_name = False
        self.retrieve_mail = False
        self.retrieve_text = False
        self.retrieve_serv = False
        self.lookup_domain = ''

        # override default settings
        self.resolver = resolver.Resolver()

    def run(self, args):
        ''' Parse command arguments and execute as desired. '''

        self.parse_args(args)
        self.do_lookup()

    def query(self, *args, **kwargs):
        ''' Perform and cleanup DNS queries. '''

        hosts = []

        try:
            query = self.resolver.query(*args)
            for rdata in query.response.answer:
                if kwargs.get('fqdn'):
                    hosts.append(str(rdata.name).rstrip('.'))
                else:
                    for item in rdata.items:
                        hosts.append(str(item).rstrip('.'))
        except resolver.NXDOMAIN:
            pass

        return hosts

    def display_usage(self):
        ''' Display the correct "digx" usage. @TODO '''

        print('%s usage: @TODO' % self.__class__.__name__.lower())

    def parse_args(self, args):
        '''Parse the command line arguments and turn them into variables. '''

        # retrieve domain name entries
        if 'ns' in args or 'name' in args:
            self.retrieve_name = True
            args.remove('ns')

        # retrieve domain mail entries
        if 'mx' in args or 'mail' in args:
            self.retrieve_mail = True
            args.remove('mx')

        # retrieve domain text entries
        if 'txt' in args or 'text' in args:
            self.retrieve_text = True
            args.remove('txt')

        # use specific nameserver if given
        nameserver = None
        for arg in args:
            if arg.startswith('@'):
                nameserver = arg[1:]
                break
        if nameserver:
            print('rsvr: %s' % nameserver)
            print('--')
            try:
                socket.inet_aton(nameserver)
            except socket.error:
                nameserver = self.query(nameserver, 'a')[0]
            self.resolver.nameservers = [nameserver]

        # empty and/or missing arguments
        if not args:
            raise UsageError('empty and/or missing arguments.')

        # extract domain if it's an URL
        domain = re.sub('^https?://([^/]*).*$', '\\1', args[0])
        self.lookup_domain = domain

    def do_lookup(self):
        ''' Execute the lookups based on the variales of "parse_args". '''

        hosts = []
        addrs = []
        rdnss = []
        try:
            # confirm that lookup_domain is a valid IP address or except...
            socket.inet_aton(self.lookup_domain)
            addrs = [self.lookup_domain]
            rdnss = self.query(
                reversename.from_address(self.lookup_domain), 'ptr')
        except socket.error:
            # lookup sequence of all domain names
            hosts = self.query(self.lookup_domain, fqdn=True)

            # lookup all final addresses and its reverse dns
            if hosts:
                for value in self.query(hosts[-1], 'a'):
                    addrs.append(value)
                    rdnss.extend(
                        self.query(reversename.from_address(value), 'ptr'))

        # do retrieve domain name entries
        if hosts and self.retrieve_name:
            for value in self.query(hosts[-1], 'ns'):
                print('name: %s' % value)
            print('--')

        # do retrieve domain mail entries
        if hosts and self.retrieve_mail:
            for value in self.query(hosts[-1], 'mx'):
                print('mail: %s' % value.split(' ')[1])
            print('--')

        # do retrieve domain text entries
        if hosts and self.retrieve_text:
            for value in self.query(hosts[-1], 'txt'):
                print('text: %s' % value)
            print('--')

        # print hosts, address and reverse dns
        for host in hosts:
            print('host: %s' % (host))
        print('host: %s' % ', '.join(addrs))
        print('--')
        print('rdns: %s' % ', '.join(rdnss))


def cli():
    import sys

    digx = Digx()  # pylint: disable=C0103

    try:
        sys.exit(digx.run(sys.argv[1:]))
    except UsageError as ex:
        digx.display_usage()
        sys.exit(digx.RETVAL_ERROR_USAGE)


if __name__ == '__main__':
    cli()
