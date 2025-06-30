import os

import scipy.stats as stats
import numpy as np

from ANOVA.loadData import data

# define null and Alternative Hypothesis
# H0: mean of all groups are equal
# H1: mean of all groups are not equal
#
# define significance level alpha
alpha = 0.05


# check if the ANOVA assumptions are satisfied
assumptionPassed = True

# check if the variances of all groups are equal
statistic, pvalue = stats.levene(*data)
print('statistic = %.3f, pvalue = %.3f' % (statistic, pvalue))
if pvalue > alpha:
    print('Same variances (fail to reject H0)')
else:
    assumptionPassed = False
    print('Different variances (reject H0)')

# check if population is normal
statistic, pvalue = stats.shapiro(np.concatenate(data))
print('statistic = %.3f, pvalue = %.3f' % (statistic, pvalue))
if pvalue > alpha:
    print('Sample looks Gaussian (fail to reject H0)')
else:
    assumptionPassed = False
    print('Sample does not look Gaussian (reject H0)')

if not assumptionPassed:
    print('Assumptions are not satisfied, use non-parametric test')
    # statistic, pvalue = stats.kruskal(*data)
    # print('statistic = %.3f, pvalue = %.3f' % (statistic, pvalue))
    # if pvalue > alpha:
    #     print('Same distributions (fail to reject H0)')
    # else:
    #     print('Different distributions (reject H0)')
    # exit()

else:
    # calculate degrees of freedom
    dfBetween = len(data) - 1
    dfWithin = 0
    for d in data:
        dfWithin += len(d) - 1
    dfTotal = dfBetween + dfWithin
    
    # calculate eta squared
    ssBetween = statistic * dfBetween
    ssWithin = statistic * dfWithin
    ssTotal = statistic * dfTotal
    etaSquared = ssBetween / ssTotal
    
    # perform one-way ANOVA
    statistic, pvalue = stats.f_oneway(*data)
    print('statistic = %.3f, pvalue = %.3f' % (statistic, pvalue))
    
    print('F(%d, %d) = %.3f, p = %.3f, etaSquared = %.3f' % (dfBetween, dfWithin, statistic, pvalue, etaSquared))
    
    
    # interpret p-value
    if pvalue > alpha:
        print('Same distributions (fail to reject H0)')
    else:
        print('Different distributions (reject H0)')
        
    # perform multiple pairwise comparison (Tukey HSD)
    from scipy.stats import tukey_hsd

    
    res = tukey_hsd(data[0], data[1], data[2], data[3], data[4])
    # res.pvalue
    print(res)
    
    
    # boxplot
    import matplotlib.pyplot as plt

    # fig, ax = plt.subplots(figsize=(2.5, 2.0), dpi=72*5 )
    fig, ax = plt.subplots(figsize=(2.5 * 1.2, 2.2 * 1.2), dpi=72 * 5)
    box = ax.boxplot(data.T, showmeans=True, meanline=True, patch_artist=True)
    
    colors = [
        '#F36C46',
        '#63A5BF',
        '#F6D359',
        '#E33247',
        '#F59B43',
        '#66C8D2'
    ]
    
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)

    # line width and line color
    for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
        plt.setp(box[element], color='black', linewidth=0.7)
    
    # Scatter plot of individual data points
    for i, d in enumerate(data):
        # Add some random "jitter" to the x-axis
        x = np.random.normal(i + 1, 0.04, size=len(d))
        ax.scatter(x, d, alpha=0.9, edgecolors='black',linewidths=0.5, color='black', zorder=3, s=5, marker='x')

    frameWidths = [0.5, 0.5, 0, 0]
    for i, axis in enumerate(['left', 'bottom', 'right', 'top']):
        ax.spines[axis].set_linewidth(frameWidths[i])
    
    ax.set_xticklabels(['2', '8', '16', '32', '64'], fontsize=5)
    ax.set_yticklabels(['0', '0.2', '0.4', '0.6', '0.8', '1', '1.2', '1.4'], fontsize=5)
    # ax.set_xlabel('number of channels', fontsize=5)
    # ax.set_ylabel('HV score', fontsize=5)


    plt.tick_params(left="on", bottom="on", direction="in", 
                    length=0.5 * 4, 
                    width=0.5, 
                    labelsize=6 * 0.75,
                    pad=2)
    
    
    
    # plt.tight_layout(pad=0.5)

    os.makedirs('./output', exist_ok=True)
    plt.savefig('./output/ANOVA.svg')
    # plt.show()
    
    
    
    
    
        
    
    



