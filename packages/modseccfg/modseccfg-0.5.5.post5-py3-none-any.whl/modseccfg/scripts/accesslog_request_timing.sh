#!/bin/sh
# title: access.log request duration
# type: report
# category: report
# params: {logfn}

. $(dirname $0)/aliases.sh

cat "$1"  | alduration  | arbigraph --lines --logscale   2>&1
