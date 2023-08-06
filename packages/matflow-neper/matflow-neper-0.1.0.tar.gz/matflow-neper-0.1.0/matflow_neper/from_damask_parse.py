import re
import copy
from pathlib import Path

import numpy as np


def euler2quat(euler_angles):
    """Conver Bunge-convention Eueler angles to unit quaternions.

    Parameters
    ----------
    euler_angles : ndarry of shape (N, 3) of float
        Array of N row three-vectors of Euler angles, specified as proper Euler angles in
        the Bunge convention (rotations are about Z, new X, new new Z).

    Returns
    -------
    quats : ndarray of shape (N, 4) of float
        Array of N row four-vectors of unit quaternions.

    Notes
    -----
    Conversion of Bunge Euler angles to quaternions due to Ref. [1].

    References
    ----------
    [1] Rowenhorst, D, A D Rollett, G S Rohrer, M Groeber, M Jackson,
        P J Konijnenberg, and M De Graef. "Consistent Representations
        of and Conversions between 3D Rotations". Modelling and Simulation
        in Materials Science and Engineering 23, no. 8 (1 December 2015):
        083501. https://doi.org/10.1088/0965-0393/23/8/083501.            

    """

    phi_1 = euler_angles[:, 0]
    Phi = euler_angles[:, 1]
    phi_2 = euler_angles[:, 2]

    sigma = 0.5 * (phi_1 + phi_2)
    delta = 0.5 * (phi_1 - phi_2)
    c = np.cos(Phi / 2)
    s = np.sin(Phi / 2)

    quats = np.array([
        +c * np.cos(sigma),
        -s * np.cos(delta),
        -s * np.sin(delta),
        -c * np.sin(sigma),
    ]).T

    # Move to northern hemisphere:
    quats[quats[:, 0] < 0] *= -1

    return quats


def validate_element_material_idx(element_material_idx):
    num_mats = np.max(element_material_idx) + 1
    emi_range = np.arange(0, num_mats)
    set_diff = np.setdiff1d(emi_range, element_material_idx)
    if set_diff.size:
        msg = (f'The unique values (material indices) in `element_material_idx` '
               f'should form an integer range. This is because the distinct '
               f'materials are defined implicitly through other index arrays in the '
               f'volume element. Found missing material indices:\n{set_diff}')
        raise ValueError(msg)

    return num_mats


def validate_orientations(orientations):
    """Check a set of orientations are valid, optionally with respect to a volume element.

    Parameters
    ----------
    orientations : dict
        Dict containing the following keys:
            type : str
                One of "euler", "quat".
            quaternions : (list or ndarray of shape (R, 4)) of float, optional
                Array of R row four-vectors of unit quanternions. Specify either
                `quaternions` or `euler_angles`.
            euler_angles : (list or ndarray of shape (R, 3)) of float, optional            
                Array of R row three-vectors of Euler angles. Specify either `quaternions`
                or `euler_angles`. Specified as proper Euler angles in the Bunge
                convention (rotations are about Z, new-X, new-new-Z).

    Returns
    -------
    orientations_valid : dict
        Validated orientations where, if orientations were specified as Euler angles in
        `orientations`, they have been converted to quaternions. Dict with the following
        key/values:
            type : str
                Value is "quat".
            quaternions : ndarray of shape (R, 4) of float
                Orientations represented as an array of row 4-vectors.

    """

    # LATER: maybe need to represent as list of list of Decimal instead of float
    # ndarray (should get around 15 dp from float) ?

    ori_type = orientations.get('type')
    eulers = orientations.get('euler_angles')
    quats = orientations.get('quaternions')

    if ori_type not in ['euler', 'quat']:
        msg = f'Specify orientation `type` as either "euler" or "quat".'
        raise ValueError(msg)

    elif ori_type == 'euler':
        if eulers is None:
            msg = (f'Specify orientations as an array of row three-vector Euler angles '
                   f'with the key "euler_angles".')
            raise ValueError(msg)
        euler_angles = np.array(eulers)
        if euler_angles.shape[1] != 3:
            msg = (f'Euler angles specified in "euler_angles" should be a nested list or '
                   f'array of shape (R, 3), but shape passed was: {euler_angles.shape}.')
            raise ValueError(msg)

        # Convert Euler angles to quaternions:
        quaternions = euler2quat(euler_angles)

    elif ori_type == 'quat':
        if quats is None:
            msg = (f'Specify orientations as an array of row four-vector unit '
                   f'quaternions with the key "quaternions".')
            raise ValueError(msg)
        quaternions = np.array(quats)
        if quaternions.shape[1] != 4:
            msg = (f'Quaternions specified in "quaternions" should be a nested list or '
                   f'array of shape (R, 4), but shape passed was: {quaternions.shape}.')
            raise ValueError(msg)

    # TODO: should we check and raise if not normalised?
    norm_factor = np.sqrt(np.sum(quaternions ** 2, axis=1))
    if not np.allclose(norm_factor, 1):
        print('Quaternions are not normalised; they will be normalised.')
        quaternions = quaternions / norm_factor[:, None]

    orientations_valid = {
        'type': 'quat',
        'quaternions': quaternions,
    }

    return orientations_valid


