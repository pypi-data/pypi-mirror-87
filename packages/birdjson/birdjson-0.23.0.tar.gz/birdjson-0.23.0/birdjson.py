import inspect
import re
from datetime import datetime
from types import MappingProxyType
from typing import Any, Union

import inflection
import simplejson as json

__all__ = ['JsonObject', 'KeyConverter', 'GenericObject']


def _attr_is_function(cls, attr):
    return hasattr(cls, attr) and inspect.isfunction(getattr(cls, attr))


class KeyConverter:
    @staticmethod
    def camel(key):
        return inflection.camelize(key, uppercase_first_letter=False)

    @staticmethod
    def Camel(key):
        return inflection.camelize(key, uppercase_first_letter=True)

    @staticmethod
    def snake(key):
        return inflection.underscore(key)

    @staticmethod
    def mongo(key):
        """
        sanitize keys for mongo databases
        - periods become underscores
        - prefix underscore if key starts with $
        """
        if key[0] == '$':
            key = '_' + key
        return re.sub(r'[.$ ]', '_', key)

    @staticmethod
    def sanitize_attr(key):
        """
        sanitize keys to be used as python attributes
        - do not start with a number
        - spaces, dashes, and periods become underscores
        """
        if '0' <= key[0] <= '9':
            key = '_' + key
        return re.sub(r'[^_a-zA-Z0-9]', '_', key)

    @staticmethod
    def all(*converters):
        """Combine multiple converters into one ordered converter"""
        return lambda key: map(lambda conv: conv(key), converters)


_restricted_keys = ['_items_', '_default_factory', '_asdict', '_set_internal']


class GenericObject:

    def __init__(self, default_factory=None, recursive=False, **kwargs):
        object.__setattr__(self, '_items_', dict())
        object.__setattr__(self, '_default_factory', default_factory)
        if recursive:
            object.__setattr__(self, '_default_factory', type(self))

        for k, v in kwargs.items():
            self._items_[k] = _load(v, cls=self.__class__)

    def __call__(self, *args, **kwargs):
        if len(args) == 0:
            raise TypeError('unable to call without an argument supplied')
        fn = getattr(type(self), args[0], None)
        if fn is None:
            raise TypeError(f'method {args[0]} does not exist on type {type(self)}')

        return fn(self, *args[1:], **kwargs)

    def _generate_default(self, key):
        try:
            val = self._default_factory()
            if isinstance(val, GenericObject):
                object.__setattr__(val, '_default_factory', self._default_factory)
        except TypeError:
            val = self._default_factory

        self._items_[key] = val
        return val

    def __getitem__(self, key):
        try:
            _items_ = object.__getattribute__(self, '_items_')
        except AttributeError:
            _items_ = dict()
            object.__setattr__(self, '_items_', _items_)

        if type(key) is int and key < len(self):
            # assuming insertion order, which should be guaranteed in py 3.6/3.7+ (PEP 520)
            return self._items_[list(self._items_.keys())[key]]
        return self.__getattribute__(key)

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __delitem__(self, key):
        if key in self._items_:
            del self._items_[key]

    def __getattribute__(self, key):
        try:
            _items_ = object.__getattribute__(self, '_items_')
        except AttributeError:
            _items_ = dict()
            object.__setattr__(self, '_items_', _items_)

        if key in _items_:
            return _items_[key]

        try:
            return super().__getattribute__(key)
        except AttributeError:
            pass

        try:
            __default = object.__getattribute__(self, '_generate_default')
        except AttributeError:
            object.__setattr__(self, '_generate_default', None)
            return None

        if key not in _restricted_keys:
            return __default(key)

        return None

    def __setattr__(self, key, value):
        self._items_[key] = value

    def __delattr__(self, key):
        if key in self._items_:
            del self._items_[key]

    def __contains__(self, key):
        return key in self._items_

    def __repr__(self):
        return dumps(self)

    def __str__(self):
        return dumps(self)

    def __iter__(self):
        for k, v in self._items_.items():
            yield k, v

    def __len__(self):
        return len(self._items_.keys())

    def __eq__(self, o: object) -> bool:
        # todo: implement equals better
        return str(self) == str(o)

    def keys(self):
        return self._items_.keys()

    def keylist(self):
        return list(self._items_.keys())

    def items(self):
        return self._items_.items()

    def values(self):
        return self._items_.values()

    def valuelist(self):
        return list(self._items_.values())

    def convert_to(self, cls, key_conv=None) -> Any:
        return _load(self, cls=cls, key_conv=key_conv)

    def obj(self, cls=dict, key_conv=None) -> Union[Any, dict]:
        return self.convert_to(cls, key_conv=key_conv)

    def dict(self, key_conv=None) -> Union[Any, dict]:
        return self.convert_to(dict, key_conv=key_conv)

    def get(self, key: str, default=None) -> Any:
        return self[key] if key in self else default

    # @classmethod
    # def recursive(cls):
    #     return cls.with_default_factory(cls)
    #
    # @classmethod
    # def with_default_factory(cls, default_factory):
    #     class Default(cls):
    #
    #         def _get_default(self):
    #             if isinstance(default_factory(), GenericObject):
    #                 return default_factory.with_default_factory(default_factory)
    #             return default_factory()
    #
    #         def __getitem__(self, item):
    #             if item in self._items_:
    #                 return self._items_[item]
    #             self._items_[item] = self._get_default()
    #             return self._items_[item]
    #
    #         def __getattr__(self, item):
    #             if item in self._items_:
    #                 return self._items_[item]
    #
    #             # fix for simplejson
    #             if item == '_asdict':
    #                 return None
    #
    #             self._items_[item] = self._get_default()
    #             return self._items_[item]
    #
    #     return Default()


