#!/usr/bin/env python
##########################################################
# Copyright (c) 2019 Saltstack Formulas
##########################################################
# encoding: utf-8
# This script displays a formula menu for default profile.
# http://npyscreen.readthedocs.org/introduction.html

try:
    import sys, os, platform, subprocess
except ImportError("Cannot import sys, os, platform, subprocess, modules"):
    exit(100)
try:
    import npyscreen
except ImportError("Cannot import npyscreen"):
    exit(102)

class TestApp(npyscreen.NPSApp, outdir='/srv/salt'):
    def __init__(self):
        self.dir = outdir
        # Set option users will see in the multi select widget
        self.maven = 'Maven'
        self.postgres = 'Postgres'
        self.java = 'Oracle JDK8 / JCE'
        self.tomcat = 'Tomcat7'
        self.apache = 'Apache (after install do not use port 80)'
        self.intellij = 'Intellij IDEA latest'
        self.pycharm = 'Pycharm latest'
        self.eclipse = 'Eclipse IDE latest'
        self.sqlplus = 'SQLPlus recent'
        self.sqldeveloper = 'SQL Developer recent'
        
    def main(self):
        # Create form
        F  = npyscreen.Form(name = "Example Linux Developer profile:",)
        # Create multi select widget on form
        multi_select = F.add(npyscreen.TitleMultiSelect, max_height =-2, value = [], name="Select Components",
                values = [
                          self.maven,
                          self.postgres,
                          self.java,
                          self.tomcat,
                          self.apache,
                          self.intellij,
                          self.pycharm,
                          self.eclipse,
                          self.sqlplus,
                          self.sqldeveloper], scroll_exit=True)
        # Allow users to interact with form
        F.edit()
        self.selection = multi_select.get_selected_objects()
        self.write_top()

    def write_top(self):
        # Map selected options to salt states
        select_list = []
        for item in self.selection:

            if item == self.maven:
                select_list.extend(('maven', 'maven.env'))
            if item == self.postgres:
                select_list.extend(('postgres', 'postgres.server.image'))
            if item == self.java:
                select_list.append('java')
            if item == self.tomcat:
                select_list.extend(
                    ('tomcat', 'tomcat.config', 'tomcat.native', 'tomcat.manager')
                )

            if item == self.apache:
                select_list.extend(
                    (
                        'apache',
                        'apache.config',
                        'apache.certificates',
                        'apache.mod_mpm',
                        'apache.modules',
                        'apache.mod_rewrite',
                        'apache.mod_proxy',
                        'apache.mod_proxy_http',
                        'apache.mod_proxy_fcgi',
                        'apache.mod_wsgi',
                        'apache.mod_actions',
                        'apache.mod_headers',
                        'apache.mod_pagespeed',
                        'apache.mod_perl2',
                        'apache.mod_geoip',
                        'apache.mod_php5',
                        'apache.mod_cgi',
                        'apache.mod_fcgid',
                        'apache.mod_dav_svn',
                        'apache.mod_security',
                        'apache.mod_security.rules',
                        'apache.mod_socache_shmcb',
                        'apache.mod_ssl',
                        'apache.mod_suexec',
                        'apache.mod_vhost_alias',
                        'apache.mod_remoteip',
                        'apache.mod_xsendfile',
                        'apache.own_default_vhost',
                        'apache.no_default_vhost',
                        'apache.vhosts.standard',
                        'apache.manage_security',
                    )
                )

            if item == self.pycharm:
                select_list.extend(('pycharm', 'pycharm.linuxenv', 'pycharm.developer'))
            if item == self.intellij:
                select_list.extend(('intellij', 'intellij.linuxenv', 'intellij.developer'))
            if item == self.eclipse:
                select_list.extend(
                    (
                        'eclipse',
                        'eclipse.linuxenv',
                        'eclipse.developer',
                        'eclipse.plugins',
                    )
                )

            if item == self.sqlplus:
                select_list.extend(('sqlplus', 'sqlplus.linuxenv', 'sqlplus.developer'))
            if item == self.sqldeveloper:
                select_list.extend(
                    (
                        'sqldeveloper',
                        'sqldeveloper.linuxenv',
                        'sqldeveloper.developer',
                    )
                )

        if select_list:
            #Assume users & packages are mandatory
            select_list.insert(0, 'users')
            select_list.insert(0, 'packages')
            try:
                f = open(f'{self.dir}/top.sls', 'w')
                f.write("base:\n")
                f.write("  '*':\n")
                for ele in select_list:
                    f.write("    - %s\n" % ele)
            finally:
                f.close()
        else:
            print("No selection made.")


#### Run the select screen & handle interrupts
if __name__ == "__main__":
    try:
        outdir = str(sys.argv[1]) if len(sys.argv) > 1 else '/srv/salt'
        App = TestApp(outdir)
        App.run()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(12)
        except SystemExit:
            os._exit(12)
