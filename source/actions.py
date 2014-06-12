#!/usr/bin/python
# encoding: utf-8
from __future__ import unicode_literals

import sys
import urllib
import os.path
import subprocess

import workflow
import ccl_bplist

HOME = os.path.expanduser("~")
BIB_DIR = HOME + "/Library/Caches/Metadata/edu.ucsd.cs.mmccrack.bibdesk/"

################################################
# AppleScript Functions
################################################

def _applescriptify_str(text):
    """Replace double quotes in text for Applescript string"""
    text = text.replace('"', '" & quote & "')
    text = text.replace('\\', '\\\\')
    return text

def _applescriptify_list(_list):
    """Convert Python list to Applescript list"""
    quoted_list = []
    for item in _list:
        if type(item) is unicode:   # unicode string to AS string
            _new = '"' + item + '"'
            quoted_list.append(_new)    
        elif type(item) is str:     # string to AS string
            _new = '"' + item + '"'
            quoted_list.append(_new)    
        elif type(item) is int:     # int to AS number
            _new = str(item)
            quoted_list.append(_new)
        elif type(item) is bool:    # bool to AS Boolean
            _new = str(item).lower()
            quoted_list.append(_new)
    quoted_str = ', '.join(quoted_list)
    return '{' + quoted_str + '}'

def as_run(ascript):
    """Run the given AppleScript and return the standard output and error."""
    osa = subprocess.Popen(['osascript', '-'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    return osa.communicate(ascript)[0].strip()

def set_clipboard(data):
    """Set clipboard to ``data``""" 
    scpt = """
        set the clipboard to "{0}"
    """.format(_applescriptify_str(data))
    subprocess.call(['osascript', '-e', scpt])

################################################
# Helper Function
################################################

def read_cachedir():
    """Read BibDesk cache dir into Python array"""
    _data = []
    for bib in os.listdir(BIB_DIR):
        bib_path = os.path.join(BIB_DIR, bib)
        with open(bib_path, 'rb') as _file:
            bib_data = ccl_bplist.load(_file)
            _file.close()
        _data.append(bib_data)
    return _data

################################################
# Actions
################################################   

def export_cite_command(cite_key):
    """Return LaTeX cite command"""
    cmd = "\\cite{{{0}}}".format(cite_key)
    set_clipboard(cmd)
    return "Cite Command"

def open_attachment(cite_key):
    """Open PDF attachment in default app"""
    data = read_cachedir()
    sources = [x['kMDItemWhereFroms']
                for x in data
                if x['net_sourceforge_bibdesk_citekey'] == cite_key]
    for _val in sources:
        if _val != []:
            for source in _val:
                if 'pdf' in source:
                    if not 'http' in source:
                        clean_file = urllib.unquote(source)
                        _file = clean_file.replace('file://localhost', '')
                        if os.path.isfile(_file):
                            subprocess.Popen(
                                ['open', _file], 
                                shell=False, 
                                stdout=subprocess.PIPE)

def open_item(cite_key):
    """Open item in BibDesk"""
    scpt = """
        if application id "edu.ucsd.cs.mmccrack.bibdesk" is not running then
            tell application id "edu.ucsd.cs.mmccrack.bibdesk"
                launch
                delay 0.3
                activate
                delay 0.3
                open location "x-bdsk://" & "{0}"
            end tell
        else
            tell application id "edu.ucsd.cs.mmccrack.bibdesk"
                activate
                delay 0.3
                open location "x-bdsk://" & "{0}"
            end tell
        end if
    """.format(cite_key)
    as_run(scpt)

def save_group(group, wf):
    """Save Group name to tmp file"""
    with open(wf.cachefile("group_result.txt"), 'w') as _file:
        _file.write(group.encode('utf-8'))
        _file.close()

def save_keyword(keyword, wf):
    """Save Keyword name to tmp file"""
    with open(wf.cachefile("keyword_result.txt"), 'w') as _file:
        _file.write(keyword.encode('utf-8'))
        _file.close()

def act(cite_key, action, wf):
    """Main API method"""
    if action == 'open':
        open_item(cite_key)
    elif action == 'cite':
        return export_cite_command(cite_key)
    elif action == 'att':
        open_attachment(cite_key)
    elif action == 'save_group':
        save_group(cite_key, wf)
    elif action == 'save_keyword':
        save_keyword(cite_key, wf)
    
    #elif action == 'ref':
    #    return export_ref()
    #elif action == 'cite_group':
    #    return export_group()
    #elif action == 'append':
    #    return append_to_bib()
    #elif action == 'bib':
    #    return read_save_bib()

################################################
# Main Function
################################################

def main(wf):
    #cite_key = "Allen_1938a_On-the-Friendship-of-Lucretius-with"
    #action = "cite"
    cite_key = wf.args[0]
    action = wf.args[1]

    print act(cite_key, action, wf)


if __name__ == '__main__':
    wf = workflow.Workflow()
    sys.exit(wf.run(main))  
