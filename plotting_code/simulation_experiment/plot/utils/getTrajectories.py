import numpy as np
import cv2


def getSimulationTrajectory(iJoint):
    vs = np.load('./data/trajectories/trajectory_simulation.npy', allow_pickle=True)

    
    
    iJointTrackToSim = {
        0: 13,
        1: 11,
        2: 1,
        3: 8,
        4: 3,
        5: 9,
        6: 16
    }
    
    iJoint_0 = iJointTrackToSim[iJoint]
    
    sim0 = vs[:, iJoint_0, :]
    sim = np.load('./data/trajectories/trajectory_simulation_{}.npy'.format(iJoint), allow_pickle=True)

    assert((sim0 == sim).all(), "The loaded simulation trajectory does not match the expected trajectory.")


    # remove the second dimension
    simNew = np.zeros([sim.shape[0], 2])
    simNew[:, 0] = sim[:, 0]
    simNew[:, 1] = sim[:, 2]
    sim = simNew
    
    return sim


def getTrackingTrajectory(iJoint):
    print('loading trajectory_{}.npy'.format(iJoint))
    track = np.load('./data/trajectories/trajectory_{}.npy'.format(iJoint), allow_pickle=True)
    print('loaded trajectory_{}.npy'.format(iJoint))
    track = track[:, :2]
    
    return track

def getIFramesAndISteps(iJoint):
    iFrames = np.array([410 + 537 * i for i in np.arange(0, 9)])
    iSteps = np.array([12210 + 15070 * i for i in np.arange(0, 9)])
    
    if iJoint == 2:
        iFrames = np.array([390 + 537 * i for i in np.arange(0, 9)])
    
    if iJoint == 3:
        iFrames = np.array([370 + 537 * i for i in np.arange(0, 9)])
        
    if iJoint == 6:
        iFrames = np.array([390 + 537 * i for i in np.arange(0, 9)])
        
    
    return iFrames, iSteps

def cropTrajectories(sim, track, iJoint):
    iFrames, iSteps = getIFramesAndISteps(iJoint)
    track = track[iFrames[0]:iFrames[-1]+1]
    sim = sim[iSteps[0]:iSteps[-1] +1]
    
    return sim, track

def applyTransformation(sim, track, iJoint):
    
    # flip the y-axis of the tracking trajectory
    track[:, 1] *= -1
    track[:, 0] *= -1
    track = np.array(track, dtype=np.float32)

    
    # smooth out the tracking trajectory
    def smooth_trajectory(trajectory, window_size=10):
        smoothed_trajectory = np.zeros_like(trajectory, dtype=np.float32)
        for i in range(trajectory.shape[0]):
            start = max(0, i - window_size // 2)
            end = min(trajectory.shape[0], i + window_size // 2)
            smoothed_trajectory[i] = np.mean(trajectory[start:end], axis=0)
        
        return smoothed_trajectory
    track = smooth_trajectory(track, window_size=60)
    

    # zero out the starting point of the trajectories
    sim -= sim[0]
    track -= track[0]
    
    if iJoint == 6:
        pts1 = np.float32([
            [0, 0],
            [-26.4, 50.8],
            [293.9, 34.8],
            [406, -18]
        ])
        pts2 = np.float32([
            [0, 0],
            [-26.4, 72.8],
            [340.9, 72.8],
            [392, 3]
        ])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        track = np.array([np.dot(matrix, np.array([x, y, 1])) for x, y in track])
        # reduce dimension
        track = track[:, :2]
        
    
    if iJoint == 2:
        pts1 = np.float32([[0, 0], [400, -100], [400, 0]])
        pts2 = np.float32(
            [[0, 0], [380, -85], [380, 0]])
        
        matrix = cv2.getAffineTransform(pts1, pts2)
        track = np.array([np.dot(matrix, np.array([x, y, 1])) for x, y in track])
        
        track = np.array([[p[0], p[1] + ((1 - p[0] / 400) ** 2 * (p[1] / -100) * -15)] for p in track])
    
    if iJoint == 3:
        pass
    
    # scale tracking trajectory to real world scale
    # track *= 0.0006772215664264255
    sim /=0.0006772215664264255
    
    return sim, track

    
def getTrajectoryKeyPoints(sim, track, iJoint):
    
    iFrames, iSteps = getIFramesAndISteps(iJoint)
    
    pointsSim = sim[iSteps - iSteps[0]]
    pointsTrack = track[iFrames - iFrames[0]]
    
    return pointsSim, pointsTrack



def getTrajectoryCycles(sim, track, iJoint):
    iFrames, iSteps = getIFramesAndISteps(iJoint)
    
    cycleSim = sim[iSteps[0]: iSteps[1]-1]
    cyclesTrack = [track[iFrames[i]: iFrames[i+1]-1] for i in range(len(iFrames) - 1)]
    
    cycleSim[:, 0] -= cycleSim[0, 0]
    for i in range(len(cyclesTrack)):
        cyclesTrack[i][:, 0] -= cyclesTrack[i][0, 0]
    
    return cycleSim, cyclesTrack
    
    

    
    