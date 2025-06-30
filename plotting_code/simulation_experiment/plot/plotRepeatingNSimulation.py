import numpy as np
import matplotlib.pyplot as plt
import sys

from utils.getTrajectories import \
    getSimulationTrajectory, \
    getTrackingTrajectory, \
    cropTrajectories, \
    applyTransformation, \
    getTrajectoryCycles

from utils.plot import plotCycles

iJoint = int(sys.argv[1])

# get trajectories
sim = getSimulationTrajectory(iJoint)
track = getTrackingTrajectory(iJoint)

sim, track = cropTrajectories(sim, track, iJoint)
sim, track = applyTransformation(sim, track, iJoint)

cycleSim, cyclesTrack = getTrajectoryCycles(sim, track, iJoint)

print('plotting')
plotCycles(cycleSim, cyclesTrack, iJoint)



