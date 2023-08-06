from importlib import import_module
from functools import partial, update_wrapper


class Router:
    '''
    路由器类
    '''

    def __init__(self, module):
        '''
        初始化。
        '''

        self.module = module
        self.actions = []

    def route(self, app):
        '''
        添加路由到应用。
        '''

        for cn, n, uri, args, kwargs in self.actions:
            if cn != None:
                controller_class = getattr(self.module, cn)
                controller = controller_class()
                method = getattr(controller_class, n)
                handler = partial(method, controller)
                update_wrapper(handler, method)
                app.add_route(handler, uri, *args, **kwargs)
            else:
                handler = getattr(self.module, n)
                app.add_route(handler, uri, *args, **kwargs)

    def append(
        self,
        class_name,  # 类名
        method_name,  # 方法名
        uri,  # 路由 URI
        args,  # 路由 数组参数
        kwargs  # 路由 键值参数
    ):
        '''
        存储路由参数。
        '''

        self.actions.append((
            class_name,
            method_name,
            uri,
            args,
            kwargs
        ))


def action(uri,  *args, **kwargs):
    '''
    路由信息设置。
    '''

    def decorator(method):
        '''
        装饰器。
        '''

        n = method.__name__
        qn = method.__qualname__
        cn = qn[:-len(n) - 1] if qn != n else None
        mn = method.__module__
        m = import_module(mn)
        if not hasattr(m, '___router___'):
            setattr(m, '___router___', Router(m))
        m.___router___.append(cn, n, uri, args, kwargs)
        return method
    return decorator


def any(uri, *args, **kwargs):
    '''
    接受所有方法类型。
    '''

    kwargs['methods'] = [
        'HEAD',
        'GET',
        'POST',
        'PUT',
        'DELETE',
        'CONNECT',
        'OPTIONS',
        'TRACE',
        'PATCH',
    ]
    return action(uri, *args, **kwargs)


def get(uri,  *args, **kwargs):
    '''
    接受 GET 请求。
    '''

    kwargs['methods'] = ['GET']
    return action(uri, *args, **kwargs)


def put(uri,  *args, **kwargs):
    '''
    接受 PUT 请求。
    '''

    kwargs['methods'] = ['PUT']
    return action(uri, *args, **kwargs)


def delete(uri,  *args, **kwargs):
    '''
    接受 DELETE 请求。
    '''

    kwargs['methods'] = ['DELETE']
    return action(uri, *args, **kwargs)


def post(uri,  *args, **kwargs):
    '''
    接受 POST 请求。
    '''

    kwargs['methods'] = ['POST']
    return action(uri, *args, **kwargs)
