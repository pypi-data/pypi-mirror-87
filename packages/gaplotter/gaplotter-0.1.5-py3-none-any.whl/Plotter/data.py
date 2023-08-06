import numpy as np


class Data(np.ndarray):
    # See https://numpy.org/doc/stable/user/basics.subclassing.html
    def __new__(cls, array, *args, **kwargs):
        obj = np.asarray(array).view(cls)
        kwargs.update(dict(markevery=10, linewidth=2))
        obj.opts = dict(args=args, kwargs=kwargs)
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.opts = getattr(obj, "opts", None)

    def update(self, *args, **opts):
        if len(args) > 0:
            self.opts["args"] = args
        self.opts["kwargs"].update(opts)

    def copy(self, **kwargs):
        c = super().copy(**kwargs)
        c.opts = dict(self.opts)
        return c
