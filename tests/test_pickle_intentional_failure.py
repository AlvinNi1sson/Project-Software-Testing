import hashlib
import pickle


def test_pickle_hash_intentional_failure():
    data = {
        "name": "pickle-test",
        "values": [1, 2, 3],
    }

    pickled_data = pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)
    digest = hashlib.sha256(pickled_data).hexdigest()

    assert digest == "this_is_intentionally_wrong"
