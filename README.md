# digx
Bash wrapper of dig command to make it easier to resolve website hosts and its associated reverse addresses

## Usage

    $ digx http://www.configr.com/
    host: www.configr.com
    host: configr.com
    host: 45.79.10.58
    --
    rdns: monty.confi.gr


## Installation

    $ cp digx.sh /usr/local/bin/digx
    $ chmod a+x /usr/local/bin/digx
