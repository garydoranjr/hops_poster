#!/usr/bin/env python
from collections import defaultdict
import yaml
    
#\hop{10}{10}{Admiral}{11--15\%}{Said to be citrusy, orange flavored. A good compliment hop to Targets. Good dual purpose hop.}{English IPAs, Ales}{All Purpose}{UK, US}

IFILE = 'hops.yaml'
OFILE = 'hops.tex'

ROWS = 9
COLSKIP = 5.5
ROWSKIP = 3.5
START = 1

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

def main():
    with open(IFILE, 'r+') as f:
        hops = yaml.load(f.read())

    lines = []
    for h, hop in enumerate(hops):
        col = h / ROWS
        row = h % ROWS
        x, y = (START + col*COLSKIP), (START + row*ROWSKIP)
        name = fix_name(hop['name'])
        alpha = format_alpha(hop['alpha'])
        countries = 'US'
        types = 'All Purpose'
        description = hop['description']
        beers = ', '.join(hop['uses'])
        lines.append(FMT % (x, y, name, alpha, description, beers, types, countries))

    data = '\n'.join(lines)
    with open(OFILE, 'wb+') as f:
        f.write(data)

if __name__ == '__main__':
    main()
