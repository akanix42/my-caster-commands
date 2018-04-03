from inspect import getargspec
from dragonfly import Alternative, Compound


class FuncChoice(Alternative):

    def __init__(self, choices, name = None, extras = None, default = None):

        # Argument type checking.
        assert isinstance(name, basestring) or name is None
        assert isinstance(choices, dict)
        for k, v in choices.iteritems():
            assert isinstance(k, basestring)

        # Construct children from the given choice keys and values.
        self._choices = choices
        self._extras = extras
        children = []
        for k, v in choices.iteritems():
            if callable(v):
                child = Compound(spec = k, value_func = v, extras = extras)
            else:
                child = Compound(spec = k, value = v, extras = extras)
            children.append(child)

        # Initialize super class.
        Alternative.__init__(self, children = children,
                             name = name, default = default)


def F(func):
    (args, varargs, varkw, defaults) = getargspec(func)
    if varkw:
        _filter_keywords = False
    else:
        _filter_keywords = True
    _valid_keywords = set(args)

    def wrap_func(node, extras):
        if _filter_keywords:
            invalid_keywords = set(extras.keys()) - _valid_keywords
            for key in invalid_keywords:
                del extras[key]
        return func(**extras)

    return wrap_func
