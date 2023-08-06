# encoding: utf-8
# api: modseccfg
# title: Writer
# description: updates *.conf files with new directives
# version: 0.5
# type: file
# category: config
# config:
#     { name: write_etc, type: bool, value: 0, description: "Write to /etc without extra warnings", help: "Normally modseccfg would not update default apache/modsecurity config files." }
#     { name: write_sudo, type: bool, value: 0, description: "Use sudo to update non-writable files", help: "Run `sudo` on commandline to update files, if permissions insufficient" }
#     { name: backup_files, value: 1, type: bool, description: "Copy files to ~/backup-config/ before rewriting" }
#     { name: backup_dir, value: "~/backup-config/", type: str, description: "Where to store copies of configuration files" }
# state: alpha
#
# Reads, updates and then writes back configuration files.
# Contains multiple functions for different directives.
# Some need replacing, while others (lists) just need to be
# appended.
# 


import os, re, time, shutil
from modseccfg import vhosts, utils
from modseccfg.utils import srvroot, conf
import PySimpleGUI as sg


class rx:
    pfx = re.compile(r"""
        ^(\h*)\w+
    """, re.X|re.M)
    end = re.compile(r"""
        ^(?=\s*</VirtualHost>) | \Z
    """, re.X|re.M)


#-- file I/O --

# read src from config file
def read(fn):
    return srvroot.read(fn)

# update file
def write(fn, src):
    is_system_file = re.search("^/etc/|^/usr/share/", fn) and not re.search("/sites-enabled/|/crs-setup.conf|RE\w+-\d+-EXCLUSION", fn)
    if is_system_file and not conf.write_etc:
        # alternatively check for `#editable:1` header with pluginconf
        if sg.popup_yes_no(f"Default Apache/mod_sec config file '{fn}' should not be updated. Proceed anyway?") != "Yes":
            return
    if not srvroot.writable(fn):
        sg.popup_cancel(f"Config file '{fn}' isn't writeable. (Use chown/chmod to make it so.)")
        # elif conf.write_sudo: write_sudo(fn, src)
        return
    # save a copy before doing anything else
    if conf.backup_files:
        backup(fn)
    # actually write
    srvroot.write(fn, src)

# copy *.conf to ~/backup-config/
def backup(fn):
    dir = utils.expandpath(conf.backup_dir)
    os.makedirs(dir, 0o751, True)
    dest = re.sub("[^\w\.\-\+\,]", "_", fn)
    dest = f"{dir}/{time.time()}.{dest}"
    shutil.copyfile(srvroot.fn(fn), dest)

# write to file via sudo/tee pipe instead
def write_sudo(fn, src):
    p = subprocess.Popen(['sudo', 'tee'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p.stdin.write(src.encode("utf-8"))
    p.stdin.close()
    print(p.stdout.read())
    p.wait()


# detect if changes should go to vhost.*.preconf
# this will probably just be used by recipes to swap out the target filename
def fn_preconf(fn, addsrc, create_from_vh={}):
    return fn

# detect leading whitespace
def pfx(src):
    space = rx.pfx.findall(src)
    if space:
        return space[0]
    else:
        return ""


#-- update methods --

# directive insertion doesn't look for context
def append(fn, directive, value, comment=""):
    src = read(fn)
    insert = f"{pfx(src)}{directive} {value}   {comment}\n"
    srcnew = rx.end.sub(insert, src, 1)
    write(fn, srcnew)        # count ↑ =0 would insert before all </VirtualHost> markers

# strip SecRuleRemoveById …? nnnnnnn …?
def remove_remove(fn, directive, value):
    src = read(fn)
    variants = {
        rf"^\s* {directive} \s+ {value} \s* (\#.*)?$": r'',
        rf"^ ( \s*{directive} \s+ (?:\d+\s+)+ ) \b{value}\b ( .* )$": r'\1\2'
    }
    for rx,repl in variants.items():
        if re.search(rx, src, re.X|re.M|re.I):
            src = re.sub(rx, repl, src, 1, re.X|re.M|re.I)
            return write(fn, src)
    print("NOT FOUND / NO CHANGES")

# list of SecOptions to be added/changed
def update_or_add(fn, pairs):
    src = read(fn)
    spc = pfx(src)
    for dir,val in pairs.items():
        # dir=regex
        if type(dir) is re.Pattern:
            if re.search(dir, src):
                src = re.sub(dir, val, src, 1)
            else:
                src = src + val
        # StringDirective
        elif re.search(rf"^[\ \t]*({dir}\b)", src, re.M|re.I):
            src = re.sub(rf"^([\ \t]*)({dir}\b).+\n", f"\\1{dir} {val}\n", src, 1, re.M|re.I)
        else:
            src = src + f"{spc}{dir} {val}\n"
    write(fn, src)