def validate_constituent_material_idx(constituent_material_idx):
    """Check that a constituent_material_idx array (as defined within a volume element)
    is an increasing range starting from zero.

    Parameters
    ----------
    constituent_material_idx : ndarray of shape (N,) of int

    """

    cmi_range = np.arange(0, np.max(constituent_material_idx) + 1)
    if np.setdiff1d(cmi_range, constituent_material_idx).size:
        msg = (f'The unique values (material indices) in `constituent_material_idx` '
               f'should form an integer range. This is because the distinct materials '
               f'are defined implicitly through other index arrays in the volume '
               f'element.')
        raise ValueError(msg)


def get_material_constituent_idx(constituent_material_idx):
    """Get the index array that is the inverse of the constituent_material_idx
    index array.

    Parameters
    ----------
    constituent_material_idx : (list or ndarray of shape (N,)) of int
        Determines the material to which each constituent belongs, where N is the
        number of constituents.

    Returns
    -------
    material_constituent_idx : list of 1D ndarray of variable length of int
        The inverse index array to the input array. The list length will be equal to
        the number of materials.

    """

    validate_constituent_material_idx(constituent_material_idx)
    material_constituent_idx = []
    for mat_idx in np.unique(constituent_material_idx):
        mat_const_idx_i = np.where(np.isin(constituent_material_idx, mat_idx))[0]
        material_constituent_idx.append(mat_const_idx_i)

    return material_constituent_idx


