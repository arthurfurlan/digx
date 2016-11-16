#!/bin/bash

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

  if [[ "$2" == "txt" ]] || [[ "$2" == "text" ]]; then
    HA=$H
    HC=1
    while [ $HC -gt 0 ]; do
      _HA=$HA
      HA=`dig +short $HA | head -1 | sed -e 's,\.$,,'`
      if [[ "$HA" == "" ]]; then
        HA=$H
        break
      fi
      echo $HA | grep -e '[0-9]\{1,3\}\.[0-9]\{1,3\}' &> /dev/null

      if [ $? -eq 0 ]; then
        HA=$_HA
        break
      fi
    done

    i=0
    dig $HA txt | sed -e 's,\.$,,' | while read TX; do
      i=$(($i+1))
      echo "text: $TX"
    done
    
    echo '--'
  fi


  if [[ "$2" == "mx" ]] || [[ "$2" == "mail" ]]; then
    HA=$H
    HC=1
    while [ $HC -gt 0 ]; do
      _HA=$HA
      HA=`dig +short $HA | head -1 | sed -e 's,\.$,,'`
      if [[ "$HA" == "" ]]; then
        HA=$H
        break
      fi
      echo $HA | grep -e '[0-9]\{1,3\}\.[0-9]\{1,3\}' &> /dev/null

      if [ $? -eq 0 ]; then
        HA=$_HA
        break
      fi
    done

    i=0
    for MX in `dig $HA mx | cut -d ' ' -f 2 | sed -e 's,\.$,,'`; do
      i=$(($i+1))
      echo "mail: $MX"
    done
    
    if [ $i -gt 0 ]; then
      echo '--'
    fi
  fi

  if [[ "$2" == "ns" ]] || [[ "$2" == "name" ]]; then
    HA=$H
    HC=1
    while [ $HC -gt 0 ]; do
      _HA=$HA
      HA=`dig +short $HA | head -1 | sed -e 's,\.$,,'`
      if [[ "$HA" == "" ]]; then
        HA=$H
        break
      fi
      echo $HA | grep -e '[0-9]\{1,3\}\.[0-9]\{1,3\}' &> /dev/null

      if [ $? -eq 0 ]; then
        HA=$_HA
        break
      fi
    done

    i=0
    for NS in `dig $HA ns | sed -e 's,\.$,,'`; do
      i=$(($i+1))
      echo "name: $NS"
    done
    
    if [ $i -gt 0 ]; then
      echo '--'
    fi
  fi

  echo "host: ${H}"

  HA=$H
  HC=1
  
  echo $HA | grep -e '[0-9]\{1,3\}\.[0-9]\{1,3\}' &> /dev/null
  RT=$?

  HL=""
  if [ $RT -eq 1 ]; then
    while [ $HC -gt 0 ]; do
      HA=`dig +short $HA | sed -e 's,\.$,,'`
      echo $HA | grep -e '\([0-9]\{1,3\}\.[0-9]\{1,3\} \)\+' &> /dev/null
      RT=$?

      if [[ "$HA" == "" ]]; then
        break
      fi

      if [ $RT -eq 1 ]; then
        _HA=`echo ${HA} | head -1 | cut -d ' ' -f 1`
        echo "host: ${_HA}"
      else
        echo -n 'host:'

        RS=""
        for HC in $HA; do
          RS="${RS}, ${HC}"
        done
        echo "${RS}" | sed -e 's/^\s*\,//g'
        break
      fi
      HL="${HA}"
    done
  fi

  if [[ "$HL" == "" ]]; then
    HL="${HA}"
  fi

  echo '--'
  echo -n 'rdns:'

  RS=""
  for HC in $HL; do
    HB=`dig +short -x $HC 2> /dev/null`
    RS="${RS}, ${HB%%.}"
  done
  echo "${RS}" | sed -e 's/^\s*\,//g'
}
digx $@
