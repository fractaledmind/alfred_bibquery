#!/usr/bin/python
# encoding: utf-8
import re
import plistlib
import os.path
import ccl_bplist

HOME = os.path.expanduser("~")
BIB_DIR = HOME + "/Library/Caches/Metadata/edu.ucsd.cs.mmccrack.bibdesk/"

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


def main():
    print "hello"

if __name__ == '__main__':
    main()