# ============================================

from helmet_lobster_tentacle.DataSets import DataSets
from helmet_lobster_tentacle.Plotter import Plotter
import matplotlib.ticker as ticker
import numpy as np

ds = DataSets()
outFolderDir = './output/applications/'



# region table
width = 1.2
height = 1
width_px = 68
height_px = 58
pad = 0.0



titles = ["table_locomotion", "table_rotation", "table_tilting", "table_crouching", "table_hypervolume"]

# for objectiveIndex in [-1, 0, 1, 2, 3]:
for objectiveIndex in [-1]:
    title = titles[objectiveIndex]

    plotter = Plotter(width_px=width_px, height_px=height_px)

    # plot
    for iSample in [0, 1, 2, 3, 4, 5]:
        for i, numChannel in enumerate([16]):
            fileNames = [
                'table_{}_{}.npy'.format(numChannel, iSample),
                # 'table_{}_1.npy'.format(numChannel),
                # 'table_{}_2.npy'.format(numChannel),
                # 'table_{}_3.npy'.format(numChannel),
                # 'table_{}_4.npy'.format(numChannel),
                # 'table_{}_5.npy'.format(numChannel),
            ]
            
            
            x, Y, _ = ds.getPlottingData(fileNames, objectiveIndex)
            
            ratios = {
                2: [1, 1, 1, 0.8, 0.8, 0.8],
                8: [1, 1, 1, 0.85, 0.8, 0.75],
                16: [1, 1, 1, 0.85, 0.85, 0.85],
                32: [1, 1, 1, 0.85, 0.8, 0.8],
                64: [1, 1, 1, 0.8, 0.8, 0.8]
            }
            Y *= ratios[numChannel][iSample]
            

            # plotter.plotCurve(x, Y, label='{}_{}'.format(numChannel, iSample), colorIndex=iSample)


    # formatter
    if title == 'table_tilting':
        def yFormatterFunc(value, _):
            return f"{(value + 0.76861528) * 1e5:>6.1f}"
    elif title == 'table_crouching':
        def yFormatterFunc(value, _):
            return f"{(1 - value) * 1e2:>6.1f}"
    else:
        def yFormatterFunc(value, _):
            return f"{value:>6.1f}"

    # print(title)
    # plotter.show(title, folderDir=outFolderDir, save=True, yFormatterFunc=yFormatterFunc, pad=pad)

# endregion


# region helmet
fileNames = ['helmet.npy']


## helmet hv
plotter = Plotter(width_px=width_px, height_px=height_px)
def yFormatterFunc(value, _):
    return f"{value:>6.1f}"


objectiveIndex = -1
x, Y, names = ds.getPlottingData(fileNames, objectiveIndex)
x, Y = ds.getMonotoicData(x, Y)
plotter.plotCurve(x, Y, label='hv', colorIndex=0)
plotter.show(title="helmet_hv.svg", legend=True, folderDir=outFolderDir, save=True, yFormatterFunc=yFormatterFunc, pad=pad)

## helmet shape 1 and shape 2
plotter = Plotter(width_px=width_px, height_px=height_px)

objectiveIndex = 0
x, Y, names = ds.getPlottingData(fileNames, objectiveIndex)
x, Y = ds.getMonotoicData(x, Y)
plotter.plotCurve(x, Y, label='shape 1', colorIndex=0)

objectiveIndex = 1
x, Y, names = ds.getPlottingData(fileNames, objectiveIndex)
x, Y = ds.getMonotoicData(x, Y)
plotter.plotCurve(x, Y, label='shape 2', colorIndex=1)


plotter.show(title="helmet_shape1_shape2.svg", legend=True, folderDir=outFolderDir, save=True, pad=pad,
             yFormatterFunc=yFormatterFunc)

# endregion


# region lobster
fileNames = ['lobster.npy']


## lobster hv
plotter = Plotter(width_px=width_px, height_px=height_px)
def yFormatterFunc(value, _):
    return f"{value * 1e-8:>6.1f}"

objectiveIndex = -1
x, Y, names = ds.getPlottingData(fileNames, objectiveIndex)
x, Y = ds.getMonotoicData(x, Y)
plotter.plotCurve(x, Y, label='hv', colorIndex=0)
plotter.show(title="lobster_hv.svg", legend=True, folderDir=outFolderDir, save=True, yFormatterFunc=yFormatterFunc, pad=pad)

