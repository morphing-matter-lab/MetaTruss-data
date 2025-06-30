# Setup Environment

## Create Conda Environment

```bash
# Create conda environment with Python 3.10
conda create -n metatruss-data python=3.10

# Activate the environment
conda activate metatruss-data

# Install packages from requirements.txt
pip install -r requirements.txt
```


# Generate Plots
## Plotting Code
The plotting code is located in the `plotting_code` directory. To generate all figures, simply run:

```bash
python plot.py
```

This script will automatically call the necessary plotting and dataset reading functions from other folders to generate each figure to the `.output` folder.

# Dataset
All training history data is stored in a single file, `data/training_histories.npy`. All tracked joint trajectories from simulations and experiments are stored as separate `.npy` files in the `data/trajectories/` folder. Each `.npy` file can be loaded in Python using NumPy:

```python
import numpy as np

# for trajectory data
data = np.load('{file_name}.npy', allow_pickle=True)

# for training histories data
data = np.load('data/training_histories.npy', allow_pickle=True).item()
```

## Trajectories Data
Trajectory files are stored as NumPy arrays in the `data/trajectories/` directory. The tracked trajectories from experiments are named `trajectory_{iJoint}.npy` where `iJoint` is 2, 3, or 6. Each file has shape `(n_Frames, 4)`, with columns:
1. x position (pixel) of the tracked joint
2. y position (pixel) of the tracked joint
3. bounding box width (not used in plotting)
4. bounding box height (not used in plotting)

The tracked trajectories from simulations are named `trajectory_simulation_{iJoint}.npy` where `iJoint` is 2, 3, or 6. Each file has shape `(n_Frames, 2)`. The columns have the same meaning as the first two columns of the experiment trajectory files.

## Training Histories Data

The training histories data is stored in the `data/training_histories.npy` file. This file contains a dictionary where each key corresponds to an experiment, named as `helmet.npy`, `tentacle.npy`, `lobster.npy`, or `table_{n_c_networks}_{i_experiment}`. Each value is itself a dictionary with the results for that experiment.

For keys of the form `table_{n_c_networks}_{i_experiment}`, the data represents experiments on the quadruped metatruss robot, where `n_c_networks` is the number of networks used and `i_experiment` is the experiment index.

Each experiment dictionary contains the following fields:
- **objectives**: A list of sub-objective names (e.g., `moveForward`, `turnLeft`, etc.).
- **iters**: A list of iteration indices at which data was captured.
- **scores**: A 2D array of shape `(n_iters, n_subobjectives)`, where each element represents the score of a specific sub-objective at a given iteration (iteration index corresponds to the position in `iters`).
- **hvScores**: A 1D array of length `n_iters`, where each element is the hypervolume score for the corresponding iteration.












