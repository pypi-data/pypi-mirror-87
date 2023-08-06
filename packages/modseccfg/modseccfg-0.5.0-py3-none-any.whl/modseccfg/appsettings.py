# api: python
# type: io
# title: app settings
# description: read/store modseccfg options
# depends: pluginconf (>= 0.7.2), python:appdirs (>= 1.3), python:pathlib
# category: config
# version: 0.1
# config:
#    { name: "test[key]", type: bool, value: 1, description: "Array[key] test" }
# 
# Basically just a dictionary for the GUI and some
# module behaviours. GUI courtesy of pluginconf.
#


import json, os
from modseccfg.utils import expandpath
import pluginconf, pluginconf.gui
#import appdirs

# defaults
conf = {
    "theme": "DarkGrey",
    "edit_sys_files": False,
    "log_entries": 5000,
    "log_filter": "(?!404|429)[45]\d\d",
    "log_skip_rx" : "PetalBot|/.well-known/ignore.cgi",
    "max_rule_range": 1000,  # obsolete already (SecRuleDisById ranges do a lookup)
    "sshfs_mount": "~/.config/modseccfg/mnt/",
    "backup_files": True,
    "backup_dir": "~/backup-config/",
    "conf_dir": expandpath("~/.config/modseccfg/"),
    "conf_file": "settings.json",
    "plugins": {
        "__init__": 1,
        "mainwindow": 1,
        "appsettings": 1,
        "utils": 1,
        "vhosts": 1,
        "logs": 1,
        "writer": 1
    }
}

# plugin lookup
pluginconf.module_base = __name__
pluginconf.plugin_base = [__package__]
for module,meta in pluginconf.all_plugin_meta().items():
    pluginconf.add_plugin_defaults(conf, {}, meta, module)
#print(pluginconf.module_list())
#print(conf)

# read config file
def cfg_read():
    fn = conf["conf_dir"] + "/" + conf["conf_file"]
    if os.path.exists(fn):
        conf.update(json.load(open(fn, "r", encoding="utf8")))

# write config file
def cfg_write():
    os.makedirs(conf["conf_dir"], 0o755, True)
    print(str(conf))
    fn = conf["conf_dir"] + "/" + conf["conf_file"]
    json.dump(conf, open(fn, "w", encoding="utf8"), indent=4)

# show config option dialog
def window(mainself, *kargs):
    fn_py = __file__.replace("appsettings", "*")
    save = pluginconf.gui.window(conf, conf["plugins"], files=[fn_py], theme=conf["theme"])
    if save:
        cfg_write()

# initialze conf{}
cfg_read()
