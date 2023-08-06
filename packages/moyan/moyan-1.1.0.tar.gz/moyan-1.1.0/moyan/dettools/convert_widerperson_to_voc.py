# -*- coding: utf-8 -*-
# Created on 8月-27-20 16:17
# @site: https://github.com/moyans
# @author: moyan
    
import os
import moyan


def main():
    root_dir = r'D:\Dataset\WiderPerson'
    txt_dir = os.path.join(root_dir, 'Annotations')
    img_dir = os.path.join(root_dir, 'Images')
    xml_dir = os.path.join(root_dir, 'xml')
    txt_list = os.listdir(txt_dir)
    for idx, names in enumerate(txt_list):
        img_name = os.path.splitext(names)[0]
        txt_path = os.path.join(txt_dir, names)
        img_path = os.path.join(img_dir, img_name)
        assert os.path.exists(txt_path)
        assert os.path.exists(img_path)
        print(idx, img_name)
        objects = []
        pic_struct = {}
        height, width, channel = moyan.cv_read(img_path).shape
        pic_struct['width'] = str(width)
        pic_struct['height'] = str(height)
        pic_struct['depth'] = str(channel)
        objects.append(pic_struct)

        txt_lines = moyan.readTxt2Lines(txt_path)
        for k, v in enumerate(txt_lines):
            if k == 0 : continue
            class_label, x1, y1, x2, y2 =  v.strip().split(' ')
            if int(class_label) == 5 : continue
            obj_struct = {}
            # print(class_label, x1, y1, x2, y2)
            obj_struct['name'] = 'person'
            obj_struct['bbox'] = [int(float(x1)),
                              int(float(y1)),
                              int(float(x2)),
                              int(float(y2))]
            objects.append(obj_struct)
        xml_path = os.path.join(xml_dir, os.path.splitext(img_name.strip())[0]+'.xml')
        moyan.writeXml(objects, img_name, xml_path)
        # print(objects, xml_path)
    
if __name__ == '__main__':
    main()