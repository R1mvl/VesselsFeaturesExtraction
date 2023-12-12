import numpy as np
from skimage.morphology import skeletonize_3d
from tqdm import tqdm
import plotly.graph_objects as go


def skeletonization(matrix):
    """
        This function takes a 3D matrix and returns a list of coordinates of the skeleton points.

        Args:
            skeleton_matrix (numpy.ndarray): 3D matrix with the skeleton of the input matrix

        Returns:
            skeleton_point (list): list of coordinates of the skeleton points
    """

    pbar = tqdm(total=4, desc="Skeletonization", colour="green",bar_format="{desc:30}: {percentage:3.0f}%|{bar:200}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")
    skeleton_matrix = skeletonize_3d(matrix)
    pbar.update(1)
    skeleton_matrix[skeleton_matrix == 255] = 1
    pbar.update(1)
    skeleton_point_indices = np.argwhere(skeleton_matrix > 0)
    pbar.update(1)
    skeleton_point = skeleton_point_indices.tolist()
    pbar.update(1)
    pbar.close()

    return skeleton_matrix, skeleton_point