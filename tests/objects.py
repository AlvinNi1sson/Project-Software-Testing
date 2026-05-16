def recursive_list():
    x = []
    x.append(x)
    return x


class SimpleClass:
    def __init__(self):
        self.a = 1
        self.b = "hello"


class SlotClass:
    __slots__ = ("x", "y")

    def __init__(self):
        self.x = 1
        self.y = 2


def get_test_objects():
    shared = []
    return {
        "int": 42,
        "large_int": 10**100,
        "string": "hello",
        "bytes": b"hello",
        "tuple": (1, 2, 3),
        "list": [1, 2, 3],
        "dict_fixed_order": {"a": 1, "b": 2, "c": 3},
        "set_strings": {"a", "b", "c"},
        "frozenset_strings": frozenset({"a", "b", "c"}),
        "float_zero": 0.0,
        "float_negative_zero": -0.0,
        "float_nan": float("nan"),
        "float_inf": float("inf"),
        "shared_reference": [shared, shared],
        "recursive_list": recursive_list(),
        "simple_class": SimpleClass(),
        "slot_class": SlotClass(),
    }