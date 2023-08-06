import boomdiff

## Test suite for boomdiff

# Test initalization of base class
def test_base():
    x = boomdiff.AD(1, {'x1':1})
    assert x.func_val == 1
    print(x.func_val)
    assert x.partial_dict['x1'] == 1
    assert len(x.partial_dict.keys()) == 1

