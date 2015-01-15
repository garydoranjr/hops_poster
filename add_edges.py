#!/usr/bin/env python
import os
import numpy as np
from collections import defaultdict
import yaml

from to_tex import IFILE, COLS, COLSKIP, ROWSKIP, START, order_hops

VWIDTH = 1.25
HWIDTH = 1.0
HOPW = COLSKIP - VWIDTH
HOPH = ROWSKIP - HWIDTH

def corner(r, c):
    return (START + c*COLSKIP), (START + r*ROWSKIP)

def islastcol(col): return (col == (COLS - 1))
def islastrow(row): return (row == ((90/COLS) - 1))
    
OFILE = os.path.join('poster', 'edgelist.tex')

FMT = r'\draw [color=yfibred, line width=2pt] %s;'

class EdgeDrawer(object):

    def __init__(self, edges):
        self.edges = edges

        self.vchannels = defaultdict(int)
        self.hchannels = defaultdict(int)
        self.ports = defaultdict(int)

    def get_abstract_path(self, sr, sc, dr, dc):
        path = []
        if sc == dc:
            if islastcol(sc):
                path.append((sr, sc, 'W'))
                path.append((None, sc, 'V'))
                path.append((dr, dc, 'W'))
                self.vchannels[sc] += 1
                self.ports[sr, sc, 'W'] += 1
                self.ports[dr, dc, 'W'] += 1
            else:
                path.append((sr, sc, 'E'))
                path.append((None, sc+1, 'V'))
                path.append((dr, dc, 'E'))
                self.vchannels[sc+1] += 1
                self.ports[sr, sc, 'E'] += 1
                self.ports[dr, dc, 'E'] += 1

        elif sr == dr:
            if islastrow(sr):
                path.append((sr, sc, 'S'))
                path.append((sr, None, 'H'))
                path.append((dr, dc, 'S'))
                self.hchannels[sr] += 1
                self.ports[sr, sc, 'S'] += 1
                self.ports[dr, dc, 'S'] += 1
            else:
                path.append((sr, sc, 'N'))
                path.append((sr+1, None, 'H'))
                path.append((dr, dc, 'N'))
                self.hchannels[sr+1] += 1
                self.ports[sr, sc, 'N'] += 1
                self.ports[dr, dc, 'N'] += 1
        else:
            return None

        return path

    def get_abstract_paths(self):
        return [self.get_abstract_path(sr, sc, dr, dc)
                for (sr, sc), (dr, dc) in self.edges]

    def get_port(self, r, c, s, n):
        x, y = corner(r, c)
        if s == 'N':
            spacing = HOPW / (self.ports[r, c, s] + 1)
            y += HOPH
            x += spacing*(n + 1)
        elif s == 'S':
            spacing = HOPW / (self.ports[r, c, s] + 1)
            x += spacing*(n + 1)
        elif s == 'E':
            spacing = HOPH / (self.ports[r, c, s] + 1)
            x += HOPW
            y += spacing*(n + 1)
        elif s == 'W':
            spacing = HOPH / (self.ports[r, c, s] + 1)
            y += spacing*(n + 1)
        else: raise ValueError('Bad side "%s"' % s)
        return x, y

    def get_v(self, c, n):
        spacing = VWIDTH / (self.vchannels[c] + 1)
        x, _ = corner(0, c)
        x -= spacing*(n + 1)
        return x

    def get_h(self, r, n):
        spacing = HWIDTH / (self.hchannels[r] + 1)
        _, y = corner(r, 0)
        y -= spacing*(n + 1)
        return y

    def get_paths(self):
        vcs = defaultdict(int)
        hcs = defaultdict(int)
        pts = defaultdict(int)

        abpaths = self.get_abstract_paths()
        paths = []

        for abpath in abpaths:
            if abpath is None: continue
            path = []
            last = None
            for r, c, s in abpath:
                if s in 'NESW':
                    x, y = self.get_port(r, c, s, pts[r, c, s])
                    if last == 'V':
                        path[-1][1] = y
                    if last == 'H':
                        path[-1][0] = x
                    path.append([x, y])
                    pts[r, c, s] += 1

                elif s == 'V':
                    x = self.get_v(c, vcs[c])
                    y = path[-1][1]
                    path.append([x, y])
                    path.append([x, None])
                    vcs[c] += 1

                elif s == 'H':
                    y = self.get_h(r, hcs[r])
                    x = path[-1][0]
                    path.append([x, y])
                    path.append([None, y])
                    hcs[r] += 1

                else: raise ValueError('Bad type "%s"', s)

                last = s

            paths.append(path)

        return paths

    def draw_edges(self):
        paths = self.get_paths()
        lines = []
        for path in paths:
            pathstr = ' -- '.join('(%fin, %fin)' % tuple(vertex) for vertex in path)
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
