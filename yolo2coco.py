from PIL import Image
import json
import os
import argparse
import pandas as pd

def parse_id(img_name):
    """
    e.g. 
    img_name == xx_00000000.txt, return 0
    img_name == xx_00001024.txt, return 1024
    """
    return int(img_name.split('_')[1].split('.')[0])

def convert(w, h, y1, y2, y3, y4):
    x_max = int(0.5 * ( (2*y1*w) + (y3*w) ))
    x_min = int(0.5 * ( (2*y1*w) - (y3*w) ))
    y_max = int(0.5 * ( (2*y2*h) + (y4*h) ))
    y_min = int(0.5 * ( (2*y2*h) - (y4*h) ))

    x_max = x_max if x_max <= w else w
    x_min = x_min if x_min >= 0 else 0
    y_max = y_max if y_max <= h else h
    y_min = y_min if y_min >= 0 else 0

    return x_max, x_min, y_max, y_min

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="let's make yolo 2 coco!")
    parser.add_argument("--phase", type=str, default='val')  # 'train' or 'val'
    opts = parser.parse_args()

    # parameters
    new_dataset_name = "dataset_new"
    classes_name = "classes.txt"
    # parameters end

    # count the number of targets in train and val, and assign id
    train_labels = os.listdir(os.path.join(new_dataset_name, "train_labels"))
    val_labels = os.listdir(os.path.join(new_dataset_name, "val_labels"))
    train_obj_cout = 0
    val_obj_cout = 0
    for lab in train_labels:
        f = open(os.path.join(new_dataset_name, "train_labels", lab))
        line = f.readline()
        while line:
            train_obj_cout += 1
            line = f.readline()  
        f.close()
    for lab in val_labels:
        f = open(os.path.join(new_dataset_name, "val_labels", lab))
        line = f.readline()
        while line:
            val_obj_cout += 1
            line = f.readline()  
        f.close()
    train_obj_id = [i for i in range(train_obj_cout)]
    val_obj_id = [j for j in range(train_obj_cout, train_obj_cout+val_obj_cout)]

    if opts.phase == 'train':
        obj_id = train_obj_id
    else:
        obj_id = val_obj_id

    # step 0 "info"
    info_json = {
        "description": "none",
        "url": "none",
        "version": "1.0",
        "year": 1900,
        "contributor": "none",
        "date_created:": "1900/01/01"
    }

    # step 1 "categories"
    categories = pd.read_table(os.path.join(new_dataset_name, classes_name), header=None)
    categories = categories.values.tolist()
    categories = [i[0] for i in categories]
    
    categories_json = []
    for idx, item in enumerate(categories):
        categories_json.append({"id": idx, "name":item})
    # print(categories_json)

    # step 2 "images" and "annotations" 
    if opts.phase == "train":
        images_list = os.listdir(os.path.join(new_dataset_name, "train"))
    elif opts.phase == "val":
        images_list = os.listdir(os.path.join(new_dataset_name, "val"))
    else:
        print("wrong argparse input detected!")

    images_json = []
    annotations_json = []
    obj_count = 0  # how many objects

    for num_idx, image in enumerate(images_list):
        # first "images"
        pil_image = Image.open(os.path.join(new_dataset_name, opts.phase, image))
        height = pil_image.height
        width = pil_image.width
        idx = parse_id(image)
        # print(idx, image, height, width)
        images_json.append({"file_name": image, "height": height, "width": width, "id": idx})

        # then "annotations"
        txts_list = [i.replace('.jpg', '.txt') for i in images_list]
        f = open(os.path.join(new_dataset_name, "{}_labels".format(opts.phase), txts_list[num_idx]))
        
        line = f.readline()            
        while line:
            five = line.replace('\n', '').split(' ')
            cls_id = int(five[0])
            yolo_1, yolo_2, yolo_3, yolo_4, = float(five[1]), float(five[2]), float(five[3]), float(five[4])
            
            x_max, x_min, y_max, y_min = convert(width, height, yolo_1, yolo_2, yolo_3, yolo_4)

            data_anno = dict(
                image_id=idx,
                id=obj_id[obj_count],  # can't have the same id in train and val
                category_id=cls_id,
                bbox=[x_min, y_min, x_max - x_min, y_max - y_min],
                area=(x_max - x_min) * (y_max - y_min),
                segmentation=None,
                iscrowd=0)
            annotations_json.append(data_anno)
            obj_count += 1
            line = f.readline()

        f.close()

    # save the json file
    json_dict = {
        "info": info_json,
        "images": images_json,
        "annotations": annotations_json,
        "categories": categories_json
    }
    
    os.makedirs("{}/annotations".format(new_dataset_name), exist_ok=True)

    with open("{}/annotations/{}.json".format(new_dataset_name, opts.phase), 'w', encoding="utf-8") as f:
        json.dump(json_dict, f, indent=None, sort_keys=False, ensure_ascii=False)
    
    print("{} set finished!".format(opts.phase))


