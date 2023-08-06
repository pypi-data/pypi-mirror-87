__all__ = ['sanitize', 'jsfiddle_url']


import github_gist
import github_name
import os
import re

"""
repo:
https://jsfiddle.net/gh/get/library/pure/{github_tree}/
https://jsfiddle.net/gh/get/library/pure/owner/repo/tree/master/relpath/

gist:
http://jsfiddle.net/gh/gist/library/pure/{id}/
"""


def sanitize(path, replacement="_"):
    """return a sanitized path supported by jsfiddle.net"""
    if replacement is None:
        replacement = "_"
    return re.sub('[^!@#$&*()\'?\\/_\-0-9a-zA-Z]+', replacement, path)


def git_root():
    path = os.getcwd()
    while path and len(path) > 1:
        if os.path.exists(os.path.join(path, ".git")):
            return path
        path = os.path.dirname(path)


def github_tree():
    """return `github_tree` string for a current directory. git remote required"""
    fullname = github_name.get()
    if not fullname:
        return ""
    relpath = os.path.relpath(os.getcwd(), git_root())
    return "/".join([fullname, "tree/master", relpath])


def jsfiddle_url():
    """return jsfiddle url for a current directory. git remote required"""
    _github_tree = github_tree()
    if not _github_tree:
        return ""
    gist_id = github_gist.getid()
    if gist_id:
        return "http://jsfiddle.net/gh/gist/library/pure/%s/" % gist_id
    return "https://jsfiddle.net/gh/get/library/pure/%s/" % github_tree()
