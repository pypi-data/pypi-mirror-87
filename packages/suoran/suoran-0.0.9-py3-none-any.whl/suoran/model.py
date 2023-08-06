from pkgutil import iter_modules
from importlib import import_module


def collect(module, deep=True):
    '''
    获取指定包及子模块名。
    '''

    name = module.__name__
    result = set([name])
    if deep and module.__loader__.is_package(name):
        for _, child, _ in iter_modules(module.__path__):
            mn = '{}.{}'.format(name, child)
            m = import_module(mn)
            result |= collect(m, deep)
    return result


async def initialize(setting, *modules):
    '''
    初始化。
    '''

    models = set()
    for m in modules:
        models |= collect(m)
    setting['modules']['models'] = models
