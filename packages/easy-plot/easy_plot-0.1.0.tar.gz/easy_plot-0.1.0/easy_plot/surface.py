'''
Python module for generating surface plots.
'''
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import matplotlib.animation as animation


def surface(df, scatter_sub_df='', xvar: str='', yvar: str='', zvar: str='', title='Surface Plot', bins=20, minpoints=3, smooth=False, largest_fontsize: int=17, zero_minz=True, show_or_gif: str='show') -> None:
    '''
    Display a surface plot of specified x, y and z columns
    "bins" arg is how many bins to be used in averaging the points.

    optional "scatter_sub_df" kwargs is a filtered dataframe that will plot a subset of 3d points separately from 3d surface calculations
    '''
    x = df[xvar].tolist()
    y = df[yvar].tolist()
    z = df[zvar].tolist()
    plot_x, plot_y, plot_z = zip(*generate_3d_points(list(zip(x, y, z)), bins, minpoints, smooth))

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    surf = ax.plot_trisurf(plot_x, plot_y, plot_z, cmap=plt.cm.viridis, linewidth=0.5, alpha=0.9)
    fig.colorbar(surf, shrink=0.5, aspect=5)

    if len(scatter_sub_df) > 0:
        sub_x = scatter_sub_df[xvar].tolist()
        sub_y = scatter_sub_df[yvar].tolist()
        sub_z = scatter_sub_df[zvar].tolist()
        ax.scatter(sub_x, sub_y, zdir='z', zs=0, s=3, alpha=0.5, color='blue')
        ax.scatter(sub_x, sub_y, zdir='z', zs=sub_z, s=30, alpha=0.2, color='blue')
    else:
        ax.scatter(x, y, zdir='z', zs=0, s=3, alpha=0.5, color='blue')
        ax.scatter(x, y, zdir='z', zs=z, s=30, alpha=0.2, color='blue')

    ax.set_xlabel(f'\n{xvar}', fontsize=0.7 * largest_fontsize, linespacing=2)
    ax.set_ylabel(f'\n{yvar}', fontsize=0.7 * largest_fontsize, linespacing=3)
    ax.set_zlabel(f'\n{zvar}', fontsize=0.7 * largest_fontsize, linespacing=4)

    ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda n, p: '{:,.0f}'.format(n)))
    ax.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda n, p: '{:,.0f}'.format(n)))
    ax.zaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda n, p: '{:,.0f}'.format(n)))

    if zero_minz:
        ax.set_zlim(bottom=0)

    plt.suptitle(title, fontsize=largest_fontsize)
    plt.subplots_adjust(left=0.04, right=1.0, bottom=0.02, top=0.98)

    if show_or_gif == 'gif':
        rotate = lambda angle: ax.view_init(azim=angle, elev=15)
        rot_animation = animation.FuncAnimation(fig, rotate, frames=list(range(-90, -2, 2)) + list(range(-2, -90, -2)), interval=100)
        rot_animation.save('surfaceplot_rotation.gif', dpi=100)
    else:
        plt.show()


def generate_3d_points(coordinates: list, bins: int=10, minpoints: int=7, smooth: bool=False) -> list:
    '''
    First arg is a list of (x, y, z) coordinates.
    This runs through the coordinates, creates x and y bins,
    and averages the z values within the bins.
    Retuns a list of coordinates that can be used to generate a
    clean surface plot (one z value for each x/y zone).
    Set "smooth" == True to smooth surface by pulling in outside points to each bin
    '''
    x, y, z = zip(*coordinates)
    minx, maxx = min(x), max(x)
    miny, maxy = min(y), max(y)
    midx = sorted([abs(n) for n in x])[len(x)//2]  # median
    midy = sorted([abs(n) for n in y])[len(y)//2]  # median

    def magnitude(n):
        return int(math.log10(abs(n)))

    magx = magnitude(midx)
    magy = magnitude(midy)

    # next lines set the lower and upper bounds of the bins on both x & y
    # clever method to round to the nearest number below and above min and max at the current order of magnitude
    # could have issues if variables span several orders of magnitude!!!
    bin_min_x = minx - abs(minx) % 10 ** magx
    bin_max_x = maxx + 10 ** magx - maxx % 10 ** magx
    bin_min_y = miny - abs(miny) % 10 ** magy
    bin_max_y = maxy + 10 ** magy - maxy % 10 ** magy

    bin_size_x = (bin_max_x - bin_min_x) / bins
    bin_size_y = (bin_max_y - bin_min_y) / bins

    average_points = []
    for i in range(bins):
        for j in range(bins):
            if smooth:
                # taking points from current bin, current bin + 1 offset bin, and current bin + 2 offset bins.
                # this significantly smooths the results with heavier weighting to nearer points.
                bin_z_data = [coord[2] for coord in coordinates if
                              coord[0] >= bin_min_x + bin_size_x * i and
                              coord[0] < bin_min_x + bin_size_x * (i + 1) and
                              coord[1] >= bin_min_y + bin_size_y * j and
                              coord[1] < bin_min_y + bin_size_y * (j + 1)]

                bin_z_data.extend([coord[2] for coord in coordinates if
                                   coord[0] >= bin_min_x + bin_size_x * (i - 1) and
                                   coord[0] < bin_min_x + bin_size_x * (i + 2) and
                                   coord[1] >= bin_min_y + bin_size_y * (j - 1) and
                                   coord[1] < bin_min_y + bin_size_y * (j + 2)])

                bin_z_data.extend([coord[2] for coord in coordinates if
                                   coord[0] >= bin_min_x + bin_size_x * (i - 2) and
                                   coord[0] < bin_min_x + bin_size_x * (i + 3) and
                                   coord[1] >= bin_min_y + bin_size_y * (j - 2) and
                                   coord[1] < bin_min_y + bin_size_y * (j + 3)])

            else:
                bin_z_data = [coord[2] for coord in coordinates if
                              coord[0] >= bin_min_x + bin_size_x * i and
                              coord[0] < bin_min_x + bin_size_x * (i + 1) and
                              coord[1] >= bin_min_y + bin_size_y * j and
                              coord[1] < bin_min_y + bin_size_y * (j + 1)]
            try:
                avg_z = sum(bin_z_data) / len(bin_z_data)
                if smooth:
                    if len(bin_z_data) >= minpoints * 3:  # want to have at least a small minimum number of points in an average to accept it
                        average_points.append((bin_min_x + bin_size_x * (i + 0.5), bin_min_y + bin_size_y * (j + 0.5), avg_z))
                else:
                    if len(bin_z_data) >= minpoints:  # want to have at least a small minimum number of points in an average to accept it
                        average_points.append((bin_min_x + bin_size_x * (i + 0.5), bin_min_y + bin_size_y * (j + 0.5), avg_z))
            except ZeroDivisionError:
                pass

    return average_points
