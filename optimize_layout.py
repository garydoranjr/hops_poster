#!/usr/bin/env python
import os
import numpy as np
import random
import yaml
from itertools import count, combinations

from to_tex import IFILE, COLS
from add_edges import EdgeDrawer

OFILE = 'bestperm.txt'

def obj(hops, perm):
    hops = [hops[p] for p in perm]

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

    return drawer.sum_edges()

def saveperm(perm):
    with open(OFILE, 'w+') as f:
        f.write('\n'.join(map(str, perm)))

def loadperm():
    if os.path.exists(OFILE):
        with open(OFILE, 'r+') as f:
            return [int(l.strip()) for l in f]
    else:
        return None

def optimize(hops, perm):
    pairs = list(combinations(xrange(len(hops)), 2))
    o = obj(hops, perm)
    for i in count(1):
        print 'Iteration %d, Obj: %f' % (i, o)
        changed = False
        random.shuffle(pairs)
        for u, v in pairs:
            newperm = list(perm)
            newperm[u], newperm[v] = newperm[v], newperm[u]
            newo = obj(hops, newperm)
            if newo < o:
                changed = True
                perm = newperm
                o = newo
        if not changed: break
    print 'Optimal solution found: %f' % o
    return perm, o

def main():
    with open(IFILE, 'r+') as f:
        hops = yaml.load(f.read())

    best_perm = loadperm()
    if best_perm is None:
        best_perm = range(len(hops))
    best_obj = obj(hops, best_perm)

    while True:
        print 'Optimizing (best: %f)' % best_obj
        seed = np.random.permutation(len(hops))
        pstar, ostar = optimize(hops, seed)
        if ostar < best_obj:
            best_perm = pstar
            best_obj = ostar
            saveperm(best_perm)

if __name__ == '__main__':
    main()
