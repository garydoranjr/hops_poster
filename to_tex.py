#!/usr/bin/env python
import os
import numpy as np
from collections import defaultdict
import yaml
    
#\hop{10}{10}{Admiral}{11--15\%}{Said to be citrusy, orange flavored. A good compliment hop to Targets. Good dual purpose hop.}{English IPAs, Ales}{All Purpose}{UK, US}

IFILE = 'hops.yaml'
OFILE = os.path.join('poster', 'hoplist.tex')
PERMFILE = 'bestperm.txt'

COLS = 10
COLSKIP = 4.5
ROWSKIP = 3
START = 1.5

FMT = r'\hop{%.1f}{%.1f}{%s}{%s}{%s}{%s}{%s}{%s}'

def fix_name(name):
    name = name.replace('. ', r'.\ ')
    name = name.replace('fruh', r'fr\"{u}h')
    return name

def format_number(flt):
    if int(flt) == flt:
        return ('%d' % flt)
    else:
        return ('%.1f' % flt)

def format_alpha(alpha):
    if len(alpha) == 1 or alpha[0] == alpha[1]:
        return r'%s\%%' % format_number(alpha[0])
    else:
        return r'%s--%s\%%' % tuple(map(format_number, alpha))

def fix_beer(beer):
    beer = beer.replace('Koelsch', r'K\"{o}lsch')
    beer = beer.replace('Kolsch', r'K\"{o}lsch')
    beer = beer.replace(' ', '~')
    return beer

TYPES = {
    'finishing': 'Finishing',
    'bittering': 'Bittering',
    'aroma': 'Aroma',
    'flavor': 'Flavor',
    'all purpose': 'All Purpose',
    'dual purpose': 'Dual Purpose',
}

def fix_type(htype):
    return TYPES[htype]

COUNTRIES = {
    'US' : 'US',
    'UK' : 'UK',
    'Germany' : 'DE',
    'German' : 'DE',
    'Czech' : 'CZ',
    'New Zealand' : 'NZ',
    'Canada' : 'CA',
    'Australia' : 'AU',
    'AU' : 'AU',
    'Japan' : 'JP',
    'Poland' : 'PL',
    'SI' : 'SI',
}

def fix_country(country):
    return COUNTRIES[country]

def fix_descr(desc):
    desc = desc.replace('uber alles', r'\"{u}ber alles')
    desc = desc.replace('fruh', r'fr\"{u}h')
    return desc

def order_hops(hops):
    if os.path.exists(PERMFILE):
        with open(PERMFILE, 'r+') as f:
            perm = [int(l.strip()) for l in f]
        hops = [hops[p] for p in perm]
        return hops

    hops = sorted(hops, key=lambda h: -np.average(h['alpha']))
    hops = sum((sorted(hops[COLS*i:COLS*i+COLS], key=lambda h: h['name']) for i in range(9)), [])
    return hops

def main():
    with open(IFILE, 'r+') as f:
        hops = yaml.load(f.read())

    hops = order_hops(hops)

    lines = []
    for h, hop in enumerate(hops):
        col = h % COLS
        row = h / COLS
        x, y = (START + col*COLSKIP), (START + row*ROWSKIP)
        name = fix_name(hop['name'])
        alpha = format_alpha(hop['alpha'])
        countries = ', '.join(map(fix_country, hop['countries']))
        types = ', '.join(map(fix_type, hop['types']))
        description = fix_descr(hop.get('alt_description', hop['description']))
        beers = ', '.join(map(fix_beer, hop['uses']))
        lines.append(FMT % (x, y, name, alpha, description, beers, types, countries))

    data = '\n'.join(lines)
    with open(OFILE, 'wb+') as f:
        f.write(data)

if __name__ == '__main__':
    main()
