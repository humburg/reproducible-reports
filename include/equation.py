#! /usr/bin/env python

"""
Pandoc filter to convert the contents of divs with
class 'equation' to equation environments when 
producing latex output.

If the div contains a single math block the equation environment
is used and a label matching the ID of the div (if present) is placed inside.

If the div contains more than one math block the align environment
is used instead but only the first equation is labelled. Alignment
characters present in the equations ('&') are honoured. Equations
without predifined alignment are aligned on the first '='.
"""

from pandocfilters import toJSONFilter, RawBlock, Div
import re
import sys


def latex(x):
  return RawBlock('latex',x)

def debug(key, value, id):
    print >> sys.stderr, id
    print >> sys.stderr, "  key: " + str(key)
    print >> sys.stderr, "    value: " + str(value)

def iter_flatten(iterable):
  it = iter(iterable)
  for e in it:
    if isinstance(e, (list, tuple)):
      for f in iter_flatten(e):
        yield f
    else:
      yield e


def getMath(x):
    if isinstance(x, list):
        return [getMath(l) for l in x]
    if isinstance(x, dict):
        if x['t'] == 'Math':
            return x['c'][1]
        else:
            return getMath(x['c'])

def alignLatexMath(x):
    if re.search(r'[^\\]&', x) is None:
         idx = re.search('=', x).start()
         return x[:idx] + '&' + x[idx:]
    return x    

def equation(key, value, format, meta):
    if key == 'Div':
        [[ident,classes,kvs], contents] = value
        if 'equation' in classes:
            math = iter_flatten([ getMath(contents)])
            math = [x for x in math if x is not None]
            label = '' 
            if format == 'latex':
                type = 'equation'
                if len(math) > 1:
                    type = 'align'
                    math = [alignLatexMath(x) for x in math]
                if ident != '':
                    label = '\\label{' + ident + '}'
                else:
                    type = type + '*'
                return [latex('\\begin{' + type + '}' + label + "\n" + \
                              "\\\\\n".join(math) + \
                              "\n" + '\\end{' + type + '}')]
        
if __name__ == '__main__':
    toJSONFilter(equation)