from collections import OrderedDict

from odoo.models import LOG_ACCESS_COLUMNS, Model


def vals(model):
    model.ensure_one()
    return {field_name: getattr(model, field_name) for field_name in model._fields}


def prepare_value_for_table(record, field_name):

    if field_name == '__xml_id__':
        return record.get_xml_id()[record.id]

    field = record._fields[field_name]

    if field.type == 'binary':
        return "b'...'"
    else:
        return record[field_name]


def value_to_str(value, col_width):
    value_str = unicode(value)

    if len(value_str) > col_width:
        return value_str[:col_width - 1] + '…'

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return value_str.ljust(col_width)
    else:
        return value_str.ljust(col_width)


def pad_table(table):

    row_count = len(table)
    col_count = len(table[0])

    col_widths = {}
    for col_number in range(col_count):
        col_values = [table[row_number][col_number] for row_number in range(row_count)]
        col_lengths = map(len, map(unicode, col_values))
        col_widths[col_number] = max(col_lengths)

    for col_number in range(col_count):
        col_widths[col_number] = min(col_widths[col_number], 60)

    for row_number in range(row_count):
        for col_number in range(col_count):
            value = table[row_number][col_number]
            col_width = col_widths[col_number]

            table[row_number][col_number] = value_to_str(value, col_width)

    return table


def print_table(table):
    for row in table:
        print(' '.join(row))

# TODO skip __xml_id__ row if no data
PINNED_FIELD_NAMES = [
    'id',
    'display_name',
    'name',
    # 'create_date',
    # 'create_uid',
    # 'write_date',
    # 'write_uid',
]

IGNORE_FIELD_NAMES = set(LOG_ACCESS_COLUMNS)
IGNORE_FIELD_NAMES.add('__last_update')


def field_detailed_name(field):
    detailed_name = field.name

    if field.related:
        detailed_name += ' → ' + '.'.join(field.related)

    return detailed_name


def get_field_names(fields):

    field_names = OrderedDict()

    for field_name, field in sorted(fields.items()):
        if field_name in IGNORE_FIELD_NAMES:
            continue

        field_names[field_name] = field_detailed_name(field)

    pinned_field_names = OrderedDict({'__xml_id__': '__xml_id__'})
    pinned_field_names.update((pinned_field_name, field_names.pop(pinned_field_name, ''))
                              for pinned_field_name in PINNED_FIELD_NAMES if pinned_field_name in field_names)

    pinned_field_names.update(field_names)

    return pinned_field_names


def different_row_values(table):
    new_table = []
    for row in table:
        # print set(row[1:])
        if len(set(row[1:])) > 1:
            new_table.append(row)

    # print new_table
    return new_table


def print_recorset(line, user_ns, diff=False):
    # import ipdb
    # ipdb.set_trace()

    if not line.strip():
        line = '_'

    records = eval(line, user_ns)

    if not isinstance(records, Model):
        return records

    field_names = get_field_names(records._fields)

    table = [[''] * (len(records) + 1) for i in range(len(field_names))]

    for row_number, (field_name, field_detailed_name) in enumerate(field_names.items()):
        table[row_number][0] = field_detailed_name

        for col_number, record in enumerate(records, start=1):
            table[row_number][col_number] = prepare_value_for_table(record, field_name)

    if diff:
        table = different_row_values(table)

    pad_table(table)
    print_table(table)

