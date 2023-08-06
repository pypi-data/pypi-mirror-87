import re
import copy
from pathlib import Path

import numpy as np

from matflow_neper.from_damask_parse import validate_volume_element


def read_neper_tess_block(path, block_name):
    """Read a block from a Neper-compatible .tess or .tesr tessellation file.

    Parameters
    ----------
    path : Path or str
        Path to the .tesr or .tess file.

    Returns
    -------
    block_str : str
        Characters from the input file associated with a given Neper data block.

    References
    ----------
    [1] Neper Reference Manual, Romain Quey, 24 November 2020        

    """

    with Path(path).open() as handle:
        file_contents = handle.read()

    # Return empty string if block does not exist:
    if f'*{block_name}' not in file_contents:
        return ''

    # Otherwise, get all lines in the block:
    pattern = r'(?:\*{}\s)([\s\S]+?)(?:\*)'.format(block_name)
    match_group = re.search(pattern, file_contents).groups()[0]
    block_lines = match_group.strip().split('\n')

    return block_lines


def read_neper_tesr(tesr_path):
    """Read a Neper-compatible raster tessellation file (.tesr).

    Parameters
    ----------
    tesr_path : Path or str
        Path to the .tesr file.
    data_starting_index : int, 0 or 1, optional
        Should the returned data array (if included in the .tesr file) be zero- or one-indexed. By default, 0.


    Returns
    -------
    tesr_data : dict
        Dict representing the raster tessellation.

    References
    ----------
    [1] Neper Reference Manual, Romain Quey, 24 November 2020

    """

    # Parse mandatory parameters:
    tesr_format_raw = read_neper_tess_block(tesr_path, 'format')[0].strip().split()
    tesr_general_raw = read_neper_tess_block(tesr_path, 'general')
    tesr_format = {
        'format': float(tesr_format_raw[0]),
        'data_format': tesr_format_raw[1],
    }
    tesr_general = {
        'dimension': int(tesr_general_raw[0]),
        'size': [int(i) for i in tesr_general_raw[1].strip().split()],
        'voxel_size': [float(i) for i in tesr_general_raw[2].strip().split()],
    }
    tesr_data = {
        'format': tesr_format,
        'general': tesr_general,
    }

    # Parse optional parameters:
    OPTIONAL_BLOCK_NAMES = [
        'origin',
        'cell',
        'id',
        'seed',
        'ori',
        'oridist',
        'coo',
        'vol',
        'convexity',
        'crysym',
        'data',
        'oridata',
    ]
    for opt_name in OPTIONAL_BLOCK_NAMES:

        block_lines = read_neper_tess_block(tesr_path, opt_name)
        if not block_lines:
            continue

        if opt_name == 'data':
            # New lines have no significance:
            block = ' '.join(block_lines)
            block = np.array([int(i) for i in block.split()])
            block = np.swapaxes(
                block.reshape(tesr_data['general']['size'][::-1]),
                0,
                2,
            )

        elif opt_name == 'ori':
            # First line is descriptor:
            ori_descriptor = block_lines[0]
            oris = np.array([[float(j) for j in i.split()] for i in block_lines[1:]])
            block = {
                'orientations': oris,
                'descriptor': ori_descriptor,
            }

        elif opt_name == 'cell':
            # Note if we `-transform addbuffer`, number of cells does not increment
            opt_name = 'number_of_cells'
            block = int(block_lines[0])

        else:
            # TODO: add custom parsing for other block names here
            block = block_lines

        tesr_data.update({opt_name: block})

    return tesr_data


