#!/usr/bin/env python
from collections import defaultdict
import yaml

IFILE = 'hops.yaml'
OFILE = 'hops.gv'
TO_REPLACE = [" .'"]

def main():
    with open(IFILE, 'r+') as f:
        hops = yaml.load(f.read())

    lines = ['digraph G {']

    for hop in hops:
        name = hop['name']
        for sub in hop['substitutes']:
            lines.append('  "%s" -> "%s";' % (name, sub))

    lines.append('}')

    with open(OFILE, 'wb+') as f:
        f.write('\n'.join(lines))

if __name__ == '__main__':
    main()
