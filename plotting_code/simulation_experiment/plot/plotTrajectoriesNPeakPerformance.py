import sys
import numpy as np
import matplotlib.pyplot as plt
from utils.getTrajectories import \
    getSimulationTrajectory, \
    getTrackingTrajectory, \
    cropTrajectories, \
    applyTransformation, \
    getTrajectoryKeyPoints

from utils.plot import plotTrajectoryAndPeakPoints


iJoint = int(sys.argv[1])

# get trajectories
sim = getSimulationTrajectory(iJoint)
track = getTrackingTrajectory(iJoint)


sim, track = cropTrajectories(sim, track, iJoint)
sim, track = applyTransformation(sim, track, iJoint)

pointsSim, pointsTraj = getTrajectoryKeyPoints(sim, track, iJoint)

print('plotting')
plotTrajectoryAndPeakPoints(sim, track, pointsSim, pointsTraj, iJoint)



# sample sim with the exact same number of points as track
iSteps = np.array(np.arange(len(track)) / len(track) * len(sim), dtype=int)
sim = sim[iSteps]

# calculate average L2 distance between sim and track
L2 = np.linalg.norm(sim - track, axis=1)
L2 = np.mean(L2)
# 2: 3.84
# 3: 3.64
# 6: 3.83
# mean: 3.77


# calculate peak performance L2 distance
d = np.linalg.norm(pointsSim - pointsTraj, axis=0).mean()


# 2: 1.76
# 3: 1.217
# 6: 2.3
# mean: 1.76



















    