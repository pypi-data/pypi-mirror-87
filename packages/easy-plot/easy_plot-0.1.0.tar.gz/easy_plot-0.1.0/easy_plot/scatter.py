'''
Python module for generating scatter plots.
'''
import matplotlib.pyplot as plt
import seaborn as sns



def scatter(df, xvar: str='', yvar: str='', sizevar: str='', colorvar: str='', stylevar: str='', size_minmax: tuple=(50  , 300), alpha: float=0.9, title='Scatterplot', largest_fontsize: int=17, xlog=False, ylog=False, major_gridlines=False, minor_gridlines=False, xlim=[], ylim=[]) -> None:
    '''
    Display a (very nicely formatted) scatter plot for the df arg.
    Can visualize up to 5 variables by optionally using
    point size and/or color for additional dimensions.
    '''
    splot_kwargs = {'x': xvar, 'y': yvar}
    splot_kwargs['sizes'] = size_minmax
    if sizevar != '':
        splot_kwargs['size'] = sizevar
    else:
        splot_kwargs['s'] = 200
    if colorvar != '':
        splot_kwargs['hue'] = colorvar
        splot_kwargs['palette'] = 'coolwarm'


    ax = sns.scatterplot(data=df, **splot_kwargs, alpha=alpha, legend=False)
    ax.figure.suptitle(title, y=0.96, fontsize=largest_fontsize)
    ax.set_xlabel(xvar, fontsize=largest_fontsize * 0.85)
    ax.set_ylabel(yvar, fontsize=largest_fontsize * 0.85)

    if xlog:
        ax.set_xscale('log')
    if ylog:
        ax.set_yscale('log')

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

    plt.subplots_adjust(left=0.08, right=0.95, bottom=0.08, top=0.90, wspace=0.10)
    plt.show()
