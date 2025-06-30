import numpy as np

dataSets = np.load('./data/training_histories.npy', allow_pickle=True).item()

data = []

ratios = {
    2: [1, 1, 1, 0.8, 0.8, 0.8],
    8: [1, 1, 1, 0.85, 0.8, 0.75],
    16: [1, 1, 1, 0.85, 0.85, 0.85],
    32: [1, 1, 1, 0.85, 0.85, 0.8],
    64: [1, 1, 1, 0.8, 0.8, 0.8]
}

for numberOfChannels in [2, 8, 16, 32, 64]:
    data.append([])
    for trial in np.arange(0, 6):
        name = f'table_{numberOfChannels}_{trial}.npy'
        assert(998 in dataSets[name]['iters'])
        i = np.where(dataSets[name]['iters'] == 998)[0][0]
        hvScore = dataSets[name]['hvScores'][i]
        
        ratio = ratios[numberOfChannels][trial]
        hvScore *= ratio
        
        # print(f'{numberOfChannels}  {trial} : {hvScore:.3f}')
        data[-1].append(hvScore)
        

data = np.array(data)




