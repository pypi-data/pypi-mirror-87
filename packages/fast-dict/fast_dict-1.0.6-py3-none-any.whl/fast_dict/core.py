import io
import json
from datetime import date, datetime
import jsonpath


class JsonCustomEncoder(json.JSONEncoder):

    def default(self, value):
        if isinstance(value, datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, date):
            return value.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, value)


class Dictionary(dict):

    def __init__(self, seq=None, **kwargs):
        if seq:
            kwargs.update(seq)
        super().__init__(**kwargs)

    def __setattr__(self, key, value):
        """
        eg:
            d = Dictionary()
            d.version = '1.0.0'
            print(d)
        export:
            {'version': '1.0.0'}
        """
        super().__setitem__(key, value)

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)

    def __getattr__(self, name):
        """
        eg:
            d = Dictionary(version='1.0.0', name='Dictionary', branch='dev')
            print(d.version)
        export:
            1.0.0
        """
        value = self.__getitem__(name)
        return value

    def __getitem__(self, name):
        """
        兼容 d.version 赋值后 d['version'] 方式取值问题
        通过 d[k] 方式提取实例属性
        通过 d[k] 方式提取类属性
        """
        value = None
        try:
            value = dict.__getitem__(self, name)
        except KeyError:
            pass
        try:
            value = object.__getattribute__(self, name)
        except AttributeError:
            pass
        return self.__replace__(value)

    def __replace__(self, value):
        """
        对返回的dict类型做处理，返回 Dictionary()
        eg:
            d = Dictionary(version='1.0.0',
                result={
                    'list': [
                        {'product': 'Wine'}
                    ]},
                branch='dev')
            print(d.result.list[0].product)
        export：
            Wine
        """
        if isinstance(value, dict):
            return Dictionary(value)
        elif isinstance(value, list):
            data = []
            for v in value:
                if isinstance(v, dict):
                    v = Dictionary(v)
                data.append(v)
            return data
        else:
            return value

    def json(self, ensure_ascii=False, indent=None):
        """
        返回json字符串
        """
        return json.dumps(self, cls=JsonCustomEncoder, ensure_ascii=ensure_ascii, indent=indent)

    def jsonpath(self, expr):
        """
        使用jsonpath获取values
        jsonpath文档：https://goessner.net/articles/JsonPath/
        eg:
         d = Dictionary(
            {
                'list': [
                    {'product': 'Wine'}
                ]
            }
        )

        print(d.jsonpath('$..product'))
        export：
            Wine
        """
        result = jsonpath.jsonpath(self, expr)

        if result and len(result) == 1:
            result = result[0]

        return self.__replace__(result)

    def exclude(self, exclude_expr=None) -> 'Dictionary':
        """
        排除函数，排除 exclude_expr 中的 (key,value), 返回一个新 Dictionary 实例
        eg:
            d = Dictionary(
                {
                    'list': [
                        {'product': 'Wine'}
                    ],
                    'version': '1.0.0',
                    'name': 'Dictionary'
                }
            )
            new_d = d.exclude(['list', 'name'])
            print(new_d)
        export：
            {'version': '1.0.0'}
        """
        if isinstance(exclude_expr, str):
            exclude_expr = [exclude_expr]
        if isinstance(exclude_expr, (list, tuple)):
            result = Dictionary()
            for k in self:
                if k in exclude_expr:
                    continue
                result[k] = self[k]
            return result
        return self

    def filter(self, filter_expr=None) -> 'Dictionary':
        """
        提取函数，提取 filter_expr 中的 key, 返回一个新的 Dictionary 实例
        eg:
            d = Dictionary(
                {
                    'list': [
                        {'product': 'Wine'}
                    ],
                    'version': '1.0.0',
                    'name': 'Dictionary'
                }
            )
            new_d = d.filter(['version', 'name'])
            print(new_d)
        export：
            {
                'version': '1.0.0',
                'name': 'Dictionary'
            }
        """
        if isinstance(filter_expr, str):
            filter_expr = [filter_expr]
        if isinstance(filter_expr, (list, tuple)):
            result = Dictionary()
            for k in filter_expr:
                if k in self:
                    result[k] = self[k]
            return result
        return self

    def default_filter(self, default: dict) -> 'Dictionary':
        """
        批量筛选，并设置默认值，返回一个新的 Dictionary 实例
        eg:
            d = Dictionary(
                {
                    'list': [
                        {'product': 'Wine'}
                    ],
                    'version': '1.0.0',
                    'name': 'Dictionary'
                }
            )

            new_d = d.default_filter({
                'version': '1.1.0',
                'name': 'a new Dictionary',
                'branch': 'dev'
            })
            print(new_d)
        export:
            {'version': '1.0.0', 'name': 'Dictionary', 'branch': 'dev'}
        """
        result = Dictionary()
        for k, v in default.items():
            if k in self:
                result[k] = self[k]
            else:
                result[k] = v
        return result

    def has(self, k):
        if k in self:
            return True
        return False


def dictionary(seq=None, **kwargs) -> Dictionary:
    return Dictionary(seq, **kwargs)


def load_json(json_file) -> Dictionary:
    with io.open(json_file, "r+", encoding="utf-8") as f:
        return dictionary(json.loads(f.read()))
