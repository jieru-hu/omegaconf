import re

from pytest import raises

from omegaconf import OmegaConf, DictConfig, ListConfig


def test_repr_list():
    c = OmegaConf.create([1, 2, 3])
    assert "[1, 2, 3]" == repr(c)


def test_is_empty_list():
    c = OmegaConf.create('[1,2,3]')
    assert not c.is_empty()
    c = OmegaConf.create([])
    assert c.is_empty()


def test_list_value():
    c = OmegaConf.create('a: [1,2]')
    assert {'a': [1, 2]} == c


def test_list_of_dicts():
    v = [
        dict(key1='value1'),
        dict(key2='value2')
    ]
    c = OmegaConf.create(v)
    assert c[0].key1 == 'value1'
    assert c[1].key2 == 'value2'


def test_pretty_list():
    c = OmegaConf.create([
        'item1',
        'item2',
        dict(key3='value3')
    ])
    expected = '''- item1
- item2
- key3: value3
'''
    assert expected == c.pretty()
    assert OmegaConf.create(c.pretty()) == c


def test_list_get_with_default():
    c = OmegaConf.create([None, "???", "found"])
    assert c.get(0, 'default_value') == 'default_value'
    assert c.get(1, 'default_value') == 'default_value'
    assert c.get(2, 'default_value') == 'found'


def test_iterate_list():
    c = OmegaConf.create([1, 2])
    items = [x for x in c]
    assert items[0] == 1
    assert items[1] == 2


def test_list_pop():
    c = OmegaConf.create([1, 2, 3, 4])
    assert c.pop(0) == 1
    assert c.pop() == 4
    assert c == [2, 3]
    with raises(IndexError):
        c.pop(100)


def test_in_list():
    c = OmegaConf.create([10, 11, dict(a=12)])
    assert 10 in c
    assert 11 in c
    assert dict(a=12) in c
    assert 'blah' not in c


def test_list_config_with_list():
    c = OmegaConf.create([])
    assert isinstance(c, ListConfig)


def test_list_config_with_tuple():
    c = OmegaConf.create(())
    assert isinstance(c, ListConfig)


def test_items_on_list():
    c = OmegaConf.create([1, 2])
    with raises(AttributeError):
        c.items()


def test_list_enumerate():
    src = ['a', 'b', 'c', 'd']
    c = OmegaConf.create(src)
    for i, v in enumerate(c):
        assert src[i] == v
        assert v is not None
        src[i] = None

    for v in src:
        assert v is None


def test_list_delitem():
    c = OmegaConf.create([1, 2, 3])
    assert c == [1, 2, 3]
    del c[0]
    assert c == [2, 3]
    with raises(IndexError):
        del c[100]


def test_list_len():
    c = OmegaConf.create([1, 2])
    assert len(c) == 2


def test_assign_list_in_list():
    c = OmegaConf.create([10, 11])
    c[0] = ['a', 'b']
    assert c == [['a', 'b'], 11]
    assert isinstance(c[0], ListConfig)


def test_assign_dict_in_list():
    c = OmegaConf.create([None])
    c[0] = dict(foo='bar')
    assert c[0] == dict(foo='bar')
    assert isinstance(c[0], DictConfig)


class IllegalType:
    def __init__(self):
        pass


def test_nested_list_assign_illegal_value():
    with raises(ValueError, match=re.escape("key a[0]")):
        c = OmegaConf.create(dict(a=[None]))
        c.a[0] = IllegalType()


def test_assign_list_in_dict():
    c = OmegaConf.create(dict())
    c.foo = ['a', 'b']
    assert c == dict(foo=['a', 'b'])
    assert isinstance(c.foo, ListConfig)
