import inspect
import uuid


class Manager:
    def __init__(self):
        self._collection = {}

    def add(self, func: 'Function'):
        self._collection[func.id] = func

    def get(self, id):
        return self._collection.get(id)

    def get_all(self):
        return list(self._collection.values())


class Function:
    manager = Manager()

    def __init__(self, func):
        self._func = func
        self.id = uuid.uuid4().hex
        self.name = func.__name__
        self.params = self._get_params(func)
        self.manager.add(self)

    @staticmethod
    def _get_params(func):
        res = []
        allowed_kind = {
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.KEYWORD_ONLY
        }
        for name, parameter in inspect.signature(func).parameters.items():
            parameter: inspect.Parameter
            if parameter.kind in allowed_kind:
                kwargs = dict(name=name)

                if parameter.default is not parameter.empty:
                    kwargs.update(default=parameter.default)

                res.append(Parameter(**kwargs))
        return res

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)

    def __repr__(self):
        return '<Function %s>' % self._func.__qualname__


undefined = object()


class Parameter:
    def __init__(self, name: str, default=undefined):
        self.name = name

        if default is not undefined:
            self.default = default

    @property
    def required(self):
        return not hasattr(self, 'default')
