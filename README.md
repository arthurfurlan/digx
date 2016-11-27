# digx
Digx is command line script used as a smarter wrapper to "dig" command that uses the same syntax of the original command but automatically does additional DNS queries in order to save time and give a more contextual answer.

## Usage

Retrieve the current IP address and its associated reverse address

    $ digx http://www.configr.com/planos/
    host: www.configr.com
    host: configr.com
    host: 45.79.10.58
    --
    rdns: monty.confi.gr


Retrieve the current IP address, DNS nameservers and its associated reverse address

    $ digx http://www.configr.com/planos/ ns
    name: ns2.configr.com
    name: ns1.configr.com
    --
    host: www.configr.com
    host: configr.com
    host: 45.79.10.58
    --
    rdns: monty.confi.gr


## Installation

    $ cp digx.py /usr/local/bin/digx
    $ chmod a+x /usr/local/bin/digx
