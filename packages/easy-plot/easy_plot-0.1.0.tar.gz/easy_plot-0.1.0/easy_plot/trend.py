'''
Python module for generating trend plots.
'''
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns



def trend(df, xvar: str='', yvar: str='', binvar: str='', alpha: float=0.25, title='Trend Plot', largest_fontsize: int=17, xlog=False, ylog=False, major_gridlines=True, minor_gridlines=True, xlim=[0, 10], ylim=[1, 1000]) -> None:
    '''
    Display a trend plot plot for the df arg.
    '''
    lplot_kwargs = {'x': xvar, 'y': yvar}
    lplot_kwargs['linewidth'] = 3
    lplot_kwargs['color'] = 'black'

    groups = set(df[binvar].tolist())
    for group in groups:
        fil = df[df[binvar] == group]
        ax = sns.lineplot(data=fil, **lplot_kwargs, alpha=alpha, legend=False)

    # Calculate and plot average curve ###############################
    sum_curve = []
    count_per_val = []
    max_x = 0
    for group in groups:
        fil = df[df[binvar] == group]
        values = fil[yvar].tolist()
        if len(values) > max_x:
            max_x = len(values)
        for index, val in enumerate(values):
            if len(sum_curve) >= index + 1:
                sum_curve[index] += val
                count_per_val[index] += 1
            else:
                sum_curve.append(val)
                count_per_val.append(1)
    average_curve = [sum / count for sum, count in zip(sum_curve, count_per_val)]
    ax.plot([i for i in range(len(average_curve))], average_curve, color='#444488', alpha=1.0, linewidth=4)
    # ###################################################################

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

    ax.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    plt.subplots_adjust(left=0.08, right=0.95, bottom=0.08, top=0.90, wspace=0.10)
    plt.show()
