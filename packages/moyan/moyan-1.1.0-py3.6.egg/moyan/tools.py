#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import os
import sys
import cv2
import numpy as np
import hashlib
import xml.etree.ElementTree as ET
 
def sayhi():
    print('hello world!!!')

def cv_read(path, tag=1):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), tag)

def parse_rec(filename, only_3477=False, only_price=False, isonline_price=False, score=False):
    """ Parse a PASCAL VOC xml file """
    tree = ET.parse(filename)
    objects = []
    for obj in tree.findall('object'):
        obj_struct = {}

        if only_3477:
            if obj.find('name').text != '3477':
                continue

        if only_price:
            if obj.find('name').text != '1':
                continue
        
        if score:
            obj_struct['score'] = obj.find('score').text



        obj_struct['name'] = obj.find('name').text
        # print(filename)
        
        if only_price:
            if isonline_price:
                prices_obj = obj.find('prices')
                prices = [p.text for p in prices_obj]
                if len(prices) == 1:
                    price = prices[0]
                elif len(prices) == 2:
                    price = '{}_{}'.format(prices[0], prices[1])
                else:
                    raise Exception("the file {} xml is wrong, len(prices)>2".format(os.path.basename(filename)))
            else:
                price = obj.find('price').text
            # print(price)
            obj_struct['price'] = price

        # obj_struct['pose'] = obj.find('pose').text
        # obj_struct['truncated'] = int(obj.find('truncated').text)
        # obj_struct['difficult'] = int(obj.find('difficult').text)
        # obj_struct['class'] = str(obj.find('name').text)
        bbox = obj.find('bndbox')
        obj_struct['bbox'] = [int(float(bbox.find('xmin').text)),
                              int(float(bbox.find('ymin').text)),
                              int(float(bbox.find('xmax').text)),
                              int(float(bbox.find('ymax').text))]
        objects.append(obj_struct)
    return objects


def read_xml_boxlist(imgPath, xmlPath, with_price=False):

    [height, width, channel] = cv2.imread(imgPath).shape
    tree = ET.parse(xmlPath)

    objects = []
    pic_struct = {}
    pic_struct['width'] = str(width)
    pic_struct['height'] = str(height)
    pic_struct['depth'] = str(channel)
    objects.append(pic_struct)

    for obj in tree.findall('object'):
        obj_struct = {}
        obj_struct['name'] = obj.find('name').text
        if with_price:
            prices_obj = obj.find('prices')
            prices = [p.text for p in prices_obj]
            obj_struct['price'] = prices
        bbox = obj.find('bndbox')
        op_xmin = int(float(bbox.find('xmin').text))
        op_ymin = int(float(bbox.find('ymin').text))
        op_xmax = int(float(bbox.find('xmax').text))
        op_ymax = int(float(bbox.find('ymax').text))
        # 防止越界 1
        op_xmin = 0 if op_xmin <= -1 else op_xmin
        op_ymin = 0 if op_ymin <= -1 else op_ymin
        op_xmax = width if op_xmax > width else op_xmax
        op_ymax = height if op_ymax > height else op_ymax
        # 防止越界 2
        if (op_xmin > width) | (op_ymin > height) | (op_xmax > width)\
                | (op_ymax > height) | (op_xmin < 0) | (op_ymin < 0)\
                | (op_xmax < 0) | (op_ymax < 0) | (op_xmin > op_xmax):
            continue
        obj_struct['bbox'] = [str(op_xmin), str(
            op_ymin), str(op_xmax), str(op_ymax)]
        objects.append(obj_struct)
    return objects


def indent(elem, level=0):
    i = "\n" + level*"\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def writeXml(bbox, img_name, xml_path, write_price=False, use3477=False, write_text=False):

    # [ { 'width': xx ; 'depth' : xx ; 'height': xx} ; {'name' : 'class_name' ; 'bbox' : [xmin ymin xmax ymax] }  ]
    new_xml = ET.Element('annotation')
    folder = ET.SubElement(new_xml, 'folder')
    folder.text = 'VOC2007'
    filename = ET.SubElement(new_xml, 'filename')
    filename.text = img_name

    size = ET.SubElement(new_xml, 'size')
    width = ET.SubElement(size, 'width')
    width.text = bbox[0]['width']
    height = ET.SubElement(size, 'height')
    height.text = bbox[0]['height']
    depth = ET.SubElement(size, 'depth')
    depth.text = bbox[0]['depth']

    h = int(bbox[0]['height'])
    w = int(bbox[0]['width'])

    for i in range(1, len(bbox)):

        object = ET.SubElement(new_xml, 'object')
        name = ET.SubElement(object, 'name')

        if use3477:
            name.text = '3477'
        else:
            label_name = str(bbox[i]['name'])
            name.text = label_name

        if write_price:
            price = ET.SubElement(object, 'price')
            price.text = str(bbox[i]['price'])

        if write_text:
            price = ET.SubElement(object, 'text_ocr')
            price.text = str(bbox[i]['text_ocr'])

        difficult = ET.SubElement(object, 'difficult')
        difficult.text = '0'

        bndbox = ET.SubElement(object, 'bndbox')

        xmin_ = int(float(bbox[i]['bbox'][0]))
        ymin_ = int(float(bbox[i]['bbox'][1]))
        xmax_ = int(float(bbox[i]['bbox'][2]))
        ymax_ = int(float(bbox[i]['bbox'][3]))

        xmin_ = 0 if xmin_ < 0 else xmin_
        ymin_ = 0 if ymin_ < 0 else ymin_
        xmax_ = xmax_ if xmax_ <= w else w
        ymax_ = ymax_ if ymax_ <= h else h

        xmin = ET.SubElement(bndbox, 'xmin')
        xmin.text = str(xmin_)
        ymin = ET.SubElement(bndbox, 'ymin')
        ymin.text = str(ymin_)
        xmax = ET.SubElement(bndbox, 'xmax')
        xmax.text = str(xmax_)
        ymax = ET.SubElement(bndbox, 'ymax')
        ymax.text = str(ymax_)

    indent(new_xml)
    et = ET.ElementTree(new_xml)  # 生成文档对象
    et.write(xml_path, encoding='utf-8', xml_declaration=True)


