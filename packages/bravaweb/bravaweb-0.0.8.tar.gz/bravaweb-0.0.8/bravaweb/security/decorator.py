
# DECORATE ALL CALLABLE METHODS IN CLASS


def require(decorator):
    def decorate(cls):
        for attr in cls.__dict__:
            if hasattr(getattr(cls, attr), '__call__'):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate
