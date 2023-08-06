'''
Python module for generating a matrix of scatter/other plots.
'''
import matplotlib.pyplot as plt
import seaborn as sns



def scatter_matrix(df, title='Scatterplot Matrix', regression_order=2, alpha: float=0.5) -> None:
    '''Display a scatter plot matrix for the df arg'''
    g = sns.PairGrid(df, diag_sharey=False)

    g.map_diag(sns.kdeplot, lw=3, shade=True)
    g.map_upper(sns.regplot, order=regression_order, scatter_kws={'alpha': alpha, 'color': '#158'}, line_kws={'linewidth': 3, 'color': '#111'})
    g.map_lower(sns.kdeplot, levels=4, cmap='Blues_d')
    g.map_lower(sns.scatterplot, marker='+', color='0.5', alpha=alpha+0.1 if alpha < 0.9 else 1.0)

    g.fig.suptitle(title, y=0.96)
    plt.subplots_adjust(left=0.08, right=0.95, bottom=0.08, top=0.90, wspace=0.10)
    plt.show()
