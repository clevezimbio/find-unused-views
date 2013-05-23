#!/usr/bin/python
"""
A simple (and pretty naive) utility to find unused views within a Django
project. It looks for functions which resemble views in files named views.py,
and for each one it finds it checks to see if it can find it mentioned in
and urls.py.

This can stupendously and hilariously fail in any number of ways and should
probably not be run by anyone ever.

ack-grep is required. Must be run in a *nix environment.

Usage:
python find_unused_views.py /path/to/project
"""
import subprocess
import sys

find_view_cmd = 'ack-grep --py "def " %s | grep \'(request\''
url_contents_cmd = 'find %s -name "urls.py"'

def find_unused_views(target_dir):
    url_contents = get_url_contents(target_dir)
    for view_path, view_name in find_views(target_dir):
        if 'views.py' not in view_path:
            continue
        if view_name not in url_contents:
            print view_path + ':' + view_name

def get_url_contents(target_dir):
    cmd = url_contents_cmd % target_dir
    output = subprocess.check_output(cmd, shell=True).strip()
    contents = ''
    for filename in output.split('\n'):
        f = open(filename)
        contents += f.read()
        f.close()
    return contents

def find_views(target_dir):
    cmd = find_view_cmd % target_dir
    output = subprocess.check_output(cmd, shell=True)
    lines = output.strip().split('\n')
    views = [(l.split(':')[0], l.split(':')[2].split(' ')[1].split('(')[0])
        for l in lines]
    return views

def main():
    try:
        target_dir = sys.argv[1]
    except IndexError:
        print >> sys.stderr, 'Please specify a directory'
    else:
        find_unused_views(target_dir)

if __name__ == '__main__':
    main()