def tesr_to_volume_element(tesr_path, phase_labels, homog_label, orientations=None):
    """Read a Neper-compatible raster tessellation file (.tesr) and parse it to a
    volume element.

    Parameters
    ----------
    tesr_path : Path or str
        Path to the .tesr file.
    phase_labels : list or ndarray of str, optional
        List of phase labels to associate with the constituents. The first list element is
        the phase label that will be associated with all of the geometrical elements
        for which an orientation is also specified. Additional list elements are
        phase labels for geometrical elements for which no orientations are
        specified. If the `-transform addbuffer()` option has been used in the creation
        of the .tesr file, additional voxels will be added with index 0 (i.e. void voxels).
        These voxels are those with which an additional phase in `phase_labels` will be
        associated.
    homog_label : str, optional
        The homogenization scheme label to use for all materials in the volume element.        
    orientations : list or ndarray of shape (R, 3) of float
        Euler angles to optionally use instead of those from the .tesr file.

    Returns
    -------
    volume_element : dict    

    """

    tesr_dat = read_neper_tesr(tesr_path)

    if orientations is not None:
        euler_angles = orientations
    else:
        if 'euler-bunge' not in tesr_dat['ori']['descriptor']:
            raise NotImplementedError('Requires euler-bunge Euler angles.')
        euler_angles = tesr_dat['ori']['orientations']

    elem_mat_idx = tesr_dat['data']

    # Set void voxels (0) to end:
    elem_mat_idx[elem_mat_idx == 0] = np.max(elem_mat_idx) + 1

    # Zero-index instead of one-index:
    elem_mat_idx -= 1

    volume_element = {
        'orientations': {
            'type': 'euler',
            'euler_angles': euler_angles,
        },
        'element_material_idx': elem_mat_idx,
        'grid_size': tesr_dat['general']['size'],
        'size': [1, 1, 1],
        'phase_labels': phase_labels,
        'homog_label': homog_label,
    }

    return validate_volume_element(volume_element)


def write_tesr(volume_element, tesr_path):
    """Write a Neper-compatbile .tesr file from a volume element representation.

    Parameters
    ----------
    volume_element : dict
        Dict that represents the specification of a volume element, with keys:
            element_material_idx : ndarray of shape equal to `grid_size` of int, optional
                Determines the material to which each geometric model element belongs,
                where P is the number of elements.
            grid_size : ndarray of shape (3,) of int, optional
                Geometric model grid dimensions.
            size : list of length three, optional
                Volume element size. By default set to unit size: [1.0, 1.0, 1.0].
            origin : list of length three, optional
                Volume element origin. By default: [0, 0, 0].
    tesr_path : str or Path
        The path to the file that will be generated.

    Returns
    -------
    tesr_path : Path
        The path to the generated file.

    """

    volume_element = validate_volume_element(volume_element)
    element_material_idx = volume_element['element_material_idx']
    dimension = 3
    ve_origin = volume_element.get('origin') or [0.0, 0.0, 0.0]
    grid_size = volume_element['grid_size']
    vox_size = [1 / i for i in grid_size]
    num_micros = np.max(element_material_idx) + 1  # element_material_idx is zero-indexed
    cell_idx_one_indexed = ' '.join([f'{i}' for i in range(1, num_micros + 1)])
    ori_descriptor = 'quaternion'
    oris_lines = [''.join([f'{j:>17.12f}' for j in i])
                  for i in volume_element['orientations']['quaternions']]

    data_flat = np.swapaxes(element_material_idx, 0, 2).reshape(-1)
    vox_id_per_line = 20
    num_lines = int(np.ceil(data_flat.size / vox_id_per_line))
    data_lines = []
    for line_index in range(num_lines):
        start_index = line_index * vox_id_per_line
        end_index = (line_index + 1) * vox_id_per_line
        sub_data = data_flat[start_index:end_index]
        data_lines.append(' '.join([f'{i}' for i in sub_data]))

    lines = [
        f'***tesr',
        f' **format',
        f'   2.0 ascii',
        f' **general',
        f'   {dimension}',
        f'   {grid_size[0]} {grid_size[1]} {grid_size[2]}',
        f'   {vox_size[0]:.12f} {vox_size[1]:.12f} {vox_size[2]:.12f}',
        f'  *origin',
        f'   {ve_origin[0]:.12f} {ve_origin[1]:.12f} {ve_origin[2]:.12f}',
        f'  *hasvoid 0',
        f' **cell',  # number of cells (i.e. number of grains)
        f'   {num_micros}',
        f'  *id',
        f'   {cell_idx_one_indexed}',
        f'  *ori',
        f'   {ori_descriptor}'
    ] + oris_lines + [
        f' **data',
    ] + data_lines + [
        f'***end',
    ]

    tesr_path = Path(tesr_path)
    with tesr_path.open('w') as handle:
        handle.write('\n'.join(lines))

    return tesr_path
