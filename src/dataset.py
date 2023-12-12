import numpy as np
import nibabel as nib

def importMatrixFromNIIFile(path, removeEmptySlices = True):
    """
        This function takes a path to a .nii file and returns a 3D matrix

        Args:
            path (str): path to .nii file
            removeEmptySlices (bool): if True, empty slices are removed from the matrix

        Returns:
            matrix (numpy.ndarray): 3D matrix
    """

    np.warnings.filterwarnings('ignore')

    img = nib.load(path)
    data = img.get_fdata()

    if removeEmptySlices:
        data = data[:, :, np.any(data, axis=(0, 1))]
        data = data[:, np.any(data, axis=(0, 2)), :]
        data = data[np.any(data, axis=(1, 2)), :, :]

    matrix = np.where(data > 0, 1, 0)

    return matrix