class Axis:
    def __init__(self, x, data=None, weight=1):
        self.x = x
        self.weight = weight
        self.data = data
        # self.axe = Axes(pl.figure(), np.zeros(4))
        self.attrs = []
        self.axe_2 = None

    def __getattr__(self, item):
        self.attrs.append(dict(fun=item))
        return self.add_attr

    def add_attr(self, *args, **kwargs):
        self.attrs[-1].update(dict(args=args, kwargs=kwargs))

    def second_axe(self, data=None, *args, **kwargs):
        self.axe_2 = Axis(self.x)
        self.axe_2_secondary_yaxis = dict(args=(*args, "right"), kwargs=kwargs)
        if data is not None:
            self.data.extend(data)
        return self.axe_2

    def plot_all(self):
        if self.axe is None:
            raise RuntimeError("Link to figure self.ax is None")

        if self.data is not None:
            for d in self.data:
                print(d.opts["args"], d.opts["kwargs"])
                self.axe.plot(
                    self.x, d, *d.opts["args"], **d.opts["kwargs"],
                )

        if self.axe_2 is not None:
            ax = getattr(self.axe, "secondary_yaxis")(
                *self.axe_2_secondary_yaxis["args"],
                **self.axe_2_secondary_yaxis["kwargs"],
            )

            for calls in self.axe_2.attrs:
                getattr(ax, calls["fun"])(*calls["args"], **calls["kwargs"])

        for calls in self.attrs:
            getattr(self.axe, calls["fun"])(*calls["args"], **calls["kwargs"])
