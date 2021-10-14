#!/bin/bash

python3 ldap_get_info.py --host="ldapad" \
  --port="389" \
  --user="uid=test,ou=users,dc=wimpi,dc=net" \
  --pass="secret" \
  --base="dc=wimpi,dc=net"