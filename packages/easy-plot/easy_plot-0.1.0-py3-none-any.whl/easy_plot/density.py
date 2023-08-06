'''
Python module for generating density plots.
'''
import matplotlib.pyplot as plt
import seaborn as sns



def density(df, xvar, categoryvar: str='', x_label: str='', y_label: str='', show_rug: bool=False, size_minmax: tuple=(50  , 300), alpha: float=0.9, title='Densityplot', largest_fontsize: int=17, xlog=False, major_gridlines=False, minor_gridlines=False, xlim=[], ylim=[]) -> None:
    '''
    Display a density plot for the xvar arg (string or iterable of strings).
    '''
    colors = sns.color_palette(n_colors=len(set(df[categoryvar])) if categoryvar else 10)
    if type(xvar) == str:
        if categoryvar == '':
            ax = sns.kdeplot(df[xvar], shade=True)
            if show_rug:
                ax.plot(df[xvar], [0.0] * len(df), '|', color=colors[0])
        else:
            categories = sorted(set(df[categoryvar]))
            counter = 0
            plotted_categories = []
            for cat in categories:
                fil = df[df[categoryvar] == cat]
                if len(fil) > 1:
                    ax = sns.kdeplot(fil[xvar], shade=True)
                    plotted_categories.append(cat)
                    if show_rug:
                        ax.plot(fil[xvar], [0.0] * len(fil), '|', color=colors[counter])
                        counter += 1
                else:
                    print(f'Error plotting {cat} since at least two points are needed!')
            label_list = [t for t in ax.get_legend_handles_labels()]
            ax.legend(handles=label_list[0], labels=plotted_categories)
    else:
        for i, var in enumerate(xvar):
            ax = sns.kdeplot(df[var], shade=True)
            if show_rug:
                ax.plot(df[var], [0.0] * len(df), '|', color=colors[i])

    ax.figure.suptitle(title, y=0.96, fontsize=largest_fontsize)
    if x_label != '':
        ax.set_xlabel(xvar, fontsize=largest_fontsize * 0.85)
    if y_label != '':
        ax.set_ylabel(y_label, fontsize=largest_fontsize * 0.85)

    ax.set_yticks([])
    if xlog:
        ax.set_xscale('log')

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
