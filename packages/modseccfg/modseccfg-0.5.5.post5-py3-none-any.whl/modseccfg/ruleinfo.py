# encoding: utf8
# api: modseccfg
# type: function
# category: gui
# title: Rule Info
# description: displays details (params/flags) of mod_security rule
# version: 0.2
# config:
#    { name: info_log_count, type: int, value: 7, description: Number of log entries to show. }
# license: Apache-2.0
#
# Brings up a text window to visualise SecRule flags and options.
# Highlights some interesting flags, and appends recent log entries
# about the rule when available.
#


import re, json
from modseccfg import utils, vhosts, icons
from modseccfg.utils import conf
import PySimpleGUI as sg
import textwrap


def wrap(s, w=60):
    return "\n".join(textwrap.wrap(s, w))


def show(id, log_values=None, vh=None):

    # display options to pass as **style.name to sg.T() widgets
    style = utils.DictObj({
        "head":  dict(font=("Ubuntu", 20, "bold")),
        "virt":  dict(text_color="gray"),
        "state": dict(font=("Ubuntu", 18, "bold"), text_color="darkgray"),
        "sect":  dict(font=("Ubuntu", 13, "bold")),
        "msg":   dict(font=("Sans", 13, "italic"), pad=(50,0)),
        "grp":   dict(font=("Sans", 12, "italic"), pad=(50,0)),
        "val":   dict(font=("Sans", 11, "italic"), pad=(50,0)),
        "desc":  dict(text_color="gray"),
        "phase": dict(background_color="yellow"),
        "block": dict(background_color="orange"),
        "deny":  dict(background_color="red"),
        "audit": dict(background_color="lightgray"),
        "chain": dict(text_color="magenta"),
        "capture": dict(background_color="darkgray"),
        "severity": dict(background_color="#ffccbb"),
        "pass":  dict(background_color="lightgreen"),
    })

    # flag documentation
    desc = {
        "pass": "No action, not blocking request yet",
        "deny": "Quit request with error 40x",
        "block": "Quit request with error 50x",
        "t:none": "No transformation on input vars",
        "phase:1": "Request header checks",
        "phase:2": "Request body inspection",
        "phase:3": "Response headers",
        "phase:4": "Response body",
        "phase:5": "Logging"
    }
    
    # rule lookup
    r = vhosts.rules[id]  # SecRule
    is_virt = ""
    if type(id) is float:
        is_virt = "(virtual id/chained rule)"
    decl_vh = find_decl_vhost(id)
    is_state = "✅"
    if decl_vh and decl_vh.rulestate.get(id):
        is_state = decl_vh.rulestate[id] + " in rules.conf"  # conditional SecRule declaration
    elif vh and vh.rulestate.get(id):
        is_state = vh.rulestate[id]

    # params 2 widget
    layout = [
        [
            # SecRule #123456
            sg.T(f"SecRule {id}", **style.head),
            # (virtual id)
            sg.T(is_virt, **style.virt),
            #  ➗ ❌  undef=✅
            sg.T(f"state={is_state}", **style.state)
        ],
        [
            # rule comment
            sg.Frame("doc", layout=[[sg.Multiline(r.help(), auto_size_text=1, size=(60,4), background_color="lightgray")]], size=(90,4))
        ],
    ]
    for key in "msg", "vars", "pattern":
        layout.append([sg.T(key, **style.sect), sg.T(wrap(getattr(r, key)), **style.get(key, style.val))])
    for key in "flags", "params", "ctl", "setvar", "tags":
        grp = getattr(r, key)
        if not grp:
            continue
        layout.append([sg.T(key, **style.sect)])
        if type(grp) is list:
            for v in grp:
                layout.append([
                    sg.T(v, **style.grp, **style.get(v,{})),
                    sg.T(desc.get(v,""), **style.desc)
                ])
        elif type(grp) is dict:
            for k,v in grp.items():
                layout.append([
                    sg.T(k, **style.grp),
                    sg.T(v, **style.get(k,{})),
                    sg.T(desc.get(f"{k}:{v}",""), **style.desc)
                ])
    
    # logs
    if log_values and conf.info_log_count:
        layout.append([sg.Frame(title="recent log entries", pad=(10,25),
            layout=[[sg.Multiline(
                default_text="\n----------\n".join(
                    re.grep(fr"\b{id}\b", log_values())[ -conf.info_log_count: ]
                ),
                size=(60,12)
            )]]
        )])

    # print rule also as json?
    #layout.append(  [sg.T(json.dumps(r.__dict__, indent=4))]  )

    # finalize window
    layout = [
        [sg.Menu([["Rule",["Close"]]])],
        [sg.Column(layout, expand_x=1, expand_y=0, size=(675,820), scrollable="vertically", element_justification='left')]
    ]
    return sg.Window(layout=layout, title=f"SecRule #{id}", resizable=1, font="Sans 12", icon=icons.icon)
    # mainwindow chains it to global event poll .win_register()


# look up rule declaration
def find_decl_vhost(id):
    for fn,vh in vhosts.vhosts.items():
        if vh.ruledecl.get(id):
            return vh
