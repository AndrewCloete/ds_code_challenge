
import hashlib
from typing import List

from timer import time_the_thing


@time_the_thing("list")
def compare_by_list_equality(list_a, list_b):
    assert len(list_a) == len(list_b)
    assert sorted(list_a) == sorted(list_b)

@time_the_thing("set")
def compare_by_set_equality(list_a, list_b):
    assert len(list_a) == len(list_b)
    assert set(list_a) == set(list_b)

@time_the_thing("hash")
def compare_by_hash(list_a, list_b):
    assert len(list_a) == len(list_b)
    def hash_indexes(indexes: List[str]):
        sorted_indexes = sorted(indexes)
        h = hashlib.md5()
        h.update(''.join(sorted_indexes).encode('utf-8'))
        
        return h.hexdigest()

    assert hash_indexes(list_a) == hash_indexes(list_b)

