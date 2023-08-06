import numpy as np
import aermanager


def test_is_sorted():
    from aermanager.annotate_aedat import is_sorted
    assert is_sorted(np.array([1, 2, 3, 4, 5]))
    assert not is_sorted(np.array([1, 3, 2, 4, 5]))


def test_lower_bound():

    from aermanager.annotate_aedat import lower_bound

    a = np.array([1, 2, 4, 5, 6])
    b = np.array([1, 5, 10])

    assert np.array_equal(lower_bound(a, b), np.array([0, 3, len(a)-1]))
