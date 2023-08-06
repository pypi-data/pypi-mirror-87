# plotting utilities for agnpy
import matplotlib.pyplot as plt

sed_x_label = r"$\nu\,/\,{\rm Hz}$"
sed_y_label = r"$\nu F_{\nu}\,/\,({\rm erg}\,{\rm cm}^{-2}\,{\rm s}^{-1})$"


def plot_sed(nu, sed, ax=None, y_lim=None, **kwargs):
    """plot an SED

    Parameters
    ----------
    nu: :class:`~astropy.units.Quantity`
        frequencies over which the comparison plot has to be plotted
    y_range : list of float
        lower and upper limit of the y axis limt
    comparison_range : list of float
        plot the range over which the residuals were checked 
    """
    ax = plt.gca() if ax is None else ax
    ax.loglog(nu, sed, **kwargs)
    ax.set_xlabel(sed_x_label, fontsize=12)
    ax.set_ylabel(sed_y_label, fontsize=12)
    if y_lim is not None:
        ax.set_y_lim(y_lim)
    if "label" in kwargs:
        ax.legend(fontsize=12)
    plt.show()
    return ax
