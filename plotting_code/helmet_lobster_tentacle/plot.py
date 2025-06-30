from DataSets import DataSets
from Plotter import Plotter
import matplotlib.ticker as ticker
import numpy as np

ds = DataSets()
outFolderDir = './output/applications/'


width = 1.2
height = 1
width_px = 68
height_px = 58
pad = 0.0


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



