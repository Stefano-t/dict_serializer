dict_serializer
===============

Simple metaclass to add to and from dict methods to a class.


Usage
-----

.. code:: python

    from dict_serializer import DictSerializer

    class MyClass(metaclass=DictSerializer):
        def __init__(self, param1, param2):
            self.param1 = param1
            self.param2 = param2


Now, the ``MyClass`` class will have two additional methods: ``to_dict`` to
export the class into a dict format; ``from_dict`` that takes a dict as input
and construct a new ``MyClass`` instance.


Customize methods
-----------------

The ``to_dict`` method exposes a ``_pre_serialization`` hook method to customize
the final dict that will be return. The ``from_dict`` method, instead, exposes
``_pre_deserialization`` to craft the input dict before instantiating the 
class. They are useful to customize the behavior of ``to_dict`` and ``from_dict``.
As an example, consider the following:

.. code:: python

    class MyNewClass(metaclass=Dictserializer):
          x1 = 10
          x2 = 20

          def __init__(self, param1):
              self.param1 = param1


    tmp = MyNewClass("param1")
    print(MyNewClass.from_dict(tmp.to_dict()))


This example won't work, since the final dict will have also ``x1`` and ``x2``
as valid parameters, while the ``__init__`` of our toy class only accepts
``param1``. To overcome this issue, we can define our own
``_pre_deserialization`` (note that it is a classmethod):

.. code:: python

   class MyNewClass(metaclass=Dictserializer):
          x1 = 10
          x2 = 20

          def __init__(self, param1):
              self.param1 = param1

          def _pre_deserialization(cls, dict_):
              final_dict = {}
              final_dict["param1"] = dict_["param1"]
              return final_dict

