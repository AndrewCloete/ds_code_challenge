
import hashlib
from typing import List

def compare_by_list_equality(list_a, list_b):
    assert len(list_a) == len(list_b)
    return sorted(list_a) == sorted(list_b)

def compare_by_set_equality(list_a, list_b):
    assert len(list_a) == len(list_b)
    return set(list_a) == set(list_b)

def compare_by_hash(list_a, list_b):
    assert len(list_a) == len(list_b)
    def hash_indexes(indexes: List[str]):
        sorted_indexes = sorted(indexes)
        h = hashlib.md5()
        h.update(''.join(sorted_indexes).encode('utf-8'))
        
        return h.hexdigest()

    return hash_indexes(list_a) == hash_indexes(list_b)

