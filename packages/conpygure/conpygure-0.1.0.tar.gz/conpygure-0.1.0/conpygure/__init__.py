"""
Conpygure is a library that eases the burden of configuring little python projects.
Configurator objects are classes defined extending the conpygure.Conf class.
Defining your configuration is as easy as:

    >>> import conpygure as c
    >>>
    >>> class A(c.Conf):
    >>>     option_one = "default_value"
    >>>     option_two = 2
    >>>
    >>> @c.subconfig_of(A)
    >>> class B(c.Conf):
    >>>     option_three = ["ab", "cd"]
    >>>     option_four = {"a":1}

To print your serialized configuration:

    >>> print(c.dumps())

Dump and load your config to file:

    >>> c.dump("/path/to/conf.toml")
    >>> c.load("/path/to/conf.toml")

Serializers just need to define dumps and loads methods:

    >>> import json
    >>> c.serializer = json

"""

from inspect import isclass
from pathlib import Path
from typing import Union

import toml

__version__ = "0.0.2"

serializer = toml
config_tree = None


class MetaConf(type):
    """Configuration metaclass, used for some cool operator overloading"""

    @property
    def _serializer(cls):
        """Lazy evaluation of Conpygure serializer, toml is the default one.
        Change it by setting conpygure.serializer to something else (ex. json).

        >>> import conpygure as c
        >>> import json
        >>>
        >>> c.serializer = json

        """
        return serializer

    def __iter__(cls):
        """Method defined to support the built-in dict function"""
        return iter((k, v) for k, v in cls.__dict__.items() if k[0] != "_")

    def __init__(cls, name, base, ns):
        """Base global configuration"""
        global config_tree
        type.__init__(cls, name, base, ns)
        if not config_tree:
            config_tree = cls
        else:
            setattr(config_tree, name, cls)

    def __lshift__(cls, d):
        """You can update configuration values with ConfAbc << d, where d is a dictionary"""
        if not isinstance(d, dict):
            raise TypeError("You can update Conf values only using dictionaries")
        # Check if there's any extra key
        if any(True for key in d if key not in cls):
            raise ValueError(
                "Dictionary structure must be contained in config structure, there are some extra key here!")
        for key in d:
            class_value = getattr(cls, key)
            if isclass(class_value) and issubclass(class_value, Conf):
                class_value << d[key]
            else:
                setattr(cls, key, d[key])
        return cls

    def __contains__(cls, item):
        return item in dict(cls)

    def __str__(cls):
        return cls._dumps()

    def __repr__(cls):
        return str(cls._tree())

    def _dumps(cls):
        """Dump to string"""
        return cls._serializer.dumps(cls._tree())

    def _loads(cls, s):
        """Load from string"""
        cls << cls._serializer.loads(s)

    def _dump(cls, file: Union[str, Path]):
        with open(file, "w") as f:
            f.write(cls._dumps())

    def _load(cls, file: Union[str, Path]):
        with open(file, "r") as f:
            cls._loads(f.read())

    def _tree(cls):
        """Recursive conversion to dictionary"""
        return {k: v if not isinstance(v, MetaConf) else v._tree()
                for k, v in cls.__dict__.items() if k[0] != "_"}


class Conf(metaclass=MetaConf):
    pass


def dumps(cls: MetaConf = None) -> str:
    """Dump a config class to string"""
    if cls is None:
        return config_tree._dumps()
    return cls._dumps()


def dump(file: Union[str, Path], cls: MetaConf = None):
    """Dump a config class to a file"""
    if cls is None:
        config_tree._dump(file)
    else:
        cls._dump(file)


def loads(s: str, cls: MetaConf = None):
    """Load a config from string"""
    if cls is None:
        config_tree._loads()
    else:
        cls._loads(s)


def load(file: Union[str, Path], cls: MetaConf = None):
    """Load a config from a file"""
    if cls is None:
        config_tree._load(file)
    else:
        cls._load(file)


def tree(cls: MetaConf = None) -> dict:
    """Dump a config class to string"""
    if cls is None:
        return config_tree._tree()
    else:
        return cls._tree()


def subconfig_of(over_conf):
    """Decorator used to define dependencies between configurator objects"""

    def subconfig(cls):
        if cls.__name__ in dir(config_tree):
            delattr(config_tree, cls.__name__)
        setattr(over_conf, cls.__name__, cls)
        return cls

    return subconfig


__all__ = ["Conf", "dump", "dump", "loads", "load",
           "subconfig_of", "serializer", "tree", "__version__"]
