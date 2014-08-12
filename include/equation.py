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
without predefined alignment are aligned on the first '='.
"""

from pandocfilters import toJSONFilter, RawBlock, Div
import re
import sys

def latex(x):
  return RawBlock('latex',x)

def html(x):
    return RawBlock('html', x)

def DisplayMath(x):
    return { u'c': [{u'c': [{u'c': [], u't': u'DisplayMath'}, x], u't': u'Math'}], u't': u'Plain'} 

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
    global relSymbol
    relPattern = '|'.join(relSymbol)
    if re.search(r'[^\\]&', x) is None:
         idx = re.search(relPattern, x).start()
         return x[:idx] + '&' + x[idx:]
    return x

def alignHtmlMath(x):
    global relSymbol
    relPattern = r'|'.join(relSymbol)
    cols = re.split(r"[^\\]&(?!" + relPattern + ")", x)
    align = [re.search(r"[^\\]&", x) for x in cols]
    out = []
    for i in range(len(align)): 
        if align[i] is not None:
            idx = align[i].start()
            skip = 1
        else:
            idx = re.search(relPattern, cols[i]).start()
            skip = 0
        out = out + [[cols[i][:idx+skip], cols[i][idx+2*skip:idx+2*skip+1], 
                     cols[i][idx+2*skip+1:]]] 
    return out
    
def formatHtmlMath(eq):
    return [html(' <td class=\"eq_left\"> ')] + \
    [DisplayMath(eq[0])] + \
    [html(' </td>' + "\n")] + \
    [html(' <td class=\"eq_centre\">')] + \
    [DisplayMath(eq[1])] + \
    [html(' </td>' + "\n")] + \
    [html(' <td class=\"eq_right\"> ')] + \
    [DisplayMath(eq[2])] + \
    [html(' </td>' + "\n")]

relSymbol = ['\\leq', '\\geq', '\\equiv', '\\models', '\\prec', '\\succ', '\\sim'
             '\\perp', '\\preceq', '\\succeq', '\\simeq', '\\mid', '\\ll', '\\gg',
             '\\asymp', '\\parallel', '\\subset', '\\supset', '\\approx', '\\bowtie',
             '\\subseteq', '\\supseteq', '\\cong', '\\Join', '\\sqsubset', '\\sqsupset',
             '\\neq', '\\smile', '\\sqsubseteq', '\\sqsupseteq', '\\doteq', '\\frown',
             '\\in', '\\ni', '\\propto', '=', '\\vdash', '\\dashv', '<', '>']

eqCount = 0

def equation(key, value, format, meta):
    if key == 'Div':
        [[ident,classes,kvs], contents] = value
        if 'equation' in classes:
            math = iter_flatten([ getMath(contents)])
            math = [x for x in math if x is not None]
            label = ''
            global eqCount 
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
            if format == 'html' or format == 'html5':
                math = [alignHtmlMath(x) for x in math]
                if ident != '':
                    label = 'id=\"' + ident + '\" '
                head = [html('<table ' + label + 'class=\"' + ' '.join(classes) + '\" ' + \
                    ' '.join(kvs) + '>' + "\n")]
                tail = [html('</table>' + "\n")]
                body = [html('<tbody>' + "\n")]
                for eq in math:
                    eqCount = eqCount + 1
                    body = body + [html('<tr>' + "\n")] 
                    for sub in [formatHtmlMath(y) for y in eq]:
                        body = body + sub
                    if ident != '':
                        body = body + [html(' <td class=\"eq_number\"> <br>(' + \
                                            str(eqCount) + ')<br> </td>')]
                    body = body + [html('</tr>' + "\n")]
                body = body + [html('</tbody>' + "\n")]
                return head + body + tail
                
        
if __name__ == '__main__':
    toJSONFilter(equation)