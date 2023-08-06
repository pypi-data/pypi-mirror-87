'`matflow_neper.main.py`'

from matflow_neper import (
    input_mapper,
    output_mapper,
    cli_format_mapper,
    register_output_file,
    func_mapper,
    software_versions,
)
from matflow_neper.utils import tesr_to_volume_element


@output_mapper(
    output_name='volume_element',
    task='generate_volume_element',
    method='random_voronoi'
)
def generate_volume_element_from_random_voronoi(tesr_path, homog_label, phase_label,
                                                buffer_phase_label):

    phase_labels = [phase_label]
    if buffer_phase_label:
        phase_labels.append(buffer_phase_label)

    volume_element = tesr_to_volume_element(tesr_path, phase_labels, homog_label)

    return volume_element


@cli_format_mapper(
    input_name='grid_size',
    task='generate_volume_element',
    method='random_voronoi'
)
def grid_size_formatter(grid_size_list):
    return f'{grid_size_list[0]}:{grid_size_list[1]}:{grid_size_list[2]}'


@cli_format_mapper(
    input_name='buffer_phase_size',
    task='generate_volume_element',
    method='random_voronoi'
)
def buffer_phase_size_formatter(buffer_phase_size_list):
    return (
        f'addbuffer('
        f'{buffer_phase_size_list[0]},'
        f'{buffer_phase_size_list[1]},'
        f'{buffer_phase_size_list[2]})'
    )
