import collections
import argparse
import inspect
import sys
from functools import wraps, partial as ft_partial
from typing import Generator, Union, Optional, Tuple
import pprint


class SubcommandBase:
    """Abstract definition for a single command.
    Accept by the Subcommands._add function"""

    def __init__(self, name, action, arguments, help=None):  # pylint: disable=redefined-builtin
        self.name = name
        self.help = help
        self.action = action
        self.arguments = arguments

    def add_to_parser(self, parser: argparse.ArgumentParser, actions):
        pass


class Subcommands:
    """Entry point to command line interfaces.

    Add subcommands by deriving from this class and specify
    commands in the static :subcommands: variable
    """
    description: Optional[str] = None
    required = True
    subcommands: Tuple[SubcommandBase, ...] = ()
    version: Optional[str] = None

    def __init__(self, *args, **kwargs):
        parser = argparse.ArgumentParser(
            description=self.description,
            formatter_class=argparse.RawDescriptionHelpFormatter)
        if self.version is not None:
            parser.add_argument('--version', action='version',
                                version=self.version)
        subparsers = parser.add_subparsers(
            dest='action', help='Action help')
        subparsers.required = self.required
        actions = {}
        for cmd in self.subcommands:
            cmd.add_to_parser(subparsers, actions)
        cmd_args = vars(parser.parse_args(*args, **kwargs))
        action = actions[cmd_args.pop("action")]
        action(**cmd_args)


class Subcommand(SubcommandBase):
    """A single subcommand corresponding to a function f of the main workflow
    """

    def __init__(self, f, **kwargs):
        omit = frozenset(getattr(f, "keywords", ()))
        omit_pos = frozenset(range(len(getattr(f, "args", ()))))
        args = arguments_by_signature(f,
                                      omit_positionals=omit_pos,
                                      omit_keywords=omit,
                                      **kwargs)
        super().__init__(name=kebab_case(f.__name__), action=f,
                         arguments=tuple(args), help=f.__doc__)

    def add_to_parser(self, parser, actions):
        subparser = parser.add_parser(self.name, help=self.help)
        actions[self.name] = self.action
        for arg in self.arguments:
            arg.add_to_parser(subparser)


class SubcommandGroup(SubcommandBase):
    """A subcommand consisting of multiple subsubcommands corresponding
    to functions without arguments"""

    def __init__(self, name, *fcts, help=None):  # pylint: disable=redefined-builtin
        def call(f):
            f()
        arguments = (Argument("--" + f.__name__, action="store_const",
                              dest="f", const=f) for f in fcts)
        super().__init__(name=name, action=call,
                         arguments=arguments, help=help)

    def add_to_parser(self, parser, actions):
        actions[self.name] = self.action
        subparser = parser.add_parser(self.name, help=self.help)
        group = subparser.add_mutually_exclusive_group(required=True)
        for arg in self.arguments:
            arg.add_to_parser(group)


class Argument:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def add_to_parser(self, parser):
        parser.add_argument(*self.args, **self.kwargs)

    @classmethod
    def primitive(cls, dest, arg_names, **kwargs):
        return (cls(*arg_names, dest=dest, **kwargs),)

    @classmethod
    def positional_bool(cls, dest, arg_names, **kwargs):
        return cls.primitive(dest, arg_names, type=parse_bool, **kwargs)

    @classmethod
    def keyword_bool(cls, dest, arg_names, default=False, help=None, **kwargs):  # pylint: disable=redefined-builtin
        kwargs.pop("required", None)
        long_arg_names = tuple(filter(lambda n: n.startswith("--"), arg_names))
        short_arg_names = tuple(
            filter(lambda n: n not in long_arg_names, arg_names))
        negation_flags = tuple(
            a.replace("--", "--no-") for a in long_arg_names)
        default_flags = arg_names if default else negation_flags
        if short_arg_names and default:
            raise ValueError(
                "booleans with short argument name and default=True are not supported")
        if help:
            help += " "
        else:
            help = ""
        help += f"(disable with {', '.join(negation_flags)}, default: {', '.join(default_flags)})"
        return ArgumentMutExGroup(
            cls(*arg_names,
                action="store_true",
                dest=dest,
                default=default,
                help=help,
                **kwargs),
            cls(*negation_flags,
                action="store_false",
                default=default,
                dest=dest,
                help=argparse.SUPPRESS
                )
        )


class ArgumentMutExGroup:
    def __init__(self, *args: Argument):
        self.args = args

    def add_to_parser(self, parser):
        grp = parser.add_mutually_exclusive_group()
        for arg in self.args:
            arg.add_to_parser(grp)


def decorate(f, *decorators):
    for dec in decorators:
        f = dec(f)
    return f


# Starting with python 3.7, the typing module has a new API
_origin_attr = "__extra__" if sys.version_info < (3, 7) else "__origin__"


