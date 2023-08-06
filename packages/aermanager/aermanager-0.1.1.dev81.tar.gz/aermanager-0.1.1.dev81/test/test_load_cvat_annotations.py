from aermanager.cvat.load_annotations import annotate_polygon_roi, annotate_rectangle_roi, parse_polygon_vertices
from aermanager.cvat.load_labels import load_labels_as_dict

import os
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))

label_file_path = dir_path + '/dummy_labels.json'

def test_load_labels():

    labels = load_labels_as_dict(label_file_path)

    assert labels['__Empty_Default__'] == 0
    assert labels['Pen'] == 1
    assert labels['Rabbit'] == 2
    assert labels['Box'] == 3
    assert labels['Mug'] == 4
    assert labels['Whole_frame_tag_1'] == 5
    assert labels['Whole_frame_tag_2'] == 6


def test_annotate_polygon_roi():
    frame = np.zeros((11, 11))

    # Fill a square of side 6
    vertices = [(0, 0), (6, 0), (6, 6), (0, 6), (0, 0)]

    label = 2
    annotate_polygon_roi(frame, vertices, label)
    assert np.count_nonzero(frame == label) == 36

    section = frame[0:6, 0:6]
    assert np.count_nonzero(section == label) == 36


def test_annotate_rectangle_roi():

    class StubBoundingBox:
        def __init__(self, xtl, ytl, xbr, ybr):
            self.attrib = {'ytl': ytl, 'ybr': ybr, 'xtl': xtl, 'xbr': xbr}

    frame = np.zeros((11, 11))
    bb = StubBoundingBox(0, 0, 6, 6)  # Create a StubBoundingBox of area 36

    label = 2
    annotate_rectangle_roi(frame, bb, label)
    assert np.count_nonzero(frame == label) == 36

    section = frame[0:6, 0:6]
    assert np.count_nonzero(section == label) == 36


def test_parse_polygon_vertices():
    vertices_str = "0,1;2,3;4,5"
    
    vertices = parse_polygon_vertices(vertices_str)

    assert isinstance(vertices, list)

    assert len(vertices) == 3
    assert vertices[0] == (0,1)
    assert vertices[1] == (2,3)
    assert vertices[2] == (4,5)

def test_parse_polygon_vertices_float():
    vertices_str = "0.3,1.9;2.3,3.4;4.0,5.1"
    
    vertices = parse_polygon_vertices(vertices_str)

    assert isinstance(vertices, list)

    assert len(vertices) == 3
    assert vertices[0] == (0,1)
    assert vertices[1] == (2,3)
    assert vertices[2] == (4,5)