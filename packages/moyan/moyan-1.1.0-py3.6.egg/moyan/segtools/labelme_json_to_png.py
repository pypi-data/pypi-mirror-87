# -*- coding:utf-8 -*-
# time: 2020-08-17
# @author: moyan

import json
import io, math, os
import uuid
# from moyan.tools import pathExit
from tqdm import tqdm
# from labelme import utils
import base64
import numpy as np
import PIL.ImageDraw
import PIL.ExifTags
import PIL.Image
import PIL.ImageOps

global label_name_to_value
label_name_to_value = {'_background_': 0}

def img_data_to_pil(img_data):
    f = io.BytesIO()
    f.write(img_data)
    img_pil = PIL.Image.open(f)
    return img_pil


def img_data_to_arr(img_data):
    img_pil = img_data_to_pil(img_data)
    img_arr = np.array(img_pil)
    return img_arr

def img_b64_to_arr(img_b64):
    img_data = base64.b64decode(img_b64)
    img_arr = img_data_to_arr(img_data)
    return img_arr

def shape_to_mask(
    img_shape, points, shape_type=None, line_width=10, point_size=5
):
    mask = np.zeros(img_shape[:2], dtype=np.uint8)
    mask = PIL.Image.fromarray(mask)
    draw = PIL.ImageDraw.Draw(mask)
    xy = [tuple(point) for point in points]
    if shape_type == "circle":
        assert len(xy) == 2, "Shape of shape_type=circle must have 2 points"
        (cx, cy), (px, py) = xy
        d = math.sqrt((cx - px) ** 2 + (cy - py) ** 2)
        draw.ellipse([cx - d, cy - d, cx + d, cy + d], outline=1, fill=1)
    elif shape_type == "rectangle":
        assert len(xy) == 2, "Shape of shape_type=rectangle must have 2 points"
        draw.rectangle(xy, outline=1, fill=1)
    elif shape_type == "line":
        assert len(xy) == 2, "Shape of shape_type=line must have 2 points"
        draw.line(xy=xy, fill=1, width=line_width)
    elif shape_type == "linestrip":
        draw.line(xy=xy, fill=1, width=line_width)
    elif shape_type == "point":
        assert len(xy) == 1, "Shape of shape_type=point must have 1 points"
        cx, cy = xy[0]
        r = point_size
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=1, fill=1)
    else:
        assert len(xy) > 2, "Polygon must have points more than 2"
        draw.polygon(xy=xy, outline=1, fill=1)
    mask = np.array(mask, dtype=bool)
    return mask


def shapes_to_label(img_shape, shapes, label_name_to_value, line_width):
    cls = np.zeros(img_shape[:2], dtype=np.int32)
    ins = np.zeros_like(cls)
    instances = []
    for shape in shapes:
        points = shape["points"]
        label = shape["label"]
        group_id = shape.get("group_id")
        if group_id is None:
            group_id = uuid.uuid1()
        shape_type = shape.get("shape_type", None)

        cls_name = label
        instance = (cls_name, group_id)

        if instance not in instances:
            instances.append(instance)
        ins_id = instances.index(instance) + 1
        cls_id = label_name_to_value[cls_name]

        mask = shape_to_mask(img_shape[:2], points, shape_type, line_width=line_width)
        cls[mask] = cls_id
        ins[mask] = ins_id

    return cls, ins

def lblsave(filename, lbl):
    import imgviz

    if os.path.splitext(filename)[1] != ".png":
        filename += ".png"
    # Assume label ranses [-1, 254] for int32,
    # and [0, 255] for uint8 as VOC.
    if lbl.min() >= -1 and lbl.max() < 255:
        lbl_pil = PIL.Image.fromarray(lbl.astype(np.uint8), mode="P")
        colormap = imgviz.label_colormap()
        lbl_pil.putpalette(colormap.flatten())
        lbl_pil.save(filename)
    else:
        raise ValueError(
            "[%s] Cannot save the pixel-wise class label as PNG. "
            "Please consider using the .npy format." % filename
        )


def labelme_json_to_png(jsonlist, img_dir, save_dir, pix_line=None):

    if not os.path.exists(save_dir):
        print("create new folder: {}".format(save_dir))
        os.makedirs(save_dir)

    for json_path in tqdm(jsonlist):
        assert os.path.exists(json_path)
        name = os.path.splitext(os.path.basename(json_path))[0]
        png_save_path = os.path.join(save_dir, name.strip()+'.png')

        data = json.load(open(json_path))
        imageData = data.get('imageData')
        if not imageData:
            img_path = os.path.join(img_dir, name.strip()+'.jpg')
            assert os.path.exists(img_path)
            with open(img_path, 'rb') as f:
                imageData = f.read()
                imageData = base64.b64encode(imageData).decode('utf-8')
        img = img_b64_to_arr(imageData)

        if not pix_line:
            h, w = img.shape[:2]
            pix_all = h*w
            if pix_all < 600*600:
                line_width = 1
            elif pix_all < 1200*1200:
                line_width = 2
            else:
                line_width = 3
        else:
            line_width = pix_line

        for shape in sorted(data['shapes'], key=lambda x: x['label']):
            label_name = shape['label']
            if label_name in label_name_to_value:
                label_value = label_name_to_value[label_name]
            else:
                label_value = len(label_name_to_value)
                label_name_to_value[label_name] = label_value

        lbl, _ = shapes_to_label(img.shape, data['shapes'], label_name_to_value, line_width=line_width)
        lblsave(png_save_path, lbl)
               

def main():
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
    imgdir = r'D:\code\segcode-pytorch\data\data_example\json'
    jsonlist = walkDir2RealPathList(imgdir, filter_postfix=['.json'])
    labelme_json_to_png(jsonlist, imgdir, save_dir=imgdir)

if __name__ == "__main__":
    main()