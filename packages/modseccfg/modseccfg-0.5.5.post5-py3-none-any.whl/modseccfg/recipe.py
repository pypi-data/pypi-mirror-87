# api: modseccfg
# encoding: utf-8
# version: 0.3
# type: data
# title: recipe
# description: Apache/mod_security config examples or conversions
# category: config
# config:
#    { name: replace_rules, type: bool, value: 0, description: "try to find replacement spot, else just append" }
# license: Apache-2.0
#
# Basically just blobs of text and an editor window.
# [Save] will append directives to selected vhost/*.conf file.
#
# Some samples from:
#  · https://wiki.atomicorp.com/wiki/index.php/Mod_security
#


from modseccfg import utils, vhosts, writer
import PySimpleGUI as sg
import re, random
from textwrap import dedent



class templates:

    locationmatch = """
        <Location "/app/">
          SecRuleRemoveById $id   # $msg
          # SecRuleEngine DetectionOnly
        </Location>
    """

    directory = """
        <Directory "/srv/www/app/">
          SecRuleRemoveById $id   # $msg
        </Directory>
    """

    filesmatch = """
        <FilesMatch "\.php$">
          SecRuleRemoveById $id   # $msg
        </FilesMatch>
    """
    
    exclude_parameter = """
        # Exclude GET/POST parameter from rule
        #
        SecRuleUpdateTargetByID $id "!ARGS:param"
    """
    
    rule_to_detectiononly = """
        # One rule to DetectionOnly
        #
        SecRuleUpdateActionById $id "pass,status:200,log,auditlog"
    """

    url_to_detectiononly = """
        # Set one URL to DetectionOnly
        #
        SecRule REQUEST_URI "$request_uri" "phase:1,id:$rand,t:none,t:lowercase,pass,msg:'DetectionOnly for $request_uri',ctl:ruleEngine=DetectionOnly"
    """
    
    exempt_remote_addr = """
        # Exempt client addr from all SecRules
        #
        SecRule REMOTE_ADDR "@streq $remote_addr" "phase:1,id:$rand,t:none,nolog,allow,ctl:ruleEngine=Off,ctl:auditEngine=Off"
    """

    whitelist_ip_file = """
        # List of IPs from filename trigger DetectionOnly mode
        #
        SecRule REMOTE_ADDR "@pmFromFile $confn.whitelist" "phase:1,id:$rand,t:none,nolog,allow,ctl:ruleEngine=DetectionOnly"
    """
    
    ip2location = """
        # Use mod_ip2location or Cloudflare header
        #
        SetEnvIfExpr "req('CF-IPCountry') =~ '\w\w'" IP2LOCATION_COUNTRY_SHORT=%{HTTP_CF_IPCOUNTRY}
        SecRule ENV:IP2LOCATION_COUNTRY_SHORT "!^(UK|DE|FR)$" "id:$rand,deny,status:500,msg:'Req not from whitelisted country'"
    """
    
    macros = """
        # This directive block defines some macros, which you can use to simplify a few
        # SecRules exceptions. Best applied to a central *.conf file, rather than vhosts.
        # An `Use` directive/prefix is necessary to expand these macros.
        #     ↓
        #    Use SecRuleRemoveByPath 900410 /app/exempt/
        #
        <IfModule mod_macro.c>

          <Macro NEWID $STR>
            # define %{ENV:NEWID} in the 50000 range; might yield duplicates
            SetEnvIfExpr "md5('$STR') =~ /(\d).*(\d).*(\d).*(\d)/" "NEWID=5$1$2$3$4"
          </Macro>

          <Macro SecRuleRemoveByPath $ID $PATH>
            Use NEWID "$ID$PATH"
            SecRule REQUEST_URI "@eq $PATH" "id:%{ENV:NEWID},t:none,msg:'Whitelist «$PATH»',ctl:removeById=$ID"
          </Macro>

        </IfModule>
    """
    
    apache_cloudflare_remoteip = """
        # Sets REMOTE_ADDR for Apache at large per mod_remoteip.
        # @url https://support.cloudflare.com/hc/en-us/articles/360029696071-Orig-IPs
        #
        <IfModule mod_remoteip.c>
           RemoteIPHeader CF-Connecting-IP
           RemoteIPTrustedProxy 173.245.48.0/20
           RemoteIPTrustedProxy 103.21.244.0/22
           RemoteIPTrustedProxy 103.22.200.0/22
           RemoteIPTrustedProxy 103.31.4.0/22
           RemoteIPTrustedProxy 141.101.64.0/18
           RemoteIPTrustedProxy 108.162.192.0/18
           RemoteIPTrustedProxy 190.93.240.0/20
           RemoteIPTrustedProxy 188.114.96.0/20
           RemoteIPTrustedProxy 197.234.240.0/22
           RemoteIPTrustedProxy 198.41.128.0/17
           RemoteIPTrustedProxy 162.158.0.0/15
           RemoteIPTrustedProxy 104.16.0.0/12
           RemoteIPTrustedProxy 172.64.0.0/13
           RemoteIPTrustedProxy 131.0.72.0/22
           RemoteIPTrustedProxy 2400:cb00::/32
           RemoteIPTrustedProxy 2606:4700::/32
           RemoteIPTrustedProxy 2803:f800::/32
           RemoteIPTrustedProxy 2405:b500::/32
           RemoteIPTrustedProxy 2405:8100::/32
           RemoteIPTrustedProxy 2a06:98c0::/29
           RemoteIPTrustedProxy 2c0f:f248::/32
        </IfModule>

        # Fallback alternative for CRS/mod_security, apply same remote_addr check,
        # but update only CRSs tx.real_ip and remote_addr internally. Not sure
        # if this will yield correct audit log entries.
        #
        <IfModule mod_security.c>
           # Test if remote_addr matches Cloudflare IPs
           #
           SecRule REMOTE_ADDR "@ipMatch 173.245.48.0/20,103.21.244.0/22,103.22.200.0/22,103.31.4.0/22,141.101.64.0/18,108.162.192.0/18,190.93.240.0/20,188.114.96.0/20,197.234.240.0/22,198.41.128.0/17,162.158.0.0/15,104.16.0.0/12,172.64.0.0/13,131.0.72.0/22,2400:cb00::/32,2606:4700::/32,2803:f800::/32,2405:b500::/32,2405:8100::/32,2a06:98c0::/29,2c0f:f248::/32" \
               "id:7030,t:none,pass,setvar:TX.IS_CLOUDFLARE=1,setvar:TX.IS_CDN=1,msg:'Cloudflare CDN'"

           # Update TX.REAL.IP + REMOTE_ADDR from CF-Connecting-IP:
           #
           SecRule TX.IS_CLOUDFLARE "@eq 1" "id:7031,t:none,chain,pass,msg:'Set TX.REAL_IP from Cloudflare CF-Connecting-IP'"
           SecRule REQUEST_HEADERS:cf-connecting-ip "@rx ^[\d\.:a-f]+$" "pass,t:none,capture,setvar:'TX.REAL_IP=%{TX:0}',setvar:'REMOTE_ADDR=%{TX:0}',setenv:'REMOTE_ADDR=%{TX:0}',logdata:'TX.REAL_IP=%{TX:0} set from Cloudflare CDN header'"
        </IfModule>
    """
     
    apache_errorlog_format = """
        # Extend error log w/ REQUEST_URI and somewhat standard datetime format (not quite 8601)
        #
        #  → Feedback appreciated. What ought to be the post-90s Apache default?
        #
        SetEnvIf Request_URI "(^.*$)" REQ=$1
        ErrorLogFormat "[%{cu}t] [%m:%l] [pid %P:tid %T] [client %a] %E: %M [request_uri %{REQ}e]"
        
        # "extended" log format
        # @url https://github.com/Apache-Labor/labor/tree/master/labor-04
        #
        LogFormat "%h %{GEOIP_COUNTRY_CODE}e %u [%{%Y-%m-%d %H:%M:%S}t.%{usec_frac}t] \"%r\" %>s %b \
\"%{Referer}i\" \"%{User-Agent}i\" \"%{Content-Type}i\" %{remote}p %v %A %p %R \
%{BALANCER_WORKER_ROUTE}e %X \"%{cookie}n\" %{UNIQUE_ID}e %{SSL_PROTOCOL}x %{SSL_CIPHER}x \
%I %O %{ratio}n%% %D %{ModSecTimeIn}e %{ApplicationTime}e %{ModSecTimeOut}e \
%{ModSecAnomalyScoreInPLs}e %{ModSecAnomalyScoreOutPLs}e \
%{ModSecAnomalyScoreIn}e %{ModSecAnomalyScoreOut}e" extended
    """
    
    crs_preconfig = """
        # --
        # This should be appended to /etc/modsecurity/crs/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS
        #
        #  · SecRuleDisableById can go directly into vhosts
        #  · But recipes and CRS options better reside in 900-EXCLUSION or a *.preconf file
        #  · vhost.*.preconf files should declare a <Directory> to limit changes in their DocumentRoot
        
        # e.g. Debian
        IncludeOptional /etc/apache2/sites-enabled/*.preconf

        # or vhost-adjacent config
        #IncludeOptional /www/conf.d/vhost.*.preconf
    """
    
    preconf_stub = """
        # type: config
        # sort: pre-crs
        # class: apache
        # title: {ServerName}
        # description: early mod_security configuration
        #
        # For SecRule directives that should override CRS rules, or using modseccfg macros etc.
        # SecRuleDisableById settings belong into regular vhost.conf still.
        # (Still not sure about CRS variable overrides.)
        
        <Directory {DocumentRoot}>
           # Use SecRuleRemobeByPath 900130 /app/
           
        </Directory>
    """