class JsonObject(GenericObject):
    def json(self, indent=None, separators=None, key_conv=None, **kwargs) -> str:
        return self.dumps(indent=indent, separators=separators, key_conv=key_conv, **kwargs)

    def dumps(self, indent=None, separators=None, key_conv=None, **kwargs) -> str:
        return dumps(self, indent=indent, separators=separators, key_conv=key_conv, **kwargs)

    def pretty(self, indent=2, separators=None, key_conv=None, **kwargs) -> str:
        return self.dumps(indent=indent, separators=separators, key_conv=key_conv, **kwargs)

    def minify(self, key_conv=None, **kwargs):
        return self.dumps(separators=(',', ':'), key_conv=key_conv, **kwargs)

    def camel(self, **kwargs):
        return self.dumps(key_conv=KeyConverter.camel, **kwargs)

    def yaml(self, **kwargs) -> str:
        import birdyaml
        import yaml
        yaml.add_representer(JsonObject, birdyaml._yaml_obj_representer)
        return birdyaml.dumps(self, **kwargs)

    def write_json(self, filename: str, **kwargs):
        with open(filename, 'w') as f:
            f.write(self.json(**kwargs))

    def write_yaml(self, filename: str, **kwargs):
        with open(filename, 'w') as f:
            f.write(self.yaml(**kwargs))


def load_file(filename: str, key_conv=None) -> JsonObject:
    with open(filename) as f:
        return load(f, key_conv=key_conv)


def load(fp, key_conv=None) -> JsonObject:
    return _load(json.load(fp), key_conv=key_conv)


def loads(s: str, key_conv=None) -> JsonObject:
    return _load(json.loads(s), key_conv=key_conv)


def load_obj(obj: Any, cls=JsonObject, key_conv=None) -> JsonObject:
    return _load(obj, cls=cls, key_conv=key_conv)


def dumps(obj: Any, indent=None, key_conv=None, **kwargs) -> str:
    if key_conv is not None and type(key_conv) is not str:
        obj = _load(obj, cls=dict, key_conv=key_conv)
    return json.dumps(obj, indent=indent, default=_json_default_encoder, **kwargs)


def makes(key_conv=None, **kwargs) -> str:
    """Create a json string from arguments"""
    return dumps(_load(kwargs, cls=dict, key_conv=key_conv))


def make(cls=JsonObject, key_conv=None, **kwargs) -> JsonObject:
    """Create a json object from arguments"""
    return _load(kwargs, cls=cls, key_conv=key_conv)


def make_obj(cls, key_conv=None, **kwargs) -> Any:
    return _load(kwargs, cls=cls, key_conv=key_conv)


def make_dict(key_conv=None, **kwargs) -> dict:
    return _load(kwargs, cls=dict, key_conv=key_conv)


