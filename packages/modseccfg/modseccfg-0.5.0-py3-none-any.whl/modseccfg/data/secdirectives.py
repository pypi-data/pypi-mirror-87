# encoding: utf-8
# api: pluginconf
# type: data
# title: SecEngine directives
# description: options in current *.conf/vhost file
# version: 0.0
# license: ASL
# author: OWASP Core Rule Set contributors
# category: config
# config:
#   { name: secruleengine, type: select, select: "DetectionOnly|On|Off", description: "Enables or disables mod_security at large.", category: apache }
#   { name: secuploaddir, type: str, description: "Storage location for intercepted files/POST payloads.", category: apache }
#   { name: SecRequestBodyAccess, value: On, type: select, select: On|Off, description: }
#   { name: SecRequestBodyLimit, value: 13107200, type: int, description: Maximum POST/PUT payload size. }
#   { name: SecRequestBodyNoFilesLimit, value: 131072, type: int, description: }
#   { name: SecRequestBodyInMemoryLimit, value: 131072, type: int, description: }
#   { name: SecRequestBodyLimitAction, value: Reject, type: str, description: }
#   { name: SecPcreMatchLimit, value: 100000, type: int, description: }
#   { name: SecPcreMatchLimitRecursion, value: 100000, type: int, description: }
#   { name: SecResponseBodyAccess, value: On, type: select, select: On|Off, description: }
#   { name: SecResponseBodyMimeType, value: "text/plain text/html text/xml"
#   { name: SecResponseBodyLimit, value: 524288, type: int, description: }
#   { name: SecResponseBodyLimitAction, value: ProcessPartial, type:select, select:, description:  ------------------ }
#   { name: SecTmpDir, value: "/tmp/", type: str, description: }
#   { name: SecDataDir, value: "/tmp/", type: str, description: }
#   { name: SecAuditEngine, value: RelevantOnly, type: select, select: "RelevantOnly|On|Off", description: }
#   { name: SecAuditLogRelevantStatus, value: "^(?:5|4(?!04))", type: str, description: }
#   { name: SecAuditLogParts, value: ABDEFHIJZ, type: str, description: }
#   { name: SecAuditLogType, value: Serial, type: select, select: Serial|Concurrent, description: .. }
#   { name: SecAuditLogFormat, value: Native, type: select, select: Native|JSON, description: .. }
#   { name: SecAuditLog, value: "/var/log/apache2/modsec_audit.log", type: str, description: "" }
#   { name: secargumentseparator, value: "&", type: str, description: "Ampersand is the standard", help: "Use the most commonly used application/x-www-form-urlencoded parameter separator. There's probably only one application somewhere that uses something else so don't expect to change this value." }
#   { name: seccookieformat, value: 0, type: int, description: "Restrict Cookie:/Set-Cookie: headers", help: "Settle on version 0 (zero) cookies, as that is what most applications use. Using an incorrect cookie version may open your installation to evasion attacks (against the rules that examine named cookies)." }
#   { name: secunicodemapfile, value: "unicode.mapping 20127", type: str, description: "Specify your Unicode Code Point.", help: "This mapping is used by the t:urlDecodeUni transformation function to properly map encoded data to your language. Properly setting these directives helps to reduce false positives and negatives." }
#   { name: secstatusengine, value: On, type: select, select: On|Off, description: "mod_security usage telemetry", help: "Improve the quality of ModSecurity by sharing information about your current ModSecurity version and dependencies versions. The following information will be shared: ModSecurity version, Web Server version, APR version, PCRE version, Lua version, Libxml2 version, Anonymous unique id for host." }
# doc: https://www.feistyduck.com/library/modsecurity-handbook-2ed-free/online/ch03-configuration.html
#
# Represents the settings for the current mod_security
# config file. Notably this shouldn't be used for vhost
# sections, but a local mod_security.conf override.
# Also try to avoid editing the global /etc/apache2/*
# declarations, but have a /www/conf.d/security.conf
# to apply changes with.
#
# This emtpy python script is a lazy way to reuse
# pluginconf.gui.window() again, but for presenting
# Apache directives instead.
#



