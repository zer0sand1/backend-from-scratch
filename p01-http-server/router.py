class Router:
    def __init__(self):
        self._routes = {}

    # register a route
    def add(self, method, path, handler):
        key = (method.upper(), path)

        self._routes[key] = handler

    # look up a handler
    def match(self, method, path):
        key = (method.upper(), path)

        return self._routes.get(key, None)