def validate_volume_element(volume_element, phases=None, homog_schemes=None):
    """

    Parameters
    ----------
    volume_element : dict
    phases : dict
    homog_schemes : dict

    Returns
    -------
    volume_element : dict
        Dict with keys:
            constituent_material_idx : ndarray of shape (N,) of int
                Determines the material to which each constituent belongs, where N is the
                number of constituents.
            constituent_material_fraction: ndarray of shape (N,) of float
                The fraction that each constituent occupies within its respective
                material, where N is the number of constituents.
            constituent_phase_label : ndarray of shape (N,) of str
                Determines the phase label of each constituent, where N is the number of
                constituents.
            constituent_orientation_idx : ndarray of shape (N,) of int
                Determines the orientation (as an index into `orientations`) associated
                with each constituent, where N is the number of constituents.
            material_homog : ndarray of shape (M,) of str
                Determines the homogenization scheme (from a list of available
                homogenization schemes defined elsewhere) to which each material belongs,
                where M is the number of materials.
            element_material_idx : ndarray of shape equal to `grid_size` of int, optional
                Determines the material to which each geometric model element belongs,
                where P is the number of elements.
            grid_size : ndarray of shape (3,) of int, optional
                Geometric model grid dimensions.
            orientations : dict, optional
                Dict containing the following keys:
                    type : str
                        Value is "quat".
                    quaternions : ndarray of shape (R, 4) of float, optional
                        Array of R row four-vectors of unit quanternions. Specify either
                        `quaternions` or `euler_angles`.

    """

    volume_element = copy.deepcopy(volume_element)

    ignore_missing_elements = False
    ignore_missing_constituents = False

    if 'element_material_idx' not in volume_element:
        ignore_missing_elements = True
    if 'constituent_material_idx' not in volume_element:
        ignore_missing_constituents = True

    req = [
        'orientations',
        'constituent_material_idx',
        'constituent_phase_label',
        'material_homog',
        'element_material_idx',
        'grid_size',
    ]

    if ignore_missing_elements:
        if ignore_missing_constituents:
            raise ValueError(
                'Cannot ignore both missing elements and missing constituents!')
        req.remove('element_material_idx')
        req.remove('grid_size')

    elif ignore_missing_constituents:
        req.remove('constituent_material_idx')
        req.remove('constituent_phase_label')
        req.remove('material_homog')
        req.append('phase_labels')
        req.append('homog_label')

    if ignore_missing_constituents:
        allowed = list(req)
    else:
        allowed = req + [
            'constituent_material_fraction',  # default value can be set
            'constituent_orientation_idx',    # default value can be set (sometimes)
        ]

    allowed += ['size', 'origin']

    missing = set(req) - set(volume_element)
    if missing:
        missing_fmt = ', '.join([f'"{i}"' for i in missing])
        msg = f'The following volume element keys are missing: {missing_fmt}.'
        raise ValueError(msg)

    unknown = set(volume_element) - set(allowed)
    if unknown:
        unknown_fmt = ', '.join([f'"{i}"' for i in unknown])
        msg = f'The following volume element keys are unknown: {unknown_fmt}.'
        raise ValueError(msg)

    orientations = validate_orientations(volume_element['orientations'])
    volume_element['orientations'] = orientations

    if ignore_missing_constituents:
        # Assuming a full-field model (one constituent per material), set default
        # constituent keys.

        num_mats = validate_element_material_idx(volume_element['element_material_idx'])
        num_oris = orientations['quaternions'].shape[0]
        num_new_phases = num_mats - num_oris

        if num_new_phases != len(volume_element['phase_labels'][1:]):
            msg = (f'Invalid number of phase labels specified; the first phase label '
                   f'should correspond to the elements for which orientations are '
                   f'defined (of which there are {num_oris}), and the remaining phase '
                   f'labels should be used for additional elements (of which there are '
                   f'{num_mats - num_oris}).')
            raise ValueError(msg)

        const_phase_lab = np.array(
            [volume_element['phase_labels'][0]] * num_oris +
            volume_element['phase_labels'][1:]
        )
        additional_oris = np.tile(np.array([1, 0, 0, 0]), (num_new_phases, 1))
        new_oris = np.vstack([orientations['quaternions'], additional_oris])
        mat_homog = np.array([volume_element['homog_label']] * num_mats)

        volume_element['constituent_material_idx'] = np.arange(0, num_mats)
        volume_element['constituent_material_fraction'] = np.ones(num_mats)
        volume_element['constituent_orientation_idx'] = np.arange(0, num_mats)
        volume_element['constituent_phase_label'] = const_phase_lab
        volume_element['orientations']['quaternions'] = new_oris
        volume_element['material_homog'] = mat_homog

        del volume_element['phase_labels']
        del volume_element['homog_label']

    float_arrs = ['constituent_material_fraction']
    int_arrs = [
        'constituent_material_idx',
        'constituent_orientation_idx',
        'element_material_idx',
        'grid_size',
    ]
    str_arrs = [
        'constituent_phase_label',
        'material_homog',
    ]
    arr_keys = float_arrs + int_arrs + str_arrs
    num_const = None
    for key in volume_element:

        # Convert lists to arrays and check dtypes:
        if key in arr_keys:
            new_val = np.array(volume_element[key])
            if key == 'element_material_idx':
                grid_size = volume_element['grid_size']
                if new_val.shape != tuple(volume_element['grid_size']):
                    msg = (f'Volume element key "{key}" should have shape {grid_size}, '
                           f'but has shape: {new_val.shape}.')
                    raise ValueError(msg)
            else:
                if new_val.ndim != 1:
                    msg = (f'Volume element key "{key}" should be a 1D array but has '
                           f'{new_val.ndim} dimensions.')
                    raise TypeError(msg)
            if key in float_arrs:
                if new_val.dtype.char not in np.typecodes['AllFloat']:
                    msg = (f'Volume element key "{key}" should be a float array but has '
                           f'dtype "{new_val.dtype}".')
                    raise TypeError(msg)
            elif key in int_arrs:
                if new_val.dtype.char not in np.typecodes['AllInteger']:
                    msg = (f'Volume element key "{key}" should be an int array but has '
                           f'dtype "{new_val.dtype}".')
                    raise TypeError(msg)
            elif key in str_arrs:
                if new_val.dtype.char not in {'U', 'S'}:
                    msg = (f'Volume element key "{key}" should be a str array but has '
                           f'dtype "{new_val.dtype}".')
                    raise TypeError(msg)
            volume_element[key] = new_val

        # Check all "constituent_*" keys are the same length:
        if key.startswith('constituent_'):
            if num_const is None:
                num_const = volume_element[key].size
            elif volume_element[key].size != num_const:
                msg = (f'Not all "constituent_*" volume element keys are of equal length.'
                       f'Found lengths: {num_const} and {volume_element[key].size}.')
                raise ValueError(msg)

    if 'constituent_orientation_idx' in allowed:
        const_ori_idx = volume_element.get('constituent_orientation_idx')
        if const_ori_idx is None:
            # Set a default `constituent_orientation_idx`. Only possible if number of
            # orientations provided exactly matches number of constituents provided:
            num_oris = orientations['quaternions'].shape[0]
            num_const = volume_element['constituent_material_idx'].shape[0]
            if num_oris != num_const:
                msg = (f'Cannot set default values for `constituent_orientation_idx`, '
                       f'since the number of constituents ({num_const}) does not match '
                       f'the number of orientations ({num_oris}).')
                raise ValueError(msg)
            else:
                volume_element['constituent_orientation_idx'] = np.arange(num_oris)
        else:
            # Remove non-indexed orientations:
            const_ori_idx_uniq, const_ori_idx_inv = np.unique(
                const_ori_idx,
                return_inverse=True
            )
            oris_new = orientations['quaternions'][const_ori_idx_uniq]
            volume_element['orientations']['quaternions'] = oris_new
            volume_element['constituent_orientation_idx'] = const_ori_idx_inv

    # Provide a default `constituent_material_fraction`:
    if 'constituent_material_fraction' in allowed:

        const_mat_idx = volume_element['constituent_material_idx']
        validate_constituent_material_idx(const_mat_idx)

        const_mat_frac = volume_element.get('constituent_material_fraction')
        _, const_mat_idx_inv, const_mat_idx_counts = np.unique(
            const_mat_idx,
            return_inverse=True,
            return_counts=True,
        )
        if const_mat_frac is None:
            # Default is (1 / number of constituents) for each material:
            const_mat_frac = (1 / const_mat_idx_counts)[const_mat_idx_inv]
            volume_element['constituent_material_fraction'] = const_mat_frac
        else:
            # Check constituent fractions sum to one within a material:
            mat_const_idx = get_material_constituent_idx(const_mat_idx)
            for mat_idx, mat_i_const_idx in enumerate(mat_const_idx):
                frac_sum = np.sum(const_mat_frac[mat_i_const_idx])
                if not np.isclose(frac_sum, 1):
                    msg = (f'Constituent fractions must sum to one, but fractions in '
                           f'material {mat_idx} sum to {frac_sum}.')
                    raise ValueError(msg)

    if 'element_material_idx' in req:
        num_elems = volume_element['element_material_idx'].size
        grid_size_prod = np.prod(volume_element['grid_size'])
        if grid_size_prod != num_elems:
            msg = (f'Number of elements in volume element (i.e. size of array '
                   f'`element_material_idx`, ({num_elems}), should match the product of '
                   f'`grid_size` ({volume_element["grid_size"]}, {grid_size_prod}).')
            raise ValueError(msg)

    if 'constituent_material_idx' in req:
        max_mat_idx = np.max(volume_element['constituent_material_idx'])
        num_mats = volume_element['material_homog'].size
        if max_mat_idx != (num_mats - 1):
            msg = (f'Maximum material index in `constituent_material_idx` ({max_mat_idx})'
                   f' does not index into `material_homog` with length {num_mats}.')
            raise ValueError(msg)

    if homog_schemes:
        # Check material homogenization scheme labels exist in `homog_schemes`:
        for mat_idx, mat_i_homog in enumerate(volume_element['material_homog']):
            if str(mat_i_homog) not in homog_schemes:
                msg = (f'Homogenization scheme for material index {mat_idx} '
                       f'("{mat_i_homog}") is not present in `homog_schemes`.')
                raise ValueError(msg)

    if phases:
        # Check constituent phase labels exist in `phases`:
        for const_idx, cons_i_phase in enumerate(volume_element['constituent_phase_label']):
            if str(cons_i_phase) not in phases:
                msg = (f'Phase for constituent index {const_idx} ("{cons_i_phase}") is '
                       f'not present in `phases`.')
                raise ValueError(msg)

    return volume_element
