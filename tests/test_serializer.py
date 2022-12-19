from dict_serializer import DictSerializer


def test_serializer():
    class Tmp(metaclass=DictSerializer):
        def __init__(self, param1, param2):
            self.param1 = param1
            self.param2 = param2

    tmp = Tmp("test", 1)

    assert hasattr(tmp, "to_dict")
    assert hasattr(tmp, "from_dict")
    assert not hasattr(tmp, "_pre_serializer")
    assert not hasattr(tmp, "_pre_deserializer")

    got = tmp.to_dict()
    assert got == {"param1": "test", "param2": 1}

    new_tmp = Tmp.from_dict({"param1": "test2", "param2": 2})
    assert new_tmp.param1 == "test2"
    assert new_tmp.param2 == 2

def test_serializer_override_methods():
    class Tmp(metaclass=DictSerializer):
        def __init__(self, param1, param2):
            self.param1 = param1
            self.param2 = param2

        def _pre_serialization(self, dict_):
            dict_["added"] = -1
            return dict_

        def _pre_deserialization(cls, dict_):
            dict_["param2"] = dict_["param2"] * 10
            return dict_

    tmp = Tmp("test", 1)

    got = tmp.to_dict()
    assert got["added"] == -1

    new_tmp = Tmp.from_dict({"param1": None, "param2": 1})
    assert new_tmp.param2 == 10
