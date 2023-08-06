"""Standardized orientation among different libraries.

Various libraries have different ways to interpret information read from various image formats (Dicom, NIfTi, etc)
Here, we standardize the orientation for this framework.

We indicate how to translate reading/writing orientations from current libraries (Nibabel, PyDicom, etc)

Orientation Conventions:
-------------------------
- All orientations are in patient voxel coordinates - i.e. (i, j, k) --> voxel at numpy array position [i, j, k]
- Left: corresponds to patient (not observer) left, RIGHT: corresponds to patient (not observer) right

Standard Orientation format:
----------------------------
All directions point to the increasing direction - i.e. from -x to x
- "LR": left to right; "RL": right to left
- "PA": posterior to anterior; "AP": anterior to posterior
- "IS": inferior to superior; "SI": superior to inferior

Affine Matrix format:
---------------------
The affine matrix (A) is formatted in nibabel.affine matrix format following the standard orientation format above
The affine matrix converts pixel coordinates (i, j, k) into world (NIfTI) coordinates (x, y, z)

[x, y, z, 1]' = A * [i, j, k, 1]'

e.g.:

| x |       [  0.        ,   0.        ,   1.5       , -61.66970062]     | i |
| y |   =   [ -0.3125    ,   0.        ,   0.        ,  50.85160065]  *  | j |
| z |       [  0.        ,  -0.3125    ,   0.        ,  88.58760071]     | k |
| 1 |       [  0.        ,   0.        ,   0.        ,   1.        ]     | 1 |

Attributes:
    SAGITTAL (tuple[str]): Image orientation for sagittal scans.
    CORONAL (tuple[str]): Image orientation for coronal scans.
    AXIAL (tuple[str]): Image orientation for axial scans.
"""

__all__ = ["get_transpose_inds", "get_flip_inds", "orientation_nib_to_standard", "orientation_standard_to_nib",
           "SAGITTAL", "CORONAL", "AXIAL"]


SAGITTAL = ('SI', 'AP', 'LR')
CORONAL = ('SI', 'LR', 'AP')
AXIAL = ('AP', 'LR', 'SI')

__EXPECTED_ORIENTATION_TUPLE_LEN__ = 3
__SUPPORTED_ORIENTATIONS__ = ['LR', 'RL', 'PA', 'AP', 'IS', 'SI']
__ORIENTATIONS_TO_AXIS_ID__ = {'LR': 0, 'RL': 0,
                               'PA': 1, 'AP': 1,
                               'IS': 2, 'SI': 2}


def __check_orientation__(orientation: tuple):
    """Check if orientation tuple defines a valid orientation.

    Args:
        orientation (tuple[str]): Image orientation in standard orientation format.

    Raises:
        ValueError: If orientation tuple is invalid.
    """
    is_orientation_format = len(orientation) == __EXPECTED_ORIENTATION_TUPLE_LEN__ and sum(
        [type(o) is str for o in orientation]) == __EXPECTED_ORIENTATION_TUPLE_LEN__

    orientation_str_exists = sum(
        [o in __SUPPORTED_ORIENTATIONS__ for o in orientation]) == __EXPECTED_ORIENTATION_TUPLE_LEN__

    orientation_ids = [__ORIENTATIONS_TO_AXIS_ID__[o] for o in orientation]
    unique_ids = len(orientation_ids) == len(set(orientation_ids))

    if not is_orientation_format or not orientation_str_exists or not unique_ids:
        raise ValueError("Orientation format mismatch: Orientations must be tuple of strings of "
                         "length {}".format(__EXPECTED_ORIENTATION_TUPLE_LEN__))


def get_transpose_inds(curr_orientation: tuple, new_orientation: tuple):
    """Get indices for transposing orientation axes to format volume in different plane.

    i.e. sagittal <--> axial, sagittal <--> coronal, coronal <--> axial

    Args:
        curr_orientation (tuple[str]): Current image orientation.
        new_orientation (tuple[str]): New image orientation.

    Returns:
        tuple[int]: Axes to transpose to change orientation.
    """
    __check_orientation__(curr_orientation)
    __check_orientation__(new_orientation)

    curr_orientation_ids = [__ORIENTATIONS_TO_AXIS_ID__[o] for o in curr_orientation]
    new_orientation_ids = [__ORIENTATIONS_TO_AXIS_ID__[o] for o in new_orientation]

    if set(curr_orientation_ids) != set(new_orientation_ids):
        raise ValueError("Orientation mismatch: Both curr_orientation and new_orientation must contain the same axes")

    transpose_inds = [curr_orientation_ids.index(n_o) for n_o in new_orientation_ids]

    return tuple(transpose_inds)


def get_flip_inds(curr_orientation: tuple, new_orientation: tuple):
    """Get indices for flipping orientation around axis - i.e. x --> -x, y --> -y, z --> -z.

    Args:
        curr_orientation (tuple[str]): Current image orientation.
        new_orientation (tuple[str]): New image orientation.

    Returns:
        list[int]: Axes in volume to flip.

    Raises:
        ValueError: If mismatch in orientation indices. To avoid this error, apply transpose prior to flipping.
    """
    __check_orientation__(curr_orientation)
    __check_orientation__(new_orientation)

    curr_orientation_ids = [__ORIENTATIONS_TO_AXIS_ID__[o] for o in curr_orientation]
    new_orientation_ids = [__ORIENTATIONS_TO_AXIS_ID__[o] for o in new_orientation]

    if curr_orientation_ids != new_orientation_ids:
        raise ValueError('All axis orientations (S/I, L/R, A/P) must be in the same location in tuple')

    flip_axs_inds = []
    for i in range(__EXPECTED_ORIENTATION_TUPLE_LEN__):
        if curr_orientation[i] != new_orientation[i]:
            flip_axs_inds.append(i)

    return flip_axs_inds


# Nibabel to standard orientation conversion utils.
__nib_to_standard_orientation_map__ = {'R': 'LR', 'L': 'RL',
                                       'A': 'PA', 'P': 'AP',
                                       'S': 'IS', 'I': 'SI'}


def orientation_nib_to_standard(nib_orientation):
    """Convert Nibabel orientation to the standard orientation format.

    Args:
        nib_orientation: a RAS+ tuple orientation used by Nibabel.

    Returns:
        tuple[str]: Image orientation in the standard orientation format.
    """
    orientation = []
    for symb in nib_orientation:
        orientation.append(__nib_to_standard_orientation_map__[symb])
    return tuple(orientation)


def orientation_standard_to_nib(orientation):
    """Convert standard orientation format to Nibabel orientation.

    Args:
        orientation: Image orientation in the standard orientation format.

    Returns:
        tuple[str]: RAS+ tuple orientation used by Nibabel.
    """
    nib_orientation = []
    for symb in orientation:
        nib_orientation.append(symb[1])
    return tuple(nib_orientation)