"""
# -- Rule engine initialization ----------------------------------------------

# Enable ModSecurity, attaching it to every transaction. Use detection
# only to start with, because that minimises the chances of post-installation
# disruption.
#
SecRuleEngine DetectionOnly


# -- Request body handling ---------------------------------------------------

# Allow ModSecurity to access request bodies. If you don't, ModSecurity
# won't be able to see any POST parameters, which opens a large security
# hole for attackers to exploit.
#
SecRequestBodyAccess On



# Maximum request body size we will accept for buffering. If you support
# file uploads then the value given on the first line has to be as large
# as the largest file you are willing to accept. The second value refers
# to the size of data, with files excluded. You want to keep that value as
# low as practical.
#
SecRequestBodyLimit 13107200
SecRequestBodyNoFilesLimit 131072

# Store up to 128 KB of request body data in memory. When the multipart
# parser reaches this limit, it will start using your hard disk for
# storage. That is slow, but unavoidable.
#
SecRequestBodyInMemoryLimit 131072

# What do do if the request body size is above our configured limit.
# Keep in mind that this setting will automatically be set to ProcessPartial
# when SecRuleEngine is set to DetectionOnly mode in order to minimize
# disruptions when initially deploying ModSecurity.
#
SecRequestBodyLimitAction Reject


# By default be strict with what we accept in the multipart/form-data
# request body. If the rule below proves to be too strict for your
# environment consider changing it to detection-only. You are encouraged
# _not_ to remove it altogether.
#

# PCRE Tuning
# We want to avoid a potential RegEx DoS condition
#
SecPcreMatchLimit 100000
SecPcreMatchLimitRecursion 100000



# -- Response body handling --------------------------------------------------

# Allow ModSecurity to access response bodies. 
# You should have this directive enabled in order to identify errors
# and data leakage issues.
# 
# Do keep in mind that enabling this directive does increases both
# memory consumption and response latency.
#
SecResponseBodyAccess On

# Which response MIME types do you want to inspect? You should adjust the
# configuration below to catch documents but avoid static files
# (e.g., images and archives).
#
SecResponseBodyMimeType text/plain text/html text/xml

# Buffer response bodies of up to 512 KB in length.
SecResponseBodyLimit 524288

# What happens when we encounter a response body larger than the configured
# limit? By default, we process what we have and let the rest through.
# That's somewhat less secure, but does not break any legitimate pages.
#
SecResponseBodyLimitAction ProcessPartial


# -- Filesystem configuration ------------------------------------------------

# The location where ModSecurity stores temporary files (for example, when
# it needs to handle a file upload that is larger than the configured limit).
# 
# This default setting is chosen due to all systems have /tmp available however, 
# this is less than ideal. It is recommended that you specify a location that's private.
#
SecTmpDir /tmp/

# The location where ModSecurity will keep its persistent data.  This default setting 
# is chosen due to all systems have /tmp available however, it
# too should be updated to a place that other users can't access.
#
SecDataDir /tmp/


# -- File uploads handling configuration -------------------------------------

# The location where ModSecurity stores intercepted uploaded files. This
# location must be private to ModSecurity. You don't want other users on
# the server to access the files, do you?
#
SecUploadDir /opt/modsecurity/var/upload/

# By default, only keep the files that were determined to be unusual
# in some way (by an external inspection script). For this to work you
# will also need at least one file inspection rule.
#
SecUploadKeepFiles RelevantOnly

# Uploaded files are by default created with permissions that do not allow
# any other user to access them. You may need to relax that if you want to
# interface ModSecurity to an external program (e.g., an anti-virus).
#
SecUploadFileMode 0600


# -- Debug log configuration -------------------------------------------------

# The default debug log configuration is to duplicate the error, warning
# and notice messages from the error log.
#
SecDebugLog /opt/modsecurity/var/log/debug.log
SecDebugLogLevel 3


# -- Audit log configuration -------------------------------------------------

# Log the transactions that are marked by a rule, as well as those that
# trigger a server error (determined by a 5xx or 4xx, excluding 404,  
# level response status codes).
#
SecAuditEngine RelevantOnly
SecAuditLogRelevantStatus "^(?:5|4(?!04))"

# Log everything we know about a transaction.
SecAuditLogParts ABDEFHIJZ

# Use a single file for logging. This is much easier to look at, but
# assumes that you will use the audit log only ocassionally.
#
SecAuditLogType Serial
SecAuditLog /var/log/apache2/modsec_audit.log

# Specify the path for concurrent audit logging.
SecAuditLogStorageDir /opt/modsecurity/var/audit/


# -- Miscellaneous -----------------------------------------------------------

# Use the most commonly used application/x-www-form-urlencoded parameter
# separator. There's probably only one application somewhere that uses
# something else so don't expect to change this value.
#
SecArgumentSeparator &

# Settle on version 0 (zero) cookies, as that is what most applications
# use. Using an incorrect cookie version may open your installation to
# evasion attacks (against the rules that examine named cookies).
#
SecCookieFormat 0

# Specify your Unicode Code Point.
# This mapping is used by the t:urlDecodeUni transformation function
# to properly map encoded data to your language. Properly setting
# these directives helps to reduce false positives and negatives.
#
SecUnicodeMapFile unicode.mapping 20127

# Improve the quality of ModSecurity by sharing information about your
# current ModSecurity version and dependencies versions.
# The following information will be shared: ModSecurity version,
# Web Server version, APR version, PCRE version, Lua version, Libxml2
# version, Anonymous unique id for host.
SecStatusEngine On

"""
