
class Singleton:
    """
    A Non thread safe helper class to for implementing singletons.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Also, the decorated class cannot be
    inherited from.

    To get a singleton instance, use the `instance` method.
    Directly instantiating via `__call__` will raise a `TypeError`.

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self):
        """
        Returns the singleton instance.
        At first call it creates a new instance, every concequent call
        returns the initial object created on first access.
        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singleton must be instantiated using `instance()` method.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)
