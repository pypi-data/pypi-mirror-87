from collections import defaultdict, namedtuple

PERM_NAMES = ('read', 'write', 'create', 'unlink')
PERMS = tuple('perm_' + perm_name for perm_name in PERM_NAMES)


class ModelRestrictions:
    def __init__(self):
        self.model_accesses = []
        self.global_rules = []
        self.group_rules = []

    @property
    def global_domains(self):
        return [rule.domain for rule in self.global_rules]

    @property
    def group_domains(self):
        return [rule.domain for rule in self.group_rules]


def get_user_permissions(env, user):
    if type(user) is int:
        user = env['res.users'].browse(user)

    assert isinstance(user, env['res.users'].__class__), 'User object is needed'
    user.ensure_one()


    # access = defaultdict(namedtuple('access', 'model_access global_rules group_rules'))
    # group_rules = defaultdict(list)

    restrictions = defaultdict(ModelRestrictions)

    # Group by model:
    # 1. group model access
    group_user = env.ref('base.group_user')
    boring_group_ids = [group_user.id] + group_user.trans_implied_ids.ids
    interest_groups = user.groups_id.filtered(lambda group: group.id not in boring_group_ids)

    for model_access in interest_groups.mapped('model_access'):
        restrictions[model_access.model_id].model_accesses.append(model_access)

    # 2. group rules
    for rule in interest_groups.mapped('rule_groups'):
        restrictions[rule.model_id].group_rules.append(rule)

    user_model_ids = [model.id for model in restrictions.keys()]

    # 3. global model access
    for model_access in env['ir.model.access'].search([
            ('model_id', 'in', user_model_ids),
            ('group_id', '=', None),
        ]):
        restrictions[model_access.model_id].model_accesses.append(model_access)

    # 4. global rules
    for rule in env['ir.rule'].search([
            ('model_id', 'in', user_model_ids),
            ('global', '=', True),
        ]):
        restrictions[rule.model_id].global_rules.append(rule)

    # Join all rules
    # for model, model_restrictions in restrictions.items():
        # restrictions[model].domain = join_domains(model_restrictions.global_domains, model_restrictions.group_domains)
        # model_restrictions.rule_root = construct_tree(model_restrictions.global_rules, model_restrictions.group_rules)

    return restrictions


def combine(operator, operands):
    """
    There is odoo.osv.expression.combine function.
    But it crop expressions on TRUE and FALSE domains.
    """
    return [operator] * (len(operands) - 1) + operands


def s(a, b):
    print(a, b)
    return a + b


def calc_rule_domain(domain):
    # make from domain simple human readable string.
    # Its part of visualization
    pass


def and_nodes(rule1, rule2):
    if not isinstance(rule1, RuleNode):
        normalize_domain(rule1.domain)
    return RuleNode('&', rule1, rule2)


def construct_tree(global_rules, group_rules):
    global_rules_node = reduce(lambda x, y: RuleNode('&', x, y), global_rules)
    group_rules_node = reduce(lambda x, y: RuleNode('|', x, y), group_rules)
    return RuleNode('&', global_rules_node, group_rules_node)


# TODO Write tests
def join_domains(global_domains, group_domains):
    # [(1, '==', 1), (0, '==', 1)]  =>  ['&', (1, '==', 1), (0, '==', 1)]
    # [(2, '==', 2), (0, '==', 2)]
    group_rules_norm_domains = list(map(normalize_domain, group_domains))
    global_rules_norm_domains = list(map(normalize_domain, global_domains))

    # We loose info
    group_rules_domain = combine('|', group_rules_norm_domains)
    return combine('&', global_rules_norm_domains + [group_rules_domain])


def calc_model_access(env, access_or_rule_list):
    rules = env['ir.rule']
    model_access = env['ir.rule']

    perms = {
        'perm_read': 0,
        'perm_write': 0,
        'perm_create': 0,
        'perm_unlinck': 0,
    }

    help = {
        'perm_read': [],
        'perm_write': [],
        'perm_create': [],
        'perm_unlinck': [],
    }
    for access_or_rule in access_or_rule_list:
        # if isinstance(access_or_rule, rules.__class__):
        #     pass

        # Calc access control
        if access_or_rule.__class__.__name__ == 'ir.module.access':
            for perm in perms:
                if getattr(access_or_rule, perm):
                    perms[perm] = 1
                    help[perm] = access_or_rule

        elif access_or_rule.__class__.__name__ == 'ir.rule':
            for perm in perms:
                if getattr(access_or_rule, perm):
                    perms[perm] = access_or_rule


class RuleNode:
    OPERATORS = {'!', '&', '|'}

    def __init__(self, value, left=None, right=None, domain=None):
        self.value = value
        self.left = left
        self.right = right
        self.domain = domain

    @property
    def is_operator(self):
        return self.value in self.OPERATORS

    def __str__(self):
        if self.value in {'&', '|'}:
            return '{self.left} {self.value} {self.right}'.format(self=self)
        else:
            return str(self.value)


def from_polish_notation(domain):
    """
    From Polish notation to tree
    """

    BINARY_OPERATORS = {'&', '|'}

    stack = []
    while domain:
        token = domain.pop()

        if token in BINARY_OPERATORS:
            stack.append(RuleNode(token, stack.pop(), stack.pop()))

        elif token == '!':
            stack.append(RuleNode(token, stack.pop()))

        else:
            stack.append(RuleNode(token))

    return stack[0]


def humanize_domain(domain):
    # [(1 ,'=', 1)]         Any
    # [(0 ,'=', 1)]         Neither
    # (*,'=',False)         no soma
    # ('company_id','=',False)  no company
    # ('company_id','in',[company.id for company in user.company_ids])  user company

    # ('warehouse_id.company_id', '=', False)
    # ('warehouse_id.company_id', 'in', [company.id for company in user.company_ids])       warehouse in user company
    # ('*.company_id', 'in', [])    * in user company

    # ('user_id', '=', 1)   is superuser
    pass


def get_user_exact_groups(user):
    user_trans_implied_groups = user.groups_id.mapped('trans_implied_ids')
    return user.groups_id.filtered(lambda g: g.id not in user_trans_implied_groups.ids)


def get_humanize_perms(model):
    model.ensure_one()
    return ','.join(perm_name[0] for perm_name in PERM_NAMES if getattr(model, 'perm_' + perm_name))


def get_model_access_dict(model_access):
    return OrderedDict(name=model_access.name, display_name=model_access.display_name,
                       model=model_access.model_id.model, perms=get_humanize_perms(model_access))


# =============== Other stuff ==================
def user_rights(line, user_ns):

    user_literal, model_literal = line.split()

    user = eval(user_literal, user_ns)
    user.ensure_one()

    model = eval(model_literal, user_ns)

    env = user_ns['env']

    model_access = env['ir.model.access'].search([
        ('group_id', 'in', user.groups_id.ids),
        ('model_id', '=', model._name),
    ])

    rules = env['ir.rule'].search([
        ('groups', 'in', user.groups_id.ids),
        ('model_id', '=', model._name),
    ])

    return model_access, rules
