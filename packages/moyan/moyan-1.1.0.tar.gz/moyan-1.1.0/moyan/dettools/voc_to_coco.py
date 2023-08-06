# -*- coding: utf-8 -*-
# Created on 8月-26-20 14:45
# @site: https://github.com/moyans
# @author: moyan
import os
import json
import xml.etree.ElementTree as ET

def readTxt2Lines(txt_file_path):
    with open(txt_file_path, 'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        return lines

def writeLines2Txt(lines, name):
    f = open(name, 'w')
    temp = ''
    for idx, name in enumerate(lines):
        if idx == len(lines)-1:
            temp += name
        else:
            temp += name + '\n'
    f.write(temp)
    f.close()

coco = dict()
coco['images'] = []
coco['type'] = 'instances'
coco['annotations'] = []
coco['categories'] = []

category_set = dict()
image_set = set()

category_item_id = 0
image_id = 20200000000
annotation_id = 0

voc_txt_lines = []

# coco['categories'] = [{'supercategory': 'none', 'id': 1, 'name': 'person'}, ]
# category_set = {'person': 1,}


def addCatItem(name):
    global category_item_id
    category_item = dict()
    category_item['supercategory'] = 'none'
    category_item_id += 1
    category_item['id'] = category_item_id
    category_item['name'] = name
    coco['categories'].append(category_item)
    category_set[name] = category_item_id
    return category_item_id


def addImgItem(file_name, size):
    global image_id
    if file_name is None:
        raise Exception('Could not find filename tag in xml file.')
    if size['width'] is None:
        raise Exception('Could not find width tag in xml file.')
    if size['height'] is None:
        raise Exception('Could not find height tag in xml file.')
    image_id += 1
    image_item = dict()
    image_item['id'] = image_id
    image_item['file_name'] = file_name

    im_name = file_name.strip().split('.j')[0]
    voc_txt_lines.append(im_name)

    image_item['width'] = size['width']
    image_item['height'] = size['height']
    coco['images'].append(image_item)
    image_set.add(file_name)
    return image_id


def addAnnoItem(object_name, image_id, category_id, bbox):
    global annotation_id
    annotation_item = dict()
    annotation_item['segmentation'] = []
    seg = []
    # bbox[] is x,y,w,h
    # left_top
    seg.append(bbox[0])
    seg.append(bbox[1])
    # left_bottom
    seg.append(bbox[0])
    seg.append(bbox[1] + bbox[3])
    # right_bottom
    seg.append(bbox[0] + bbox[2])
    seg.append(bbox[1] + bbox[3])
    # right_top
    seg.append(bbox[0] + bbox[2])
    seg.append(bbox[1])

    annotation_item['segmentation'].append(seg)

    annotation_item['area'] = bbox[2] * bbox[3]
    annotation_item['iscrowd'] = 0
    annotation_item['ignore'] = 0
    annotation_item['image_id'] = image_id
    annotation_item['bbox'] = bbox
    annotation_item['category_id'] = category_id
    annotation_id += 1
    annotation_item['id'] = annotation_id
    coco['annotations'].append(annotation_item)


def parseXmlFiles(xml_dir, txt_list):
    for f in txt_list:
        xml_file = os.path.join(xml_dir, f.strip()+'.xml')
        assert os.path.exists(xml_file)
        print(xml_file)

        bndbox = dict()
        size = dict()
        current_image_id = None
        current_category_id = None
        file_name = None
        size['width'] = None
        size['height'] = None
        size['depth'] = None
        
        tree = ET.parse(xml_file)
        root = tree.getroot()
        if root.tag != 'annotation':
            raise Exception('pascal voc xml root element should be annotation, rather than {}'.format(root.tag))

        # elem is <folder>, <filename>, <size>, <object>
        for elem in root:
            current_parent = elem.tag
            current_sub = None
            object_name = None

            if elem.tag == 'folder':
                continue

            if elem.tag == 'filename':
                file_name = elem.text
                if file_name in category_set:
                    raise Exception('file_name duplicated')

            # add img item only after parse <size> tag
            elif current_image_id is None and file_name is not None and size['width'] is not None:
                if file_name not in image_set:
                    current_image_id = addImgItem(file_name, size)
                    print('add image with {} and {}'.format(file_name, size))
                else:
                    raise Exception('duplicated image: {}'.format(file_name))
                    # subelem is <width>, <height>, <depth>, <name>, <bndbox>
            for subelem in elem:
                bndbox['xmin'] = None
                bndbox['xmax'] = None
                bndbox['ymin'] = None
                bndbox['ymax'] = None

                current_sub = subelem.tag
                if current_parent == 'object' and subelem.tag == 'name':
                    object_name = subelem.text
                    if object_name not in category_set:
                        current_category_id = addCatItem(object_name)
                    else:
                        current_category_id = category_set[object_name]

                elif current_parent == 'size':
                    
                    if size[subelem.tag] is not None:
                        raise Exception('xml structure broken at size tag.')
                    size[subelem.tag] = int(subelem.text)

                # option is <xmin>, <ymin>, <xmax>, <ymax>, when subelem is <bndbox>
                for option in subelem:
                    if current_sub == 'bndbox':
                        if bndbox[option.tag] is not None:
                            raise Exception('xml structure corrupted at bndbox tag.')
                        bndbox[option.tag] = int(float(option.text))

                # only after parse the <object> tag
                if bndbox['xmin'] is not None:
                    if object_name is None:
                        raise Exception('xml structure broken at bndbox tag')
                    if current_image_id is None:
                        raise Exception('xml structure broken at bndbox tag')
                    if current_category_id is None:
                        raise Exception('xml structure broken at bndbox tag')
                    bbox = []
                    # x
                    bbox.append(bndbox['xmin'])
                    # y
                    bbox.append(bndbox['ymin'])
                    # w
                    bbox.append(bndbox['xmax'] - bndbox['xmin'])
                    # h
                    bbox.append(bndbox['ymax'] - bndbox['ymin'])
                    print('add annotation with {},{},{},{}'.format(object_name, current_image_id, current_category_id,
                                                                   bbox))
                    addAnnoItem(object_name, current_image_id, current_category_id, bbox)

    print(coco['categories'])
    print(category_set)



def voc2coco(root_dir, txt_file, save_name=None, save_dir=None, save_txt=False):
    '''
    @root_dir: vocdevit dir
    @save_dir: output json file save dir
    @set_type: trainval/train/val/test
    @save_name: save_name.json
    '''
    assert os.path.exists(root_dir)
    xml_dir = os.path.join(root_dir, 'Annotations')
    if not save_dir:
        save_dir = root_dir
    if not save_name:
        sname = 'instances.json'
    else:
        sname = '{}.json'.format(save_name)
    save_path = os.path.join(save_dir, sname)

    txt_list = readTxt2Lines(txt_file)
    parseXmlFiles(xml_dir, txt_list)
    json.dump(coco, open(save_path, 'w'))
    if save_txt:
        writeLines2Txt(voc_txt_lines, os.path.join(save_dir, sname.strip().replace('.json', '.txt')))



if __name__ == '__main__':

    root_dir = r'D:\Dataset\text\CTW'
    txt_file = r'D:\Dataset\text\CTW\ImageSets\Main\val.txt'
    save_name = 'val'
    voc2coco(root_dir, txt_file, save_name)