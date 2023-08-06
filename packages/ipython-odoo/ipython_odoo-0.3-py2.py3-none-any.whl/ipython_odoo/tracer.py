import inspect
import logging
import re
import sys
from contextlib import contextmanager
from functools import wraps

from odoo.models import BaseModel

from .hierarchy import recordset_models

INTEREST_METHODS = {
    'sale.order': {
        '_prepare',
        'search',
    },

    'all': {
        'create',
        'write',
        'unlink',
    },
}

logger = logging.getLogger('debug')


def path_model_method(method):

    @wraps(method)
    def wrapped_method(self, *args, **kwargs):
        logger.debug('soma')
        return method(self, *args, **kwargs)

    return wrapped_method


def patch_model_methods(env):

    any_model_methods = INTEREST_METHODS.pop('all', set())

    for model_name, method_names in INTEREST_METHODS:
        models = recordset_models(env[model_name])
        for method_name in method_names:

            method = models.__dict__.get(method_name)
            if method:
                pass

# TRACE
all_method_names = reduce(set.union, INTEREST_METHODS.values())


def get_Model_methods():
    instancemethod = type(BaseModel.create)

    method_names = set()

    for attr_name in dir(BaseModel):
        if isinstance(getattr(BaseModel, attr_name), (instancemethod, property)):
            method_names.add(attr_name)

    return method_names


def get_skip_method_names():
    method_names = get_Model_methods()

    method_names -= {
        'create',
        'search',
    }

    method_names |= {
        '<lambda>',
        '_cache',
        'ids',

        # mail
        'message_get_reply_to',
        'message_post',
        '_get_tracked_fields',
        'message_track',
        '_message_track',
        '_track_subtype',
        '_message_track_post_template',
        '_message_get_auto_subscribe_fields',
        'message_auto_subscribe',
        '_message_post_process_attachments',
        '_track_template',
        '_message_track_get_changes',
        'message_post_with_view',
        'message_post_with_template',

        # sale
        'compute_actual_finish_date',
        'check_done',

        # HZ
        'loop',
        'aggregate',
    }
    return method_names


skip_methods = get_skip_method_names()

def get_self(frame):
    func_name = frame.f_code.co_name

    if func_name.startswith('__') and func_name.endswith('__'):
        return None, None

    if func_name in skip_methods:
        return None, None

    if func_name.startswith('_compute_'):
        return None, None

    try:
        args_info = inspect.getargvalues(frame)
    except IndexError:
        # print 'IndexError'
        return None, None

    self = 'self' in args_info[0] and args_info.locals.get('self')

    if not isinstance(self, BaseModel):
        return None, None

    if self._original_module in {
            'base',
            'mail',
            'decimal_precision',
            'bus',

            'account',
            }:
        return None, None

    try:
        if args_info[0] and args_info[0][0] == 'self':
            args_info[0].pop(0)

        args = inspect.formatargvalues(*args_info)
    except KeyError:
        print frame.f_code.co_name
        print args_info
        raise KeyError

    return self, args


class Tracer(object):
    def __init__(self):
        self.level = None

    def __enter__(self):
        sys.settrace(self.trace)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.settrace(None)

    def print_indent(self, line, newline=False):
        indent = '    ' * self.level
        if newline:
            print
        print '{}{}'.format(indent, line)

    def print_return_indent(self, line):
        indent = '    ' * (self.level + 1)
        print '{}{}'.format(indent, line)

    def print_return(self, arg):
        if isinstance(arg, dict):
            self.print_return_indent('return {')
            for key, value in sorted(arg.items()):
                self.print_return_indent('        {!r}: {}'.format(key, value))
            self.print_return_indent('       }')
        else:
            self.print_return_indent('{} {}'.format('return', arg))

    def trace(self, frame, event, arg):

        if event == 'call':
            rs, args = get_self(frame)
            if rs is not None:
                if self.level is None:
                    self.level = 0
                else:
                    self.level += 1

                file_path = inspect.getsourcefile(frame.f_code)

                match = re.match('.+/(?:addons|custom_addons)/(.+)', file_path)
                if match:
                    addon_model_path = match.groups()[0]
                    self.print_indent('# {}:{}'.format(addon_model_path, frame.f_lineno), newline=True)

                self.print_indent('{}.{}{}'.format(rs, frame.f_code.co_name, args))

                return self.trace

        elif event == 'return':
            rs, args = get_self(frame)
            if rs is not None:
                self.print_return(arg)

                if self.level:
                    self.level -= 1
