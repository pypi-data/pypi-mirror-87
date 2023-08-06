from logging import DEBUG


class tedasuke:
    def __init__(self, instance, flag: bool):
        self._instance = instance
        self._flag = flag

    def __getattr__(self, name):
        if not self._flag:
            return self._cb
        return getattr(self._instance, name)

    def _cb(self, *args, **kwargs):
        pass
