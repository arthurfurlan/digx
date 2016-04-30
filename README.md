# digx
Bash wrapper of dig command to make it easier to resolve website hosts and its associated reverse addresses

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
