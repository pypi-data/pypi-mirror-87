from aermanager.cvat.load_labels import load_labels_as_dict

from lxml import etree

import numpy as np
import math


def annotate_polygon_roi(frame: np.ndarray, vertices: list, label):
    assert len(frame.shape) == 2, "Frame must be two dimensional!"
    
    from skimage.draw import polygon

    poly = np.array(vertices)
    rr, cc = polygon(poly[:, 1], poly[:, 0], frame.shape)
    frame[rr, cc] = label


def annotate_rectangle_roi(frame: np.ndarray, bounding_box, label):
    # The rectangle case is kept separate since we can use numpy
    # directly. We don't have to go through scikit-image to
    # draw the polygon and perform the ray-cast algorithm.

    # Parse rows values of vertices and bound check values.

    ytl = math.floor(float(bounding_box.attrib['ytl']))
    ybr = math.ceil(float(bounding_box.attrib['ybr']))

    ytl = ytl if ytl < frame.shape[0] else (frame.shape[0] - 1)
    ybr = ybr if ybr < frame.shape[0] else (frame.shape[0] - 1)

    # Parse columns values of vertices and bound check values.

    xtl = math.floor(float(bounding_box.attrib['xtl']))
    xbr = math.ceil(float(bounding_box.attrib['xbr']))

    xtl = xtl if xtl < frame.shape[1] else (frame.shape[1] - 1)
    xbr = xbr if xbr < frame.shape[1] else (frame.shape[1] - 1)

    frame[ytl:ybr, xtl:xbr] = label


def parse_polygon_vertices(polygon_points: str):
    vertices = polygon_points.split(';')

    def parse_coordinates(vertex):
        coords = vertex.split(',')
        assert len(coords) == 2, "Polygon vertices must be two dimensional!"
        return (int(float(coords[0])), int(float(coords[1])))

    return [parse_coordinates(vertex) for vertex in vertices]


def load_annotations(annotation_file: str, cvat_labels_file: str):
    root = etree.parse(annotation_file)

    labels_lut = load_labels_as_dict(cvat_labels_file)

    tasks = root.xpath('//task')

    assert len(
        tasks) == 1, 'Currently only one annotation task per video file is supported!'

    length = int(tasks[0].find('size').text)
    width = int(tasks[0].find('original_size').find('width').text)
    height = int(tasks[0].find('original_size').find('height').text)

    annotations = np.zeros((length, height, width), dtype='uint8')

    for tracked_object in root.xpath('track'):
        label = labels_lut[tracked_object.attrib['label']]
        # id = tracked_object.attrib['id']

        for bouding_box in tracked_object.xpath('box'):
            frame = int(bouding_box.attrib['frame'])
            annotate_rectangle_roi(annotations[frame],
                                   bouding_box,
                                   label)

        for poly in tracked_object.xpath('polygon'):
            frame = int(poly.attrib['frame'])
            annotate_polygon_roi(annotations[frame],
                                 parse_polygon_vertices(poly.attrib['points']),
                                 label)

    return annotations