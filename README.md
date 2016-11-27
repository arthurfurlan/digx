# digx
Digx is command line script used as a smarter wrapper to "dig" command that uses the same syntax of the original command but automatically does additional DNS queries in order to save time and give a more contextual answer.

## Usage

Retrieve the current IP address and its associated reverse address

    $ digx www.acidezfeminina.com.br
    host: www.acidezfeminina.com.br
    host: acidezfeminina.com.br
    host: 45.79.212.127
    --
    rnds: cloud288.configrapp.com


Retrieve the current IP address, DNS nameservers and its associated reverse address

    $ digx http://www.acidezfeminina.com.br ns
    name: ns2.configr.com
    name: ns1.configr.com
    --
    host: www.acidezfeminina.com.br
    host: acidezfeminina.com.br
    host: 45.79.212.127
    --
    rnds: cloud288.configrapp.com


## Installation

    $ pip install -r requirements.txt
    $ cp digx.py /usr/local/bin/digx
    $ chmod a+x /usr/local/bin/digx
