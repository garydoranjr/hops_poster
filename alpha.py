#!/usr/bin/env python
import yaml
import numpy as np
import pylab as pl

if __name__ == '__main__':
    with open('hops.yaml', 'r+') as f:
        hops = yaml.load(f.read())

    hops = sorted(hops, key=lambda h: h['name'])

    alphas = [np.average(hop['alpha']) for hop in hops]

    pl.plot(np.arange(len(hops)), alphas, 'ko')

    pl.show()
