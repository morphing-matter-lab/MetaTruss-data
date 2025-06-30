from DataSets import DataSets
import numpy as np

ds = DataSets()
outFolderDir = './vector_figures/applications/'


# region helmet
fileNames = ['helmet.npy']


objectiveIndex = -1
x, Y, names = ds.getPlottingData(fileNames, objectiveIndex)
x, Y = ds.getMonotoicData(x, Y)

title = 'fig_7e_helmet_hypervolume'
dataDict = {
    'iterations': x.tolist(),
    'hypervolume': Y[0].tolist()
}
with open('source_data/' + title + '.json', 'w') as f:
    import json
    json.dump(dataDict, f, indent=4)


title = 'fig_7d_helmet_shape_1_and_2_performance'
dataDict = {
    'iterations': x.tolist()
}

objectiveIndex = 0
x, Y, names = ds.getPlottingData(fileNames, objectiveIndex)
x, Y = ds.getMonotoicData(x, Y)

dataDict['shape_1_performance'] = Y[0].tolist()

objectiveIndex = 1
x, Y, names = ds.getPlottingData(fileNames, objectiveIndex)
x, Y = ds.getMonotoicData(x, Y)

dataDict['shape_2_performance'] = Y[0].tolist()

with open('source_data/' + title + '.json', 'w') as f:
    import json
    json.dump(dataDict, f, indent=4)

# endregion


# region lobster
fileNames = ['lobster.npy']


objectiveIndex = -1
x, Y, names = ds.getPlottingData(fileNames, objectiveIndex)
x, Y = ds.getMonotoicData(x, Y)

title = 'fig_7g_lobster_hv'
dataDict = {
    'iterations': x.tolist(),
    'hypervolume': Y[0].tolist()
}
with open('source_data/' + title + '.json', 'w') as f:
    import json
    json.dump(dataDict, f, indent=4)



title = 'fig_7h_lobster_walking_distance'

dataDict = {
    'iterations': x.tolist()
}

objectiveIndex = 0
x, Y, names = ds.getPlottingData(fileNames, objectiveIndex)
x, Y = ds.getMonotoicData(x, Y)

dataDict['walking_distance_with_energy_efficiency'] = Y[0].tolist()


objectiveIndex = 1
x, Y, names = ds.getPlottingData(fileNames, objectiveIndex)
x, Y = ds.getMonotoicData(x, Y)

dataDict['walking_distance_without_energy_efficiency'] = Y[0].tolist()

with open('source_data/' + title + '.json', 'w') as f:
    import json
    json.dump(dataDict, f, indent=4)



title = 'fig_7i_lobster_energy_efficiency'
objectiveIndex = 2
x, Y, names = ds.getPlottingData(fileNames, objectiveIndex)
x, Y = ds.getMonotoicData(x, Y)

dataDict = {
    'iterations': x.tolist(),
    'energy_efficiency': Y[0].tolist()
}

with open('source_data/' + title + '.json', 'w') as f:
    import json
    json.dump(dataDict, f, indent=4)


# endregion



# region tentacle
fileNames = ['tentacle.npy']

objectiveIndex = -1
x, Y, names = ds.getPlottingData(fileNames, objectiveIndex)
x, Y = ds.getMonotoicData(x, Y)
Y -= 995
Y = np.exp(Y)

fileName = 'fig_7k_tentacle_hypervolume'

dataDict = {
    'iterations': x.tolist(),
    'hypervolume': Y[0].tolist()
}

with open('source_data/' + fileName + '.json', 'w') as f:
    import json
    json.dump(dataDict, f, indent=4)



fileName = 'fig_7l_tentacle_reaching_three_points'

objectiveIndex = 0
x, Y, names = ds.getPlottingData(fileNames, objectiveIndex)
x, Y = ds.getMonotoicData(x, Y)
Y += 1


dataDict = {
    'iterations': x.tolist(),
    'point_1_performance': Y[0].tolist()
}


objectiveIndex = 1
x, Y, names = ds.getPlottingData(fileNames, objectiveIndex)
x, Y = ds.getMonotoicData(x, Y)
Y += 1

dataDict['point_2_performance'] = Y[0].tolist()

objectiveIndex = 2
x, Y, names = ds.getPlottingData(fileNames, objectiveIndex)
x, Y = ds.getMonotoicData(x, Y)
Y += 1

dataDict['point_3_performance'] = Y[0].tolist()

with open('source_data/' + fileName + '.json', 'w') as f:
    import json
    json.dump(dataDict, f, indent=4)


# endregion



