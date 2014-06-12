# encoding: utf-8
import subprocess
import os.path

HOME = os.path.expanduser("~")
BIB_DIR = HOME + "/Library/Caches/Metadata/edu.ucsd.cs.mmccrack.bibdesk/"
BIB_QU = "{key} == '*{query}*'cd" # fuzzy, ignore case and diacritics
QUERY_KEYS = [
    "net_sourceforge_bibdesk_citekey",
    "kMDItemTitle",
    "net_sourceforge_bibdesk_container",
    "kMDItemEditors",
    "kMDItemAuthors",
    "kMDItemKeywords",
    "net_sourceforge_bibdesk_publicationdate"
    ]

################################################
# `mdfind` query
################################################

def _find(_query):
    """Wrapper for `mdfind`"""
    __query = "mdfind {0}".format(_query)
    _output = subprocess.check_output(__query, shell=True)
    _res = _output.split("\n")
    if _res[-1] == "":
        _res = _res[:-1]
    return _res

def query(_queries):
    """Search for items in BibDesk cache"""
    if os.path.exists(BIB_DIR):
        # Ensure search is only in and for BibDesk cache 
        query_base = "-onlyin \"{0}\"".format(BIB_DIR) + \
            " \"(kMDItemContentType == net.sourceforge.bibdesk.bdskcache) && "
        query_lst = []
        for _qu in _queries.split():
            # Build the fuzzy queries
            bib_query = [BIB_QU.format(
                    key=_key,
                    query=_qu)
                    for _key in QUERY_KEYS]
            bib_query = ' || '.join(bib_query)
            bib_query = '(' + bib_query + ')'
            query_lst.append(bib_query)
        
        query_body = ' && '.join(query_lst)
        # Create the final `mdfind` query
        final_query = query_base + query_body + '"'
        return _find(final_query)