def priceTag_padd_pixel(img, edge_size_w=200, edge_size_h=96):
    # print(img.shape)
    h, w, _ = img.shape

    width_ratio = float(w) / edge_size_w
    if width_ratio > 1:
        img = cv2.resize(img, (int(w/width_ratio), int(h/width_ratio)))
        h, w, _ = img.shape
        width_ratio = float(w) / edge_size_w

    height_ratio = float(h) / edge_size_h
    if height_ratio > 1:
        img = cv2.resize(img, (int(w/height_ratio), int(h/height_ratio)))
        h, w, _ = img.shape
        height_ratio = float(h) / edge_size_h

    if width_ratio > height_ratio:
        resize_width = edge_size_w
        resize_height = int(round(h / width_ratio))
        if (edge_size_h - resize_height) % 2 == 1:
            resize_height += 1
    else:
        resize_height = edge_size_h
        resize_width = int(round(w / height_ratio))
        if (edge_size_w - resize_width) % 2 == 1:
            resize_width += 1

    try:
        img = cv2.resize(img, (int(resize_width), int(
            resize_height)), interpolation=cv2.INTER_LINEAR)
    except Exception:
        print('123')

    channels = 3
    if width_ratio > height_ratio:
        padding = (edge_size_h - resize_height) // 2   # moyan
        noise_size = (padding, edge_size_w)
        if channels > 1:
            noise_size += (channels,)
        noise = np.random.randint(230, 240, noise_size).astype('uint8')
        img = np.concatenate((noise, img, noise), axis=0)
    else:
        padding = (edge_size_w - resize_width) // 2   # moyan
        noise_size = (edge_size_h, padding)
        if channels > 1:
            noise_size += (channels,)
        noise = np.random.randint(230, 240, noise_size).astype('uint8')
        img = np.concatenate((noise, img, noise), axis=1)
    return img


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


def walkDir2List(path):
    root_lists = []
    for fpathe, dirs, fs in os.walk(path):
        # 返回的是一个三元tupple(dirpath, dirnames, filenames),
        for f in fs:
            # print
            root_lists.append(f)
    return root_lists


def walkDir2RealPathList(path, filter_postfix=[]):
    root_lists = []
    filter_postfix = filter_postfix
    if filter_postfix:
        print("Files will be searched by the specified suffix, {}".format(filter_postfix))
    else:
        print("All files will be searched")

    for fpathe, dirs, fs in os.walk(path):
        # 返回的是一个三元tupple(dirpath, dirnames, filenames),
        for f in fs:
            # print(os.path.join(fpathe, f))
            apath = os.path.join(fpathe, f)
            ext = os.path.splitext(apath)[1]
            if filter_postfix:
                if ext in filter_postfix:
                    root_lists.append(apath)
            else:
                root_lists.append(apath)
    return root_lists

def walkDir2RealPathList_del(path):
    root_lists = []
    for fpathe, dirs, fs in os.walk(path):
        # 返回的是一个三元tupple(dirpath, dirnames, filenames),
        for k, f in enumerate(fs):
            if k == 0:
                print(fpathe)
            root_lists.append(os.path.join(fpathe, f))
    return root_lists


def pathExit(path):
    if isinstance(path, list):
        for ipath in path:
            if not os.path.exists(ipath):
                os.makedirs(ipath)
    else:
        if not os.path.exists(path):
            print("create new folder: {}".format(path))
            os.makedirs(path)

def crop2save(im, crop_area, output_filename):
    x1, y1, x2, y2 = crop_area
    crop_im = im[y1:y2, x1:x2, :]
    cv2.imwrite(output_filename, crop_im)

def w2l(win_path):
    '''
    windows path to linux
    '''
    return '/'.join(win_path.split('\\'))




def helloworld():
    print("hello world")

# if __name__ == "__main__":
#     helloworld()



def get_file_md5(filepath):
    with open(filepath,'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        hash = md5obj.hexdigest()
        return hash