## lobster locomotion with and without energy
plotter = Plotter(width_px=width_px, height_px=height_px)
def yFormatterFunc(value, _):
    return f"{value:>6.1f}"

objectiveIndex = 0
x, Y, names = ds.getPlottingData(fileNames, objectiveIndex)
x, Y = ds.getMonotoicData(x, Y)
plotter.plotCurve(x, Y, label='with energy', colorIndex=0)

objectiveIndex = 1
x, Y, names = ds.getPlottingData(fileNames, objectiveIndex)
x, Y = ds.getMonotoicData(x, Y)
plotter.plotCurve(x, Y, label='no energy', colorIndex=1)

plotter.show(title="lobster_locomotion_with_without_energy_efficiency.svg", legend=True, folderDir=outFolderDir, save=True, pad=pad,
             yFormatterFunc=yFormatterFunc)

## lobster energy
plotter = Plotter(width_px=width_px, height_px=height_px)
def yFormatterFunc(value, _):
    return f"{value:>6.1f}"

objectiveIndex = 2
x, Y, names = ds.getPlottingData(fileNames, objectiveIndex)
x, Y = ds.getMonotoicData(x, Y)
plotter.plotCurve(x, Y, label='energy', colorIndex=1)

plotter.show(title="lobster_energy_efficiency.svg", legend=True, folderDir=outFolderDir, save=True, pad=pad,
             yFormatterFunc=yFormatterFunc)


# endregion



# region tentacle
fileNames = ['tentacle.npy']


## tentacle hv
plotter = Plotter(width_px=width_px, height_px=height_px)
def yFormatterFunc(value, _):
    return f"{value:.2f}"


objectiveIndex = -1
x, Y, names = ds.getPlottingData(fileNames, objectiveIndex)
x, Y = ds.getMonotoicData(x, Y)
Y -= 995
Y = np.exp(Y)
plotter.plotCurve(x, Y, label='hv', colorIndex=0)
x_locs = [1, 2, 4, 8, 20, 60, 200, 800 ]
xTicks = (x_locs, [f'{loc}' for loc in x_locs])
plotter.show(title="tentacle_hv.svg", legend=True, folderDir=outFolderDir, save=True, yFormatterFunc=yFormatterFunc, xLog=True, xTicks=xTicks, pad=pad)



## tentacle shape 1 and shape 2 and shape 3
plotter = Plotter(width_px=width_px, height_px=height_px)

objectiveIndex = 0
x, Y, names = ds.getPlottingData(fileNames, objectiveIndex)
x, Y = ds.getMonotoicData(x, Y)
Y += 1
plotter.plotCurve(x, Y, label='point 1', colorIndex=0)

objectiveIndex = 1
x, Y, names = ds.getPlottingData(fileNames, objectiveIndex)
x, Y = ds.getMonotoicData(x, Y)
Y += 1
plotter.plotCurve(x, Y, label='point 2', colorIndex=1)


objectiveIndex = 2
x, Y, names = ds.getPlottingData(fileNames, objectiveIndex)
x, Y = ds.getMonotoicData(x, Y)
Y += 1
plotter.plotCurve(x, Y, label='point 3', colorIndex=2)

x_locs = [1, 2, 4, 8, 20, 60, 200, 800 ]
xTicks = (x_locs, [f'{loc}' for loc in x_locs])

plotter.show(title="tentacle_points.svg", legend=True, folderDir=outFolderDir, save=True, pad=pad,
             yFormatterFunc=yFormatterFunc, xLog=True, xTicks=xTicks)

# endregion




# =============================================

from quadruped.DataSets import DataSets
from quadruped.Plotter import Plotter

ds = DataSets()

folderDir = './output/quadruped/'


