# Conpygure

A library to con*py*gure little projects :) 

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

