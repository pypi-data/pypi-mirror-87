"""Declares decorators to use with FastAPI RESt Framework."""
import functools


def response_model(cls):
    """Decorates a request handler to use the given response model `cls`."""
    def decorator(func):
        func.response_model = cls
        return func
    return decorator


class action:
    """Marks extra methods for routing."""

    def __init__(self, detail=False, name=None, methods=None):
        self.detail = detail
        self.name = name
        self.methods = methods or ['get']

    def __call__(self, func):
        self.name = self.name or func.__name__
        self.func = func
        func.action = self
        return func

    def add_to_app(self, app, base_path, cls):
        """Add the action to the FastAPI application."""
        if self.detail:
            base_path = f'{base_path}/{{pk}}'
        for method in self.methods:
            cls.as_method_handler(app, f'{base_path}/{self.name}',
                method, self.func.__name__)