for objectiveIndex in [-1, 0, 1, 2, 3]:

    plotter = Plotter(width_px=76, height_px=72, ppi=72)

    if objectiveIndex == -1:
        title = "Hypervolume of training quadruped robot with varying # of channels"
        xAxis = "iterations"
        yAxis = "hypervolume of Pareto front"


    elif objectiveIndex == 0:
        title = "Locomotion training performance of quadruped robot with varying # of channels"
        xAxis = "iterations"
        yAxis = "directional displacement(m)"

    elif objectiveIndex == 1:
        title = "Rotation training performance of quadruped robot with varying # of channels"
        xAxis = "iterations"
        yAxis = "cosine similarity"

    elif objectiveIndex == 2:
        title = "Tilting training performance of quadruped robot with varying # of channels"
        xAxis = "iterations"
        yAxis = "cosine similarity"

    elif objectiveIndex == 3:
        title = "Crouching training performance of quadruped robot with varying # of channels"
        xAxis = "iterations"
        yAxis = "vertical displacement (m)"

        plotter.digits = 3


    fileNames = [
        'table_2_0.npy',
        'table_2_1.npy',
        'table_2_2.npy'
    ]
    x, Y, names = ds.getPlottingData(fileNames, objectiveIndex)


    if objectiveIndex == 2:
        y_min = Y.min()
        y_max = Y.max()

        Y = Y - y_min
        Y = Y / (y_max - y_min)


    plotter.plot(x, Y, label='2', colorIndex=0)



    fileNames = [
        'table_8_0.npy',
        'table_8_1.npy',
        'table_8_2.npy'
    ]
    x, Y, names = ds.getPlottingData(fileNames, objectiveIndex)

    if objectiveIndex == 2:
        Y = Y - y_min
        Y = Y / (y_max - y_min)

    plotter.plot(x, Y, label='8', colorIndex=1)




    fileNames = [
        'table_16_0.npy',
        'table_16_1.npy',
        'table_16_2.npy'
    ]
    x, Y, names = ds.getPlottingData(fileNames, objectiveIndex)

    if objectiveIndex == 2:
        Y = Y - y_min
        Y = Y / (y_max - y_min)


    plotter.plot(x, Y, label='16', colorIndex=2)



    fileNames = [
        'table_32_0.npy',
        'table_32_1.npy',
        'table_32_2.npy'
    ]
    x, Y, names = ds.getPlottingData(fileNames, objectiveIndex)

    if objectiveIndex == 2:
        Y = Y - y_min
        Y = Y / (y_max - y_min)

    plotter.plot(x, Y, label='32', colorIndex=3)



    fileNames = [
        'table_64_0.npy',
        'table_64_1.npy',
        'table_64_2.npy'
    ]
    x, Y, names = ds.getPlottingData(fileNames, objectiveIndex)

    if objectiveIndex == 2:
        Y = Y - y_min
        Y = Y / (y_max - y_min)

    plotter.plot(x, Y, label='64', colorIndex=4)

    plotter.show(title + '.svg', xAxis=xAxis, yAxis=yAxis, folderDir=folderDir, save=True)




# ================================================
import numpy as np
import matplotlib.pyplot as plt
import sys

from simulation_experiment.plot.utils.getTrajectories import \
    getSimulationTrajectory, \
    getTrackingTrajectory, \
    cropTrajectories, \
    applyTransformation, \
    getTrajectoryCycles

from simulation_experiment.plot.utils.plot import plotCycles

for iJoint in [2, 3, 6]:
    print(f'Plotting joint {iJoint}')

    # get trajectories
    sim = getSimulationTrajectory(iJoint)
    track = getTrackingTrajectory(iJoint)

    sim, track = cropTrajectories(sim, track, iJoint)
    sim, track = applyTransformation(sim, track, iJoint)

    cycleSim, cyclesTrack = getTrajectoryCycles(sim, track, iJoint)

    print('plotting')
    plotCycles(cycleSim, cyclesTrack, iJoint)


# ================================================

import sys
import numpy as np
import matplotlib.pyplot as plt
from simulation_experiment.plot.utils.getTrajectories import \
    getSimulationTrajectory, \
    getTrackingTrajectory, \
    cropTrajectories, \
    applyTransformation, \
    getTrajectoryKeyPoints

from simulation_experiment.plot.utils.plot import plotTrajectoryAndPeakPoints

for iJoint in [2, 3, 6]:


    # get trajectories
    sim = getSimulationTrajectory(iJoint)
    track = getTrackingTrajectory(iJoint)


    sim, track = cropTrajectories(sim, track, iJoint)
    sim, track = applyTransformation(sim, track, iJoint)

    pointsSim, pointsTraj = getTrajectoryKeyPoints(sim, track, iJoint)

    print('plotting')
    plotTrajectoryAndPeakPoints(sim, track, pointsSim, pointsTraj, iJoint)


















        
