"""
Metaclass implementation for a dict serializable class.

This mobule provides a basic metaclass, called ``DictSerializer`` that
automatically adds two methods to (de)serialize a class. The first method is
``to_dict`` and exports only the public fields into a dictionary. While the
second, ``from_dict``, returns a new instance of the class given a valid
dictionary. Both methods internally call hook functions, allowing the
customization of their behavior. In particular, after extracting the dict
dictionary, the ``to_dict`` method calls ``_pre_serialization``, which is a
function that takes a single argument (the dictionary) and returns another
dictionary. The ``from_dict`` method, instead, exposes the
``_pre_deserialization`` method that behaves as before.


Example::

    # Explicitly set the metaclass
    class Hello(metaclass=DictSerializer):
        x = 10
        y = 20

        def __init__(self, name):
            self.name = name

        # Customize the the ``from_dict`` behavior
        def _pre_deserialization(dict_):
            final = {}
            final["name"] = dict_["name"]
            return final

Author::
    Stefano Taverni

Version::
    - 0.1, 18/12/2022
"""


_PRE_SERIALIZATION_NAME = "_pre_serialization"
_PRE_DESERIALIZATION_NAME = "_pre_deserialization"

def _to_dict(obj):
    fields = [(name, getattr(obj, name))
              for name in dir(obj)
              if not name.startswith("_")]
    dict_ = {
        name: attr for (name, attr) in fields
        if not callable(attr)  # remove methods
        and not type(attr) is staticmethod  # remove static methods
        and not type(attr) is classmethod  # remove class methods
    }
    if hasattr(obj, _PRE_SERIALIZATION_NAME):
        dict_ = obj._pre_serialization(dict_)
    return dict_

def _from_dict(cls, dict_):
    if hasattr(cls, _PRE_DESERIALIZATION_NAME):
        dict_ = cls._pre_deserialization(cls, dict_)
    return cls(**dict_)

def _pre_serialization(self, dict_):
    return dict_

def _pre_deserialization(cls, dict_):
    return dict_

class DictSerializer(type):
    def __new__(cls, cls_name, bases, cls_dict):
        cls_dict["to_dict"] = _to_dict
        cls_dict["from_dict"] = classmethod(_from_dict)
        return type(cls_name, bases, cls_dict)
