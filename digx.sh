#!/bin/sh

# Copyright (C) 2016 Arthur Furlan <afurlan@configr.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# On Debian systems, you can find the full text of the license in
# /usr/share/common-licenses/GPL-2


## make it easier to resolve website hosts and its reverse addresses
digx() {
  H=`echo $1 | sed -e 's,^https*://*,,' -e 's,/.*,,'`
  echo "host: ${H}"

  HA=$H
  HC=1
  while [ $HC -gt 0 ]; do
    HA=`dig +short $HA | head -1 | sed -e 's,\.$,,'`
    echo $HA | grep -e '[0-9]\{1,3\}\.[0-9]\{1,3\}' &> /dev/null

    if [ $? -eq 1 ]; then
      echo "host: ${HA}"
    else
      echo "host: ${HA}"
      break
    fi
  done

  HB=`dig +short -x $HA 2> /dev/null`
  echo "--"
  echo "rdns: ${HB%%.}"
}
digx $@
