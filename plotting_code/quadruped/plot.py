from DataSets import DataSets
from Plotter import Plotter

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
