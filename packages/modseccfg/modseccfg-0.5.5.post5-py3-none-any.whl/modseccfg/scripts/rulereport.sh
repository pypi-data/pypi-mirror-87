#!/bin/sh
# title: rulereport
# description: craft exception rules based on error.log details
# type: report
# category: report
# params: {logfn}   {help} {debug} {verbose} {mode} {type} {by}
# config:
#    { name: mode, arg: "", type: select,  value:"--runtime", select: "--runtime|--startup",  description: "runtime (SecRuleRemove* / *.conf) or startup (SecRule ctl: / *.preconf) exclusion" }
#    { name: type, arg: "", type: select,  value: "--rule",   select: "--rule|-R|--target|-T",  description: "Exclude rule or parameter" }
#    { name: by,   arg: "", type: select,  value: "--byid",   select: "--byid|--bytag|--bymsg",  description: "Select rule via rule id" }
#    { name: verbose, arg: --verbose, type: bool,  value: 1,  description: "more output" }
#    { name: debug,   arg: --debug,   type: bool,  value: 0,  description: "debugging infos" }
#    { name: help,    arg: --help,    type: bool,  value: 0,  description: "review --help" }
# state: beta
#  
#  modsec-rulereport-new.rb
#
#  Requires one of each:
#    -s -r
#    -R -T
#    -i -t -m
#  
#  This script is (c) 2010-2017 by Christian Folini, netnea.com
#  It has been released under the GPLv3 license.
#  Contact: mailto:christian.folini@netnea.com
#  


echo "# Again, these should be considered configuration examples, but not applied"
echo "# without checkking if the listed rules are working as intended."
echo "#"
echo "# cat $1 | ./modsec-rulereport.rb $2 $3 $4 $5 $6"
echo "#"


cat $1 | ./modsec-rulereport-new.rb $2 $3 $4 $5 $6 2>&1