def arguments_by_signature(f, overrides=None,
                           omit_keywords=frozenset(),
                           omit_positionals=frozenset()) -> Generator[Argument, None, None]:
    """Builds argparser arguments according to the signature of a function f.
    Type hint annotations are used to infer the type for argparse"""
    sig = inspect.signature(f)
    if overrides is None:
        overrides = {}
    unknown_parameters = set(overrides) - set(sig.parameters)
    if unknown_parameters:
        raise ValueError("Function {} does not have arguments {} "
                         "(which have been provided as parameter docs)".format(
                             f.__name__, ", ".join(unknown_parameters)))
    has_keyword_only = any(
        p.kind is inspect.Parameter.KEYWORD_ONLY
        for p in sig.parameters.values())
    for pos, (p_name, p) in enumerate(sig.parameters.items()):
        if p_name in omit_keywords or pos in omit_positionals:
            continue
        positional = has_keyword_only and \
            p.kind is not inspect.Parameter.KEYWORD_ONLY
        p_overrides = overrides.get(p_name, {})
        arg_names = make_arg_names(p_overrides.get(
            "name", kebab_case(p_name) if not positional else p_name),
            p_overrides.get("alias", ()), positional)
        default = p_overrides.get("default", p.default)
        args = dict(help=p_overrides.get("help"))
        t = p_overrides.get("type", p.annotation)
        if t is inspect.Signature.empty:
            raise ValueError(f"Argument {arg_names[0]} has no type annotation")
        opt_type = optional_type(t)
        if opt_type is not None:
            if default is inspect.Signature.empty:
                raise ValueError(
                    f"{f.__name__}: {p_name}: typing.Optional arguments are "
                    "allowed only when accompanied with a default value")
            t = opt_type

        if not positional:
            args["dest"] = p_overrides.get("dest", p_name)
            args.update(default_args(default))
        if t is bool:
            if positional:
                yield Argument.positional_bool(arg_names=arg_names,
                                               **args)
            else:
                yield Argument.keyword_bool(arg_names=arg_names, **args)
            continue
        if is_sequence(t):
            t = getattr(t, "__args__", (str,))[0]
            if default is not inspect.Signature.empty:
                args["default"] = default
            if positional:
                args["nargs"] = '+' if default is inspect.Signature.empty else '*'
            else:
                args["action"] = "append"
        yield Argument(*arg_names, type=t, **args)


def default_args(default):
    if default is inspect.Signature.empty:
        return {"required": True}
    return {"default": default}


def make_arg_names(name, aliases, positional: bool):
    """Combines name and aliases into one tuple of argument names
    including "--"
    """
    n_dashes = min(2, len(name))
    arg_prefix = "-" * n_dashes
    if positional:
        if aliases:
            raise ValueError(
                "Aliases not allowed for positional arguments")
        arg_prefix = ""
    arg_names = (arg_prefix + name,)
    if isinstance(aliases, str):
        aliases = (aliases,)
    return arg_names + tuple(aliases)


bool_true_literals = ("1", "true", "y", "yes")
bool_false_literals = ("0", "false", "n", "no")

bool_literal_mapping = dict(
    [(l, True) for l in bool_true_literals] +
    [(l, False) for l in bool_false_literals])


def parse_bool(s):
    return bool_literal_mapping[s]


def is_sequence(t):
    t_origin = getattr(t, "__origin__", None)
    return isinstance(t_origin, type) and \
        issubclass(t_origin, collections.abc.Sequence)


def partial(*args, **kwargs):
    """Modified version of :functools.partial: which preserves
    __name__ and __doc__ attributes and can be used as a decorator
    """
    def decorator(f):
        keywords = getattr(f, "keywords", {})
        f_new = ft_partial(f, *args, **{**keywords, **kwargs})
        f_new.__name__ = f.__name__
        f_new.__doc__ = f.__doc__
        return f_new
    return decorator


def lazy_partial(*args, **kwargs):
    """Similar to :functools.partial: but load bound arguments at runtime of
    the wrapped function, by calling the arguments.
    """
    def decorator(f):
        @wraps(f)
        def wrapped_f(*_args, **_kwargs):
            newkeywords = {key: val()
                           for key, val in kwargs.items()}
            newkeywords.update(_kwargs)
            return f(*map(lambda f: f(), args), *_args, **newkeywords)

        wrapped_f.args = getattr(f, "args", ()) + args
        new_keywords = getattr(f, "keywords", {})
        new_keywords.update(kwargs)
        wrapped_f.keywords = new_keywords

        return wrapped_f
    return decorator


def set_default(**defaults):
    """Sets or changes default values of the decorated function"""
    def decorator(f):
        @wraps(f)
        def _f(*args, **kwargs):
            return f(*args, **{**defaults, **kwargs})
        return _f
    return decorator


def rename(name: str):
    """Changes the name of a function"""
    def wrapper(f):
        def wrapped(*args, **kwargs):
            return f(*args, **kwargs)
        wrapped.__name__ = name
        return wrapped
    return wrapper


def block(*arg_names: str):
    """Hides argument of a function from arguments_by_signature"""
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            return f(*args, **kwargs)
        keywords = getattr(wrapped, "keywords", {})
        keywords.update({n: object() for n in arg_names})
        wrapped.keywords = keywords
        return wrapped
    return wrapper


def return_to_stdout(f):
    """Converts a function :f: into a function pretty printing the
    return value of :f: and returning None
    """
    pp = pprint.PrettyPrinter(indent=2)

    @wraps(f)
    def wrapper(*args, **kwargs):
        pp.pprint(f(*args, **kwargs))
    return wrapper


def kebab_case(name):
    return name.replace("_", "-")


def optional_type(T: type) -> Optional[type]:
    """For Optional types provided by typing, return the underlying python type,
    else None.
    E.g. returns int for typing.Optional[int]"""
    if getattr(T, "__origin__", None) is not Union:
        return None
    try:
        # Here T has attribute __origin__. Thus it is a typing._GenericAlias
        T1, T2 = T.__args__  # type: ignore
    except ValueError:
        return None
    if isinstance(None, T1):
        return T2
    if isinstance(None, T2):
        return T1
    return None
