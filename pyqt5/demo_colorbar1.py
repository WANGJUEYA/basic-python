import matplotlib as mpl
import numpy as np
import pylab as plt

if __name__ == '__main__':
    fig = plt.figure(figsize=(3, 8))
    cmap = mpl.cm.Spectral_r
    ax3 = fig.add_axes([0.3, 0.2, 0.2, 0.5])  # 四个参数分别是左、下、宽、长
    norm = mpl.colors.Normalize(vmin=1.3, vmax=2.5)
    bounds = [round(elem, 2) for elem in np.linspace(1.3, 2.5, 14)]  #
    cb3 = mpl.colorbar.ColorbarBase(ax3, cmap=cmap,
                                    norm=norm,
                                    # to use 'extend', you must
                                    # specify two extra boundaries:
                                    boundaries=[1.2] + bounds + [2.6],
                                    extend='both',
                                    ticks=bounds,  # optional
                                    spacing='proportional',
                                    orientation='vertical')
    plt.show()
