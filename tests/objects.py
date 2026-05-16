def recursive_list():
    x = []
    x.append(x)
    return x

def recursive_dict():
    d = {}
    d["self"] = d
    return d

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
        # Primitive types
        "none": None,
        "bool_true": True,
        "bool_false": False,
        "int": 42,
        "large_int": 10**100,

        # Strings / bytes
        "string": "hello",
        "unicode_string": "åäö",
        "bytes": b"hello",

        # Containers
        "empty_list": [],
        "empty_dict": {},
        "tuple": (1, 2, 3),
        "mixed_tuple": (None, True, 42, "hello", b"bytes"),
        "list": [1, 2, 3],
        "nested": {"x": [1, 2, {"y": (3, 4)}]},
        "deeply_nested": [[[[["deep"]]]]],

        # Dictionaries
        "dict_fixed_order": {"a": 1, "b": 2, "c": 3},
        "dict_int_keys": {1: "a", 2: "b", 3: "c"},

        # Sets
        "set_strings": {"a", "b", "c"},
        "set_ints": {1, 2, 3},
        "frozenset_strings": frozenset({"a", "b", "c"}),

        # Floating point edge cases
        "float_zero": 0.0,
        "float_negative_zero": -0.0,
        "float_nan": float("nan"),
        "float_inf": float("inf"),
        "float_negative_inf": float("-inf"),

        # Other builtins
        "complex_number": 3 + 4j,
        "range": range(10),
        "slice": slice(1, 10, 2),

        # Shared references
        "shared_reference": [shared, shared],
        "shared_nested": {"a": shared, "b": shared},

        # Recursive structures
        "recursive_list": recursive_list(),
        "recursive_dict": recursive_dict(),

        # Classes
        "simple_class": SimpleClass(),
        "slot_class": SlotClass(),

        # Exceptions
        "exception_object": ValueError("test error"),
    }