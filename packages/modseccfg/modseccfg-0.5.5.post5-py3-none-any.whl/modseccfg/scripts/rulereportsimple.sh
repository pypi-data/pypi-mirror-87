#!/bin/sh
# title: rulereport-simple
# description: exception examples from error.log list
# type: report
# category: report
# params: {logfn}  {count}  {debug} {verbose} {mode}
# config:
#    { name: count, arg: -n, type: select,  value: 1000, select: 100|1000|10000|999999,  description: "how many log entries to scan (tail -n)"}
#    { name: mode, arg: --mode, type: select,  value: combined, select: simple|combined|supersimple|parameter|path|graphviz,  description: "report/operation mode"}
#    { name: verbose, arg: -v, type: bool,  value: 0,  description: "more output" }
#    { name: debug,   arg: -d, type: bool,  value: 0,  description: "debugging infos" }
#
# Old rulereport tool, needs some prefiltering (else bails with XXXXX)
#

echo "# Generates possible exclusion rules."
echo "# This doesn't mean you should enable all these exceptions."
echo "#"

egrep "ModSecurity: Warning. Pattern match|ModSecurity: Warning. detected (SQLi|XSS) using libinjection" $1 | tail $2 $3 | ./modsec-rulereport.rb $4 $5 $6 $7 $8 2>&1

 
