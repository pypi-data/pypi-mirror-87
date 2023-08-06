from odoo import models, fields

from table import init_table


def print_property_values(user_ns, line):
    env = user_ns['env']
    field = eval(line, user_ns)

    if isinstance(field, fields.Field):
        field = env['ir.model.fields'].search([
            ('model', '=', field.model_name),
            ('name', '=', field.name),
        ])
        assert field.ensure_one()

    assert isinstance(field, models.Model)
    assert field._name == 'ir.model.fields'

    field_type = field.ttype
    domain = [('fields_id', '=', field.id)]

    properties = env['ir.property'].search(domain).mapped('company_id')
    properties = env['ir.property'].search_read(domain, ['res_id', 'company_id', field.ttype])


    attrs = []
    attrs.append([''] + [format_location(location) for location in locations])

    for route, locations in result.items():
        row = [format_route(route, warehouse)]
        attrs.append(row)
        for location, rules in locations.items():
            row.append('\n\n'.join(map(format_rule, rules)))


