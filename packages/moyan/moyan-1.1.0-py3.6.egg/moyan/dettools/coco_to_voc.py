# -*- coding: utf-8 -*-
# Created on 8月-26-20 15:28
# @site: https://github.com/moyans
# @author: moyan
from __future__ import absolute_import
from __future__ import print_function
import cv2
import json
import os
import xml.dom.minidom
from .xml_utils import create_child_node, create_object_node, write_xml_file


COCO_Year = '2020'
AUTHOR = 'Moyan'
SEGMENTED = '0'

def coco2voc(input_json, input_img_dir, output_xml_dir):

    with open(input_json, "r+") as f:
        label_dicts = json.load(f)
        annotations = label_dicts["annotations"]
        categories = label_dicts['categories']
        images = label_dicts['images']

    img2id = {}
    for nn in images:
        img2id[nn['file_name']]= str(nn['id'])

    id2class = {}
    for item in categories:
        id2class[item['id']] = item['name']

    processed_labels = []
    for i in annotations:
        if (i['category_id'] in id2class.keys()):
            processed_labels.append({
                "filename": str(i["image_id"]),
                "name": id2class[i["category_id"]],
                "bndbox": i["bbox"]
            })


    img_list = os.listdir(input_img_dir)
    if img_list == 0:
        print("Do not find images in your img_path")
        os._exit(-1)

    if not os.path.exists(output_xml_dir):
        os.mkdir(output_xml_dir)

    for idx, img_name in enumerate(img_list):
        save_name = img_name[:-4]
        print(idx, save_name)
        xml_file_name = os.path.join(output_xml_dir, (save_name + '.xml'))

        try:
            img = cv2.imread(os.path.join(input_img_dir, img_name))
            height, width, channel = img.shape

            my_dom = xml.dom.getDOMImplementation()
            doc = my_dom.createDocument(None, 'annotation', None)
            root_node = doc.documentElement

            create_child_node(doc, 'folder', input_img_dir, root_node)
            create_child_node(doc, 'filename', img_name, root_node)
            source_node = doc.createElement('source')
            create_child_node(doc, 'database', 'LOGODection', source_node)
            create_child_node(doc, 'annotation', 'COCO' + COCO_Year, source_node)

            create_child_node(doc, 'image', 'flickr', source_node)
            create_child_node(doc, 'flickrid', 'NULL', source_node)
            root_node.appendChild(source_node)
            owner_node = doc.createElement('owner')
            create_child_node(doc, 'flickrid', 'NULL', owner_node)
            create_child_node(doc, 'name', AUTHOR, owner_node)
            root_node.appendChild(owner_node)

            size_node = doc.createElement('size')
            create_child_node(doc, 'width', str(width), size_node)
            create_child_node(doc, 'height', str(height), size_node)
            create_child_node(doc, 'depth', str(channel), size_node)
            root_node.appendChild(size_node)
            create_child_node(doc, 'segmented', SEGMENTED, root_node)

            for label in processed_labels:
                if img2id[img_name] == label["filename"]:
                    object_node = create_object_node(doc, label)
                    root_node.appendChild(object_node)
                    write_xml_file(doc, xml_file_name)
        except AttributeError:
            print('error in {}'.format(os.path.join(input_img_dir, img_name)))



def xywh_to_xyxy(xywh):
    """Convert [x1 y1 w h] box format to [x1 y1 x2 y2] format."""
    if isinstance(xywh, (list, tuple)):
        # Single box given as a list of coordinates
        assert len(xywh) == 4
        x1, y1 = xywh[0], xywh[1]
        x2 = x1 + np.maximum(0., xywh[2] - 1.)
        y2 = y1 + np.maximum(0., xywh[3] - 1.)
        return (x1, y1, x2, y2)
    elif isinstance(xywh, np.ndarray):
        # Multiple boxes given as a 2D ndarray
        return np.hstack(
            (xywh[:, 0:2], xywh[:, 0:2] + np.maximum(0, xywh[:, 2:4] - 1))
        )
    else:
        raise TypeError('Argument xywh must be a list, tuple, or numpy array.')

def xyxy_to_xywh(xyxy):
    """Convert [x1 y1 x2 y2] box format to [x1 y1 w h] format."""
    if isinstance(xyxy, (list, tuple)):
        # Single box given as a list of coordinates
        assert len(xyxy) == 4
        x1, y1 = xyxy[0], xyxy[1]
        w = xyxy[2] - x1 + 1
        h = xyxy[3] - y1 + 1
        return (x1, y1, w, h)
    elif isinstance(xyxy, np.ndarray):
        # Multiple boxes given as a 2D ndarray
        return np.hstack((xyxy[:, 0:2], xyxy[:, 2:4] - xyxy[:, 0:2] + 1))
    else:
        raise TypeError('Argument xyxy must be a list, tuple, or numpy array.')