def _load(js, cls: Any = JsonObject, key_conv=None) -> Union[JsonObject, Any]:
    if isinstance(js, (list, tuple)):
        return [_load(v, cls=cls, key_conv=key_conv) for v in js]
    elif isinstance(js, MappingProxyType):
        return _load_dict(js.copy(), cls=cls, key_conv=key_conv)
    elif isinstance(js, dict):
        return _load_dict(js, cls=cls, key_conv=key_conv)
    elif isinstance(js, GenericObject):
        return _load_dict(js._items_, cls=cls, key_conv=key_conv)
    elif type(js).__name__ == 'Int64':
        return int(js)  # stupid mongodb Int64
    elif hasattr(js, '__dict__') and len(js.__dict__) > 0:  # ignore __dict__s without elements
        return _load_dict(js.__dict__, cls=cls, key_conv=key_conv)
    return js


def _load_dict(d, cls=JsonObject, key_conv=None) -> Union[JsonObject, Any]:
    if key_conv is None:
        key_conv = str
    obj = cls()
    for key in d:
        obj[key_conv(key)] = _load(d[key], cls=cls, key_conv=key_conv)
    return obj


def _json_default_encoder(o) -> Any:
    if isinstance(o, datetime):
        return str(o)
    elif isinstance(o, MappingProxyType):
        return o.copy()
    elif isinstance(o, set):
        return list(o)
    elif isinstance(o, GenericObject):
        return o._items_
    elif hasattr(o, '__dict__'):
        return o.__dict__
    return str(o)

#
# def _recursive_object(o):
#     return o(default_factory=lambda: _recursive_object(o))


if __name__ == '__main__':
    x = make(y=2, json=3)
    # make sure __setitem__ preserves built-in functions when something overwrites it
    print(x.json)
    # print(x._json())
    x['minify'] = 10
    print(x.minify)
    # print(x._minify())

    from dataclasses import dataclass

    @dataclass
    class TestStuff(JsonObject):
        pass

    t = TestStuff()
    print(t)
    t.x = 5
    t['y'] = 6

    t2 = TestStuff()
    t2['p'] = 6
    print(t2)

    # # make sure __setattr__ preserves built-in functions when something overwrites it
    # assert callable(x.items)
    # x.items = [1, 2, 3, 4]
    # assert not callable(x.items)
    # print(x._items())
    # assert callable(x._items)
    # print('final x:', x)

    assert not callable(x.z)
    x.z = 5
    # Make sure it does not preserve non-callables
    # assert x._z is None

    print(x.yaml())
    # assert x.yaml() == x._yaml()

    js = load_file('tests/config.json')
    print(js)
    print(js.dumps(key_conv=KeyConverter.snake))
    print(js.dumps(key_conv=KeyConverter.mongo))

    print(KeyConverter.sanitize_attr('0.this.is.a-test'))

    j = JsonObject(default_factory=int)
    print(x)
    print(j.x)
    print('1', j['x']+1)
    print('10', j['y']+10)
    j.y += 10
    print('17', j['y']+7)

    # j2 = JsonObject(default_factory=lambda: JsonObject(default_factory=lambda: _recursive_object(JsonObject)))
    # j2 = JsonObject.with_default_factory(JsonObject)
    j2 = JsonObject(recursive=True)
    print('ppop', j2['some']['stupid']['shit']['poop2'])
    j2.some.stupid.shit['poop2'] = 10
    print(j2.some.stupid.shit['poop2'])
    # j2.some.stupid.shit['poop2'].x12 = 12
    j2.some.stupid.shit.poop2 = 15
    print('poop2', j2.some.stupid.shit.poop2)
    # print(j2.some.stupid.shit.poop2 + 1)

    print('simplejson C speedups?', bool(getattr(json, '_speedups', False)))

    pp = JsonObject(recursive=True)
    # pp = JsonObject.recursive()
    # pp = JsonObject.with_default_factory(JsonObject)
    print(pp)
    print(pp['pp2'])
    print(pp['pp2']['pp3'])
    print(pp['pp2']['pp3']['pp4'])

    from pprint import pprint
    pprint(vars(pp.__class__))

    # print(pp._items())
    # print('hasattr', hasattr(pp, 'items'))
    pp('items')

    # print(pp._items)
    print(pp.__class__)
    # print('items' in pp.__class__.__dict__)
    # print(pp.__class__.__dict__['items'])
    # print(pp._items())

    print(pp('pretty'))
    print(pp.pretty())

    pp['pp2']['pp3']['pp4'].x12 = 30
    print(pp['pp2']['pp3']['pp4']('pretty'))
