#!/usr/bin/env python
import os
import numpy as np
from collections import defaultdict
import yaml

from to_tex import IFILE, COLS, COLSKIP, ROWSKIP, START, order_hops
    
OFILE = os.path.join('poster', 'edgelist.tex')

FMT = r'\draw [color=yfibred, line width=2pt] %s;'

class EdgeDrawer(object):

    def __init__(self, edges):
        self.edges = edges

    def get_paths(self):
        paths = []
        for (sr, sc), (dr, dc) in self.edges:
            #print '(%d, %d) -- (%d, %d)' % (sr, sc, dr, dc)
            sx, sy = (START + sc*COLSKIP), (START + sr*ROWSKIP)
            dx, dy = (START + dc*COLSKIP), (START + dr*ROWSKIP)
            paths.append([(sx, sy), (dx, dy)])
        return paths

    def draw_edges(self):
        paths = self.get_paths()
        lines = []
        for path in paths:
            pathstr = ' -- '.join('(%fin, %fin)' % vertex for vertex in path)
            line = (FMT % pathstr)
            lines.append(line)

        return '\n'.join(lines)

def main():
    with open(IFILE, 'r+') as f:
        hops = yaml.load(f.read())

    hops = order_hops(hops)

    mapping = {}

    edges = set()

    for h, hop in enumerate(hops):
        col = h % COLS
        row = h / COLS
        source = hop['name']
        mapping[source] = (row, col)
        for dest in hop['substitutes']:
            edges.add(frozenset([source, dest]))

    edges = [sorted(mapping[node] for node in edge) for edge in edges]
    drawer = EdgeDrawer(edges)

    with open(OFILE, 'wb+') as f:
        f.write(drawer.draw_edges())

if __name__ == '__main__':
    main()