def ls():
    return [title.replace("_", " ").title() for title in templates.__dict__.keys() if not title.startswith("__")]

# inject recipe list to main menu
def add_menu(menu):
    menu[2].append(ls())
   

def has(name):
    return hasattr(templates, name.lower().replace(" ", "_"))

def show(name="", data={}, mainwindow=None, **kwargs):

    # extract infos from main UI (id and log elements)
    vars = bag(data)
    name = name.lower().replace(" ", "_")
    text = getattr(templates, name)
    if type(text) is str:
        text = dedent(text).lstrip()
        text = repl(text, vars)
    else:
        text = text(data, vars)
    #print(data)
    #print(text)
    
    # create and dispatch to main event loop
    w = win(name, data["confn"], text)
    mainwindow.win_register(w.w, w.event)


# window
class win:
    def __init__(self, name, fn, text):
        self.w = sg.Window(title=f"Recipe '{name}'", resizable=1, layout=[
            [sg.Multiline(default_text=text, key="src", size=(90,24), font="Mono 12")],
            [sg.Button(f"Save to {fn}", key="save"), sg.Button("Cancel", key="cancel")]
        ])
        self.fn = fn

   # write …
    def event(self, event, data):
        #print(data)
        if event == "save":
            text = data["src"]
            writer.append(fn=self.fn, directive=text, value="", comment="")
        self.w.close()


# prepare vars dict from mainwindow event data + selected log line
def bag(data):
    vars = {
        "id": "0",
        "rand": random.randrange(2000,5000),
        "request_uri": "/PATH",
        "confn": data.get("confn")
    }
    if data.get("log"):
        for k,v in re.findall('\[(\w+) "([^"]+)"\]', str(data["log"])):
            if k in ("uri", "request_line",): k = "request_uri"
            if k in ("request_uri",): v = re.escape(v)
            vars[k] = v
    if data.get("rule"):
        vars["id"] = data["rule"][0]
    return vars

# substitute $varnames in text string
def repl(text, vars):
    text = re.sub(r"\$(\w+)", lambda m,*k: str(vars.get(m.group(1), m.group(0))), text)
    return text

