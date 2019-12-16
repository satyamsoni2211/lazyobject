from pathlib import Path


class LazyObject(object):
    def __new__(cls, *args, **kwargs):
        print(args, kwargs)
        print(cls.__name__)
        path = Path(args[-1])
        instance = super(LazyObject, cls).__new__(cls)
        instance.path = path
        return instance

    def __init__(self, *args, **kwargs):
        print(kwargs)
        self.encoding = kwargs.get('encoding') or None
        self.errors = kwargs.get('errors') or 'strict'
        self.mode = kwargs.get('mode') or 'r'

    def __getattr__(self, attr):
        if attr == 'read':
            return self.open(mode=self.mode, encoding=self.encoding, errors=self.errors).read
        if hasattr(self.path, attr):
            return getattr(self.path, attr)
        else:
            raise AttributeError(f'No such key {attr}')


a = LazyObject('abc.csv', mode='r', encoding=None, errors='strict')
print(a.read())
print(a.is_file())
