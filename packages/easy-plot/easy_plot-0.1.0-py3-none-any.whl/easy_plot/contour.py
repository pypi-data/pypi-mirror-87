'''
Python module for generating contour plots.
'''
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np


def default_label(z):
    return '{:,.1f}'.format(z)


def contour(df, scatter_sub_df='', xvar: str='', yvar: str='', zvar: str='', contour_levels=[], title='Surface Plot', bins=20, largest_fontsize: int=17, major_gridlines=False, minor_gridlines=False, xlim=[], ylim=[], xticks=[], yticks=[], xformat='', yformat='', label_format=default_label, colorbar=True) -> None:
    '''
    Display a contour plot of specified x, y and z columns
    "bins" arg is how many bins to be used in creating contours.

    See: https://matplotlib.org/3.1.1/gallery/images_contours_and_fields/irregulardatagrid.html
    for interpolation code.
    '''
    x = df[xvar].tolist()
    y = df[yvar].tolist()
    z = df[zvar].tolist()


    # create grid values
    xi = np.linspace(min(x), max(x), bins)
    yi = np.linspace(min(y), max(y), bins)

    # Perform linear interpolation of data (x, y) on a grid defined by (xi, yi)
    triang = tri.Triangulation(x, y)
    interpolator = tri.LinearTriInterpolator(triang, z)
    Xi, Yi = np.meshgrid(xi, yi)
    zi = interpolator(Xi, Yi)


    if contour_levels != []:
        contours = plt.contour(xi, yi, zi, levels=contour_levels, cmap=plt.cm.viridis)
    else:
        contours = plt.contour(xi, yi, zi, levels=bins, cmap=plt.cm.viridis) #, linewidth=0.5, alpha=0.9)
    plt.clabel(contours, inline=True, fontsize=0.65 * largest_fontsize, fmt=label_format)

    if colorbar:
        plt.colorbar(contours, shrink=0.7, aspect=3)

    contours.ax.set_xlabel(f'\n{xvar}', fontsize=0.7 * largest_fontsize, linespacing=2)
    contours.ax.set_ylabel(f'\n{yvar}', fontsize=0.7 * largest_fontsize, linespacing=3)

    if xformat == '%':
        contours.ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda n, p: '{:,.0f}%'.format(n * 100)))
    elif xformat == '$':
        contours.ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda n, p: '${:,.2f}'.format(n)))

    if yformat == '%':
        contours.ax.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda n, p: '{:,.0f}%'.format(n * 100)))

    if major_gridlines:
        contours.ax.grid(which='major', linestyle='-', linewidth=1, color='#bbbbbb')
    if minor_gridlines:
        contours.ax.minorticks_on()
        contours.ax.grid(which='minor', linestyle='-', linewidth=0.5, color='#cccccc')

    if xlim != []:
        contours.ax.set_xlim(xlim)
    if ylim != []:
        contours.ax.set_ylim(ylim)

    if xticks != []:
        plt.xticks(xticks)
    if yticks != []:
        plt.yticks(yticks)


    plt.suptitle(title, fontsize=largest_fontsize)
    plt.subplots_adjust(left=0.15, right=0.9, bottom=0.15, top=0.90)
    plt.show()
