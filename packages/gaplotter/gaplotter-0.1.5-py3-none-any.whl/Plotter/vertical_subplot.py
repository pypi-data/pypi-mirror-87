import matplotlib.pyplot as pl
import numpy as np


class VerticalSubPlot:
    def __init__(self, axe_list, title=None, figsize=None, title_kwargs=None, **kwargs):
        vertical_weights = [a.weight for a in axe_list]

        if figsize is None:
            figsize = (8, np.sum(np.array(vertical_weights)) * 3)

        fig, axs = pl.subplots(
            len(vertical_weights),
            1,
            figsize=figsize,
            sharex="all",
            gridspec_kw={"height_ratios": vertical_weights},
            **kwargs,
        )
        # Add the 'real' figures axes to our <Axis> axes
        if not hasattr(axs, "__iter__"):
            axs = [axs]
        self.fig, self.axs = fig, axe_list
        for user_ax, ax in zip(self.axs, axs):
            user_ax.axe = ax

        if title_kwargs is None:
            title_kwargs = {}
        self.set_title(title, **title_kwargs)

    def plot_all(self):
        for a in self.axs:
            a.plot_all()

    def set_title(self, title, **kwargs):
        if title is not None:
            self.fig.suptitle(title, **kwargs)

    def set_xlabel(self, *args, **kwargs):
        self.axs[-1].set_xlabel(*args, **kwargs)
