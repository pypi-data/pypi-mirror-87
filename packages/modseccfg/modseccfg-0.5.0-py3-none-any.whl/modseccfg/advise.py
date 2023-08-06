# encoding: utf-8
# api: modseccfg
# version: 0.3
# type: data
# category: log
# title: log advise
# description: Some simple pattern detection for common log entries
# license: Apache-2.0
#
# Basically just some keyword lookups to explain the logs.
# Now that's fun, because herein we pattern-match the mod_security
# logs for potential problems.
#
# Doesn't really make sense yet. Requires way more advisory links
# like for the PCRE backtracking or other common issues.
#


from modseccfg import utils, vhosts
import PySimpleGUI as sg
import re, random, textwrap, os



patterns = {

    "PCRE limits": """Backtracking limits for regex patterns can usually be
    raised.  500000 (500K) is still reasonable for sites not under concrete
    DoS threats.  See →File→SecOptions for SecPcreMatchLimit &
    SecPcreMatchLimitRecursion 500000
    https://stackoverflow.com/questions/18226521/modsecurity-maximum-post-limits-pcre-limit-errors""",

    "tx\.allowed_request_content_type": """Might need adaption if you use any
    REST toolkit with uncommon MIME type uploads (e.g. a DAV or VCS).
    See →File→CRS options to change this variable for allowed POST payloads.""",

    "TX:anomaly_score": """Anomaly scoring mode is enabled.
    'TX:anomaly_score' denotes a transaction variable, used as counter for
    threat indicators. (Concrete causes should be noted in previous log entries.)
    https://www.modsecurity.org/CRS/Documentation/anomaly.html""",
    
    "TX:outgoing_points": """Comodo rules: total score for suspicious output.""",
    
    "(?i)CRITICAL": """Highest severity level. Though that doesn't mean it's
    a reliable match.""",
    
    "Operator GE": """'Greater or equal' comparison, of one tx:variable with
    a number probably. (Causes should be listed in previous log entries.)""",
    
    "TX:inbound_anomaly_score": """Anomaly scoring mode; counter for issues
    with incoming request data (rather than leaked code/sql/xss etc.) """,

    "Matched Phrase": """Static string match. Definitions usually reside in
    a text file (*.data) alongside the rules
    file:///usr/share/modsecurity-crs/rules/""",
    
    "libinjection.+Matched Data: \S+ found within": """libinjection frequently
    trips over two-letter strings. In such cases it might be useful to exempt
    a parameter instead of disabling the whole rule.
    Use e.g. `SecRuleUpdateTargetById 123456 "!ARGS:param"` per [Modify]→[Target].
    https://github.com/client9/libinjection/issues/145
    """,
    
    'status "429"': """HTTP error 429 == Too many requests. Error code often
    substititung for 400/Forbidden to deter bots.""",

    "wlwmanifest.xml": """Windows Live Writer remnant. For some reason an
    exploit vector on Wordpress (as usual).""",

    "/\.env": """Password crawlers love to look for .env files. Blame GitHub.""",

    "Found another rule with the same id": """Usually indicates that a rule
    file got included twice. Check `apache2ctl -t -D DUMP_INCLUDES` to see if
    there's an Include(Optional) ../* loop.
    https://stackoverflow.com/questions/53082316/apache-modsecurity-another-rule-with-the-same-id-error
    """,    
    "another rule with the same id": """And also, don't redefine rules
    "SecRuleRemove" does not really remove, but disable an existing rule.
    To fully override a condition, it needs to be redeclared with a new id:num.
    Send a bug report if it was caused by modseccfg.
    """,
    
    "SecCollectionTimeout is not yet supported": """mod_security v3 problem.
    https://stackoverflow.com/questions/49286483/seccollectiontimeout-is-not-yet-supported
    """,
    
    "Execution phases can only be specified by chain starter rules": """
    phase:123 can only be noted in the first rule, not in chained SecRule conditions
    https://stackoverflow.com/questions/43663373/modsecurity-execution-phases-can-only-be
    """,
    
    "Previous Block Reason": """One of harvester, spammer, search engine IP,
    high risk countries, or clients that previously violated rules. The %{ip.reput_block_reason}
    and %{ip.reput_block_flag} variables are global collections (dbm file in SecDataDir)
    """,
    
    """-x-m-add-""": """
    logdata:'Matched Data: %{TX.0} found within %{MATCHED_VAR_NAME}: %{MATCHED_VAR}',\
    logdata:'Restricted header detected: %{MATCHED_VAR}',\
    logdata:'Matched Data: XSS data found within %{MATCHED_VAR_NAME}: %{MATCHED_VAR}',\
    logdata:'Matched Data: Suspicious payload found within %{MATCHED_VAR_NAME}: %{MATCHED_VAR}',\
    logdata:'Matched Data: Suspicious JS global variable found within %{MATCHED_VAR_NAME}: %{MATCHED_VAR}',\
    logdata:'Matched Data: Suspicious payload found within %{MATCHED_VAR_NAME}: %{MATCHED_VAR}',\
    logdata:'Matched Data: %{TX.0} found within %{MATCHED_VAR_NAME}: %{MATCHED_VAR}',\
    logdata:'Previous Block Reason: %{ip.reput_block_reason}',\
    logdata:'Matched Data: %{TX.0} found within %{MATCHED_VAR_NAME}: %{MATCHED_VAR}',\
    """,
}



rx_url = "https?://\S+|file:///\S+"

# restrict text width
def wrap(text, width=76):
    text = re.sub("\s+", " ", text)
    return "\n".join(textwrap.wrap(text, width))

# callback for window events
def show_url(event):
    if re.match(rx_url, event):
        os.system(f"xdg-open '{event}' &")

# extract urls from text
def split_text_links(text):
    links = re.findall(rx_url, text)
    if links:
        text = re.sub(rx_url, "", text)
    return text, links
    

# scan patterns, show window
def show(mainwindow, data):
    if not data.get("log"):
        return
    log = data["log"]
    
    # look if anything matcheed
    found = {}
    for rx, text in patterns.items():
        m = re.search(rx, log[0], re.I)
        if m:
            found[m.group(0)] = text
    if not found:
        return mainwindow.status("No known log entry.")

    # prepare output
    layout = [[sg.T("Detected log messages", font=("Sans",16,"bold"), pad=(0,5,0,15), text_color="darkgray")]]
    for title, text in found.items():
        text, links = split_text_links(text)
        layout.append([sg.T(title, font=("Ubuntu",12,"bold italic"), pad=(0,10))])
        layout.append([sg.T(wrap(text), pad=(10,2))])
        for url in links:
            layout.append([sg.Button(url, pad=(10,0), font=("Noto Sans Display", 11), use_ttk_buttons=1)])
    layout.append([sg.Button("  Close  ", pad=(10,30,10,5))])

    # show + let main handle button
    w = sg.Window(title="Log patterns", layout=layout, size=(700,500), font="Sans 12")
    mainwindow.win_register(
        w, lambda ev,*d: show_url(ev) or w.close()
    )

