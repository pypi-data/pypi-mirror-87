# merge
def merge(model, replaceents):
    pass


def refferencing_records(env, recordset):

    many2x_fields = env['ir.model.fields'].search([
        ('ttype', 'in', ['many2one', 'many2many']),
        ('relation', '=', recordset._name),
        ('store', '=', True),
    ])

    many2x_fields = many2x_fields.filtered(lambda f: f.model in env
                                                     and f.name in env[f.model]._fields)

    result = []
    for field in many2x_fields.sorted(lambda x: (x.model, x.name)):
        rel_rs = env[field.model].with_context(active_test=False).search([
            (field.name, 'in', recordset.ids),
        ])
        if rel_rs:
            result.append((field.name, rel_rs))

    return result


def related_fields(line, user_ns):
    env = user_ns['env']

    try:
        recordset = eval(line, user_ns)
    except NameError as error:
        recordset = env.get(line)
        if not recordset:
            raise error

    return refferencing_records(env, recordset)
