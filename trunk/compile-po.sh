#!/bin/sh
# compile pt_BR.po pt
msgfmt $1 -o "locale/$2/en/LC_MESSAGES/acqua.mo"
