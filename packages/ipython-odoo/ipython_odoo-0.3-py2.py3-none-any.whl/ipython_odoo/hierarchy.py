import re
import inspect

from odoo.models import Model
from odoo.fields import Field

import baron
import redbaron
from texttable import Texttable

s = ''
def prepare_function(func):
    try:
        func_source = inspect.getsource(func)
    except OSError as error:
        func_source = unicode(error)

    # Decrease indent
    func_source_lines = [line for line in func_source.splitlines() if line.strip()]
    min_indent_count = min(len(re.match('^ *', line).group()) for line in func_source_lines)
    func_source = '\n'.join(line[min_indent_count:].rstrip() for line in func_source_lines)

    try:
        red = redbaron.RedBaron(func_source)
    except baron.parser.ParsingError:
        if '@api.returns' in func_source:
            return '-@api.returns-'
        else:
            return '-parsing error-'

    func_def = red[0]
    assert func_def.type == 'def'

    func_body = func_def.value

    # Remove docstring
    first_line = func_body[0]
    if first_line.type == 'string' and first_line.name is None:
        del func_body[0]

    min_indent_count = min(len(line.indentation) for line in func_body)
    func_body.decrease_indentation(min_indent_count)

    func_body_source = func_body.dumps()

    if len(func_body_source) < 180:
        return func_body_source
    else:
        return '✓'


def recordset_models(recordset):
    from odoo.models import Model

    return [klass for klass in recordset.__class__.__mro__ if Model in klass.__bases__]


def get_model_attrs(records, model_attr_name=None):
    models = recordset_models(records)
    models.reverse()

    IGNORE_ATTRS = {'_module', '__module__', '_inherit', '_order', '_name', '_description', '__doc__',
                    '_local_constraints', '_local_sql_constraints',}

    # Headers
    attrs = [[''] + [model._module for model in models]]

    # TODO show _inherits model attrs like in res.users and product.product
    names = set()
    for model in models:
        if model_attr_name:
            model_attr_names = [model_attr_name]
        else:
            model_attr_names = sorted(model.__dict__.keys())

        for name in model_attr_names:
            if name in names:
                continue

            if name in IGNORE_ATTRS:
                continue

            attrs.append([name] + [mdl.__dict__.get(name) for mdl in models])
            names.add(name)

    return attrs


def prepare_model_attrs(attrs):

    row_count = len(attrs)
    col_count = len(attrs[0])

    for col in xrange(col_count):
        for row in xrange(row_count):
            attr = attrs[row][col]

            if isinstance(attr, Field):
                attrs[row][col] = attr.__class__.__name__

            elif attr is None:
                attrs[row][col] = ''

            elif callable(attr):
                # attrs[row][col] = u'✓'
                attrs[row][col] = prepare_function(attr)

    return attrs


def print_model_attrs(attrs):
    table = Texttable()

    table.set_deco(Texttable.HEADER | Texttable.VLINES | Texttable.HLINES)
    table.set_max_width(180)

    table.add_rows(attrs)

    print(table.draw())

# Python AST
# https://github.com/PyCQA/redbaron         Preferred
# https://github.com/python-rope/rope

# Для вывода таблиц в консоль есть модули   Last release    Stars
# https://pypi.org/project/texttable/       2019            200
# https://pypi.org/project/tabulate/        2019            100
# https://pypi.org/project/termtables/      2019            15
# https://pypi.org/project/tableprint/      2018            100
# https://pypi.org/project/terminaltables/  2016            600
# https://pypi.org/project/PrettyTable/     2013
# https://pypi.org/project/asciitable/      2011
