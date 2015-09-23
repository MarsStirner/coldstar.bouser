# -*- coding: utf-8 -*-
import sys
import subprocess

import dialog

__author__ = 'viruzzz-kun'


d = dialog.Dialog(dialog="dialog")

button_names = {d.OK:     "OK",
                d.CANCEL: "Cancel",
                d.HELP:   "Help",
                d.EXTRA:  "Extra"}

while 1:
    code, tag = d.menu(
        "What do we gonna do?",
        choices=[
            ("Bouser",  "Install Bouser"),
            ("CyMySql", "Install CyMySql"),
            ("Config",  "Configure Coldstar")],
        )

    if code in (d.ESC, d.CANCEL):
        sys.exit(0)
    elif tag == "Bouser":
        subproc = subprocess.Popen(
            ['pip', 'install', '-r', 'requirements.txt', '--upgrade'],
            executable='pip',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        d.progressbox(
            fd=subproc.stdout.fileno(),
            text='installing requirements',
            width=156,
            height=40,
        )
    elif tag == 'CyMySql':
        subproc = subprocess.Popen(
            ['pip', 'install', 'cython', 'cymysql', '--upgrade'],
            executable='pip',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        d.progressbox(
            fd=subproc.stdout.fileno(),
            text='installing requirements',
            width=156,
            height=40,
        )
    elif tag == 'Config':
        checklist = [
            ('SS', 'Separate Simargl', False)
        ]
        d.checklist(
            'Checks',
            choices=checklist,
            width=156,
            height=40,
        )

d.infobox("Bye bye...", width=0, height=0, title="This is the end")
