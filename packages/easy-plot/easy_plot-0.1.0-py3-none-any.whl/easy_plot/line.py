'''
Python module for generating line plots.
'''
import matplotlib.pyplot as plt
import seaborn as sns
import pandas



def line(df, xvar: str='', yvar='', hue: str='', y_label: str='', size_minmax: tuple=(50  , 300), alpha: float=0.9, title='Lineplot', largest_fontsize: int=17, xlog=False, ylog=False, major_gridlines=False, minor_gridlines=False, xlim=[], ylim=[]) -> None:
    '''
    Display a (very nicely formatted) line plot for the df arg.
    Can plot multiple lines if multiple columns are provided as a list for yvar.
    '''
    if type(yvar) == list:
        x = df[xvar].tolist()
        y_values = [(y_val, df[y_val].tolist()) for y_val in yvar]

        data = []
        for y_val, y_value_list in y_values:
            for i in range(len(x)):
                data.append([x[i], y_value_list[i], y_val])
        plot_df = pandas.DataFrame(data, columns=[xvar, 'y_values', 'line_group'])
    else:
        plot_df = df
        plot_df['y_values'] = plot_df[yvar]


    # plot_kwargs = {'x': xvar, 'y': yvar}
    # plot_kwargs['sizes'] = size_minmax
    # if sizevar != '':
        # plot_kwargs['size'] = sizevar
    # else:
        # plot_kwargs['s'] = 200
    # if colorvar != '':
        # plot_kwargs['hue'] = colorvar
        # plot_kwargs['palette'] = 'coolwarm'


    if type(yvar) == list:
        ax = sns.lineplot(data=plot_df, x=xvar, y='y_values', hue='line_group', err_style=None)  #**plot_kwargs, alpha=alpha, legend=False)
    else:
        if hue != '':
            ax = sns.lineplot(data=plot_df, x=xvar, y='y_values', hue=hue, err_style=None)
        else:
            ax = sns.lineplot(data=plot_df, x=xvar, y='y_values', err_style=None)

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles = handles[1:], labels=labels[1:])

    ax.figure.suptitle(title, y=0.96, fontsize=largest_fontsize)
    ax.set_xlabel(xvar, fontsize=largest_fontsize * 0.85)
    if y_label != '':
        ax.set_ylabel(y_label, fontsize=largest_fontsize * 0.85)
    elif type(yvar) == str:
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
