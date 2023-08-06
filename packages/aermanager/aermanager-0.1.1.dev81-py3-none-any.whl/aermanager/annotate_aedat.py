from aermanager.cvat.load_annotations import load_annotations
from aermanager.dataset_generator import dataset_content_generator

import numpy as np


def is_sorted(vct: np.ndarray):
    return np.all(vct[:-1] <= vct[1:])


def lower_bound(vct: np.ndarray, elements: np.ndarray):
    assert len(vct.shape) == 1, "vct array should be 1-dimensional!"
    assert is_sorted(vct), "vct array must be sorted!"
    assert isinstance(vct, np.ndarray) , "vct must be a np.ndarray type!"
    assert isinstance(elements, np.ndarray), "elements must be a np.ndarray type!"

    indexes = np.searchsorted(vct, elements, side='left')
    indexes[indexes == len(vct)] -= 1

    return indexes


def annotate_events(sliced_xytp: np.ndarray, annotations: np.ndarray):
    t_min = sliced_xytp[0]['t'][0]
    t_max = sliced_xytp[-1]['t'][-1]

    assert t_max > t_min, "The time interval for the given sliced_xytp is negative!"

    annotation_frames_num = annotations.shape[0]

    assert annotation_frames_num != 0, "The number of annotated frames is zero!"

    annotations_timebins = np.linspace(t_min, t_max, num=annotation_frames_num)

    def labels_of(slice):
        return annotations[lower_bound(annotations_timebins, slice['t']), slice['y'], slice['x']]

    return [labels_of(events_slice) for events_slice in sliced_xytp]


def aedat_load_annotated(aedat_file: str, annotations_file: str, labels_file: str, **kwargs):
    annotations = load_annotations(annotations_file, labels_file)
    sliced_xytp, frames, bins = dataset_content_generator(aedat_file, **kwargs)
    return sliced_xytp, frames, annotate_events(sliced_xytp, annotations)
