'''
Python module for generating a histogram.
'''
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns



def histogram(values: list, xvar: str='Values', bins: int=20, title='Histogram', largest_fontsize: int=17, major_gridlines=False, minor_gridlines=False, xlim=[], ylim=[]) -> None:
    '''
    Display a histogram for the df arg.
    '''
    ax = sns.distplot(values, bins=bins, kde=False, rug=True)

    ax.figure.suptitle(title, y=0.96, fontsize=largest_fontsize)
    ax.set_xlabel(xvar, fontsize=largest_fontsize * 0.85)

    ax.set_axisbelow(True)
    if major_gridlines:
        ax.grid(which='major', linestyle='-', linewidth=1, color='#bbbbbb')
    if minor_gridlines:
        ax.minorticks_on()
        ax.grid(which='minor', linestyle='-', linewidth=0.5, color='#cccccc')

    if xlim != []:
        ax.set_xlim(xlim)
    if ylim != []:
        ax.set_ylim(ylim)

    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    plt.subplots_adjust(left=0.08, right=0.95, bottom=0.08, top=0.90, wspace=0.10)
    plt.show()
