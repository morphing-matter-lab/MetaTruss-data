import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.colors as colors
import matplotlib.lines as mlines
import matplotlib.ticker as mticker
import matplotlib
import matplotlib.ticker as ticker
import seaborn as sns


fontSize = 5 * 0.75
curveWidth = 0.5 * 0.75
frameWidth = 0.5
tickLength = 1.0
tickWidth = 0.5
tickPad = 1

dpi = 72 * 10
pad = 0.1

def plotTrajectoryAndPeakPoints(sim, track, pointsSim, pointsTrack, iJoint):
    
    sns.set_theme(style="white")
    matplotlib.rcParams['font.family'] = 'sans-serif'
    matplotlib.rcParams['font.sans-serif'] = 'Helvetica Neue'


    ppi = 72

    width_px = 175
    height_px = 55


    width = width_px / ppi
    height = height_px / ppi
    
    plt.figure(figsize=(width, height), dpi=72)


    ax = plt.gca()  # Get the current axes
    
    # plot simulation trajectory
    # downsample
    sim = sim[::100]
    
    points = sim.reshape(-1, 1, 2)
    segments = np.hstack((points[:-1], points[1:]))
    alphas = np.linspace(0, 0.2, len(segments)) ** (1. / 4)
    cs = [colors.to_rgba('#63A5BF', alpha=alpha) for alpha in alphas]
    lc = LineCollection(segments, colors=cs, lw=curveWidth)
    
    
    # region color bar
    # create a color map from a list of colors
    cmap = colors.ListedColormap(cs)
    # Create a ScalarMappable with the colormap
    norm = colors.Normalize(vmin=0, vmax=162)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    
    # colorbar 1
    # cb = plt.colorbar(sm, ax=ax, orientation='horizontal', pad=0.1, shrink=0.3, aspect=20)
    # cb.ax.tick_params(labelsize=fontSize, length=0.5, width=0.2, pad=0.4)
    # cb.set_ticks([0, 80, 162])
    # cb.outline.set_edgecolor('none')
    
    # end region
    
    ax.add_collection(lc)
    
    
    # plot tracking trajectory
    points = track.reshape(-1, 1, 2)
    segments = np.hstack((points[:-1], points[1:]))
    alphas = np.linspace(0, 0.1, len(segments)) ** (1. / 4)
    
    custom_cmap = colors.LinearSegmentedColormap.from_list('custom_gradient', [
        '#F1B807', '#F1B807', '#F36C46', '#F36C46', '#F21365'])
    
    cs = [custom_cmap(i / len(alphas)) for i, alpha in enumerate(alphas)]
    lc = LineCollection(segments, colors=cs, lw=curveWidth, alpha=0.7)
    
    # region color bar
    # create a color map from a list of colors
    cmap = colors.ListedColormap(cs)
    # Create a ScalarMappable with the colormap
    norm = colors.Normalize(vmin=0, vmax=162)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    #

    # colorbar 2
    # cb = plt.colorbar(sm, ax=ax, orientation='horizontal', pad=0.1, shrink=0.3, aspect=20)
    # cb.ax.tick_params(labelsize=fontSize, length=0.5, width=0.2, pad=0.4)
    # cb.set_ticks([0, 80, 162])
    # cb.outline.set_edgecolor('none')
    
    # end region
    

    ax.add_collection(lc)
    
    
    # plot peak points
    sp = plt.scatter(pointsTrack[:, 0], pointsTrack[:, 1], color='#F36C46', s=0.7, alpha=1,
                     label='simulation peak points')
    ep = plt.scatter(pointsSim[:, 0], pointsSim[:, 1], color='#63A5BF', s=0.8, alpha=1, marker='s', label='experiment peak points')
    
    
    plt.axis('equal')
    
    
    orange_line = mlines.Line2D([], [], color='#63A5BF', label='experiment', linewidth=curveWidth)
    blue_line = mlines.Line2D([], [], color='#F36C46', label='simulation', linewidth=curveWidth)
    
    # plt.legend(handles=[orange_line, blue_line, ep, sp], frameon=False, fontsize=fontSize, loc='upper left', bbox_to_anchor=(1, 1))
    
    ax = plt.gca()  # Get the current axes
    
    ax.set_xlim(-60, 410)
    # ax.set_ylim(0, y_length)
    
    frameWidths = [curveWidth] * 4
    
    for i, axis in enumerate(['left', 'bottom', 'right', 'top']):
        ax.spines[axis].set_linewidth(frameWidths[i])
    
    plt.rc('font', family='Arial')
    plt.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True, direction='in', length=tickLength,
                    width=tickWidth, pad=tickPad, labelsize=fontSize)
    
    def custom_format(x, pos):
        return str(x).rjust(4)  # Adjust the format here as needed
    
    
    # plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(custom_format))
    
    # plt.tight_layout(pad=pad)

    os.makedirs('./output/trajectories/', exist_ok=True)
    
    plt.savefig('./output/trajectories/trajectory_{}.svg'.format(iJoint))
    # plt.show()


def plotCycles(cycleSim, cyclesTrack, iJoint):


    sns.set_theme(style="white")
    matplotlib.rcParams['font.family'] = 'sans-serif'
    matplotlib.rcParams['font.sans-serif'] = 'Helvetica Neue'


    ppi = 72

    width_px = 70
    height_px = 59


    width = width_px / ppi
    height = height_px / ppi
    
    plt.figure(figsize=(width, height), dpi=72)

    ax = plt.gca()  # Get the current axes
    
    for i in range(len(cyclesTrack)):
        points = cyclesTrack[i].reshape(-1, 1, 2)
        segments = np.hstack((points[:-1], points[1:]))
        alphas = np.linspace(0, 0.5, len(segments)) ** (1. / 2)
        
        custom_cmap = colors.LinearSegmentedColormap.from_list('custom_gradient', [
            '#F1B807', '#F1B807','#F36C46','#F36C46', '#F21365'])
        
        cs = [custom_cmap(i / len(alphas)) for i, alpha in enumerate(alphas)]
        lc = LineCollection(segments, colors=cs, lw=curveWidth, alpha=0.3)
        ax.add_collection(lc)
    
    # downsample
    cycleSim = cycleSim[::100]
    points = cycleSim.reshape(-1, 1, 2)
    segments = np.hstack((points[:-1], points[1:]))
    alphas = np.linspace(0, 1.0, len(segments)) ** (1)
    cs = [colors.to_rgba('#63A5BF', alpha=alpha) for alpha in alphas]
    lc = LineCollection(segments, colors=cs, lw=curveWidth)
    
    ax.add_collection(lc)
    
    plt.axis('equal')
    
    # plt.xlabel('x (m)', fontsize=fontSize)
    # plt.ylabel('y (m)', fontsize=fontSize)
    # legend
    plt.legend(frameon=False, fontsize=fontSize)
    
    frameWidths = [curveWidth] * 4
    
    for i, axis in enumerate(['left', 'bottom', 'right', 'top']):
        ax.spines[axis].set_linewidth(frameWidths[i])
    
    plt.rc('font', family='Arial')
    plt.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True, direction='in', length=tickLength,
                    width=tickWidth, pad=tickPad, labelsize=fontSize)
    
    # plt.tight_layout(pad=pad)
    
    os.makedirs('./output/trajectories/', exist_ok=True)
    plt.savefig('./output/trajectories/trajectory_cycles_{}.svg'.format(iJoint))
    # plt.show()


