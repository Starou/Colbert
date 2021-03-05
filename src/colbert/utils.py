# -*- coding: utf-8 -*-

import datetime
import re
from decimal import Decimal

DATE_FMT = "%d/%m/%Y"


def json_encoder(obj):
    if isinstance(obj, datetime.date):
        return obj.strftime(DATE_FMT)
    elif isinstance(obj, Decimal):
        return str(obj)
    raise TypeError


# https://www.python.org/dev/peps/pep-0378/
def fmt_number(value):
    return '{:,.2f}'.format(value).replace(",", " ")


def parse_number(value):
    """Quick'n dirty. """
    return value.replace(" ", "")


def rst_title(title, symbol="="):
    """
    =====
    title
    =====
    """
    stroke = symbol * len(title)
    return "\n".join([stroke, title, stroke])


def rst_section(title, symbol="="):
    """
    title
    =====
    """
    stroke = symbol * len(title)
    return "\n".join([title, stroke])


def rst_table(table):
    header_stroke_char = '='
    normal_stroke_char = '-'
    lines = []
    last_iteration = len(table) - 1
    for i, row in enumerate(table):
        stroke_char = (i == 1) and header_stroke_char or normal_stroke_char
        add_closing_stroke = (i == last_iteration) and True
        lines.extend(rst_table_row(row, stroke_char, add_closing_stroke))
    lines = "\n".join(lines)
    return lines


def rst_table_row(row, stroke_char, add_closing_stroke=False):
    lines = []
    stroke, line = [], []
    if isinstance(row[0][0], list) or isinstance(row[0][0], tuple):
        for j, subrow in enumerate(row):
            line = []
            for k, (cell_content, cell_length) in enumerate(subrow):
                cell_content = truncate_words(cell_content, cell_length - 2)
                # Idéalement, on devrait faire le stroke sur la dernière sous-ligne, pas la premiere.
                if j == 0:
                    stroke.append('+%s' % (stroke_char * cell_length))
                sep = '||' if k < (len(subrow) - 1) else '| '
                line.append('%s %s%s' % (sep, cell_content,
                                          ' ' * (cell_length - 2 - len(cell_content))))
            if j == 0:
                stroke.append('+')
                lines.append(''.join(stroke))

            line.append('|')
            lines.append(''.join(line))
    else:
        for cell_content, cell_length in row:
            cell_content = truncate_words(cell_content, cell_length - 2)
            stroke.append('+%s' % (stroke_char * cell_length))
            line.append('| %s%s' % (cell_content,
                                     ' ' * (cell_length - 1 - len(cell_content))))
        # End of line.
        stroke.append('+')
        line.append('|')

        lines.append(''.join(stroke))
        lines.append(''.join(line))
    if add_closing_stroke:
        lines.append(''.join(stroke))

    return lines


# http://stackoverflow.com/questions/250357/smart-truncate-in-python
def truncate_words(content, length=100, suffix='...'):
    if len(content) <= length:
        return content
    else:
        content_trunc = ' '.join(content[:length + 1 - len(suffix)].split(' ')[0:-1])
        # On rétabli un éventuel contexte italique tronqué.
        if content_trunc.count("*") % 2:
            content_trunc = "%s*" % content_trunc[:-1]
        return content_trunc + suffix


def d_round(value, rounding=2):
    r = Decimal(10) ** -rounding
    return value.quantize(r)


def decode_as_ecriture(ecriture_json):
    out = {}
    for k, v in ecriture_json.items():
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
