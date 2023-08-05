
# Decorators Request Methods
from bravaweb.utils import RequestMethod


def TestMethod(required, cls, f, **args):
    if required == cls.enviroment.method:
        return f(cls, **args)
    else:
        return cls.NotAllowed()


def post(f):
    def method_decorator(cls, **args) -> f:
        return TestMethod(RequestMethod.Post, cls, f, **args)
    return method_decorator


def get(f):
    def method_decorator(cls, **args) -> f:
        return TestMethod(RequestMethod.Get, cls, f, **args)
    return method_decorator


def put(f):
    def method_decorator(cls, **args) -> f:
        return TestMethod(RequestMethod.Put, cls, f, **args)
    return method_decorator


def delete(f):
    def method_decorator(cls, **args) -> f:
        return TestMethod(RequestMethod.Delete, cls, f, **args)
    return method_decorator
