# -*- coding: utf-8 -*-

import datetime
import locale
import re
from decimal import Decimal

DATE_FMT = "%d/%m/%Y"

def json_encoder(obj):
    if isinstance(obj, datetime.date):
        return obj.strftime(DATE_FMT)
    elif isinstance(obj, Decimal):
        return str(obj)
    raise TypeError
        
def fmt_number(value):
    return locale.format("%.2f", value, grouping=True)

def rst_title(title, symbol="="):
    """
    =====
    title
    =====
    """
    stroke = symbol * len(title)
    return u"\n".join([stroke, title, stroke])

def rst_section(title, symbol="="):
    """
    title
    =====
    """
    stroke = symbol * len(title)
    return u"\n".join([title, stroke])

def rst_table(table):
    header_stroke_char = '='
    normal_stroke_char = '-'

    lines = []
    for i, row in enumerate(table):
        stroke, line = [], []
        stroke_char = (i == 1) and header_stroke_char or normal_stroke_char
        # Multiline row.
        if isinstance(row[0][0], list) or isinstance(row[0][0], tuple):
            for j, subrow in enumerate(row):
                line = []
                for cell_content, cell_length in subrow:
                    cell_content = truncate_words(cell_content, cell_length-2)
                    # Idéalement, on devrait faire le stroke sur la dernière sous-ligne, pas la premiere.
                    if j == 0:
                        stroke.append(u'+%s' % (stroke_char*cell_length))
                    line.append(u'|| %s%s' % (cell_content, 
                                             u' ' * (cell_length - 2 - len(cell_content))))
                if j == 0:
                    stroke.append(u'+')
                    lines.append(u''.join(stroke))

                line.append(u'|')
                lines.append(u''.join(line))

        else:
            for cell_content, cell_length in row:
                cell_content = truncate_words(cell_content, cell_length-2)
                stroke.append(u'+%s' % (stroke_char*cell_length))
                line.append(u'| %s%s' % (cell_content, 
                                         u' ' * (cell_length - 1 - len(cell_content))))
            # End of line.
            stroke.append(u'+')
            line.append(u'|')

            lines.append(''.join(stroke))
            lines.append(''.join(line))
    
    # A final line of strokes.
    lines.append(''.join(stroke))
    return u"\n".join(lines)

# http://stackoverflow.com/questions/250357/smart-truncate-in-python
def truncate_words(content, length=100, suffix='...'):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length+1-len(suffix)].split(' ')[0:-1]) + suffix

def d_round(value, rounding=2):
    r = Decimal(10) ** -rounding
    return value.quantize(r)

def decode_as_ecriture(ecriture_json):
    out = {}
    for k, v in ecriture_json.iteritems():
        try:
            v = Decimal(v)
        except:
            pass
        else:
            out[k] = v
            continue

        try:
            v = datetime.datetime.strptime(v, DATE_FMT).date()
        except:
            pass
        else:
            out[k] = v
            continue

        out[k] = v

    return out

def latex_escape(string):
    return re.sub(r"([&%$#_{}~^\\])", r"\\\1", string)
