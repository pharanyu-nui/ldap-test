#!/bin/bash

python3 ldap_get_info.py --host="openldap" \
  --port="389" \
  --user="admin" \
  --pass="admin_pass" \
  --base="dc=ramhlocal,dc=com"
