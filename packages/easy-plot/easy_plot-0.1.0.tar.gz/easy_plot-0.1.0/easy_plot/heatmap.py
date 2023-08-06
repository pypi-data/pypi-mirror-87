'''
Python module for generating heatmap plots.
'''
import matplotlib.pyplot as plt
import seaborn as sns



def heatmap(df, title='Heatmap', cluster: bool=False) -> None:
    '''
    Display a heatmap for the df arg
    TODO:  Turn into or make separate Hinton diagram too!
    '''
    correlations = df.corr()
    cmap = sns.diverging_palette(220, 20, n=15)  # alternatively, use 'coolwarm'
    if cluster:
        g = sns.clustermap(correlations, annot=True, fmt=',.2f', linewidths=3, cmap=cmap, center=0, dendrogram_ratio=0.15)
    else:
        ax = sns.heatmap(correlations, annot=True, fmt=',.2f', linewidths=3, cmap=cmap, center=0)
        ax.xaxis.tick_top()
        ax.figure.suptitle(title, y=0.96)

    plt.subplots_adjust(left=0.08, right=0.95, bottom=0.08, top=0.84, wspace=0.10)
    plt.show()
