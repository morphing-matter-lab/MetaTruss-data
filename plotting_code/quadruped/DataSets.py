import numpy as np
import copy

class DataSets:
    def __init__(self):
        self.dataSets = np.load('./data/training_histories.npy', allow_pickle=True).item()
    
    
    def getPlottingData(self, fileNames, indexScore, maxIterLen=1000):
        # fileNames: list of fileNames
            # fileName: e.g. table_2_0.npy
        # indexScore: e.g. 0: first objective, -1: hvScore
        # the function fill all the data and truncate the data with the fewest iterations
        
        iterList = []
        performanceList = []
        
        for fileName in fileNames:
            dataSet = self.dataSets[fileName]
    
            objectives = dataSet['objectives']
            iters = dataSet['iters']
        
            scores = dataSet['scores']  # nIter x nObjectives
            hvScores = dataSet['hvScores'].reshape(-1, 1)   # nIter x 1
            performances = np.hstack([scores, hvScores])  # nIter x (nObjectives + 1)
            
            itersContinuous = np.arange(max(iters) + 1).reshape(-1, 1)
            
            performancesContinuous = []
            iPerformance = 0
            for iter in itersContinuous:
                performancesContinuous.append(performances[iPerformance, indexScore])
                if iter in iters:
                    iPerformance += 1
            
            performancesContinuous = np.array(performancesContinuous)   # nIter x 1
            
            iterList.append(itersContinuous)
            performanceList.append(performancesContinuous)
        
        minIterLen = min(min([len(iters) for iters in iterList]), maxIterLen)
        
        iters = np.arange(minIterLen).reshape(-1)    # nIters
        performanceList = np.array([performances[:minIterLen] for performances in performanceList])   # nSamples x nIters
        
        print(objectives)
        
        objectives = copy.deepcopy(objectives)
        objectiveNames = []
        while len(objectives) > 0:
            subObjectives = objectives.pop(0)
            while len(subObjectives) > 0:
                objectiveNames.append(subObjectives.pop(0))
        
        if indexScore == -1:
            objective = 'hv'
        else:
            objective = objectiveNames[indexScore]
        
        return iters, performanceList, objective
            
        
            
        
        


