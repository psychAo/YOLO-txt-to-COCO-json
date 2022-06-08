import os
import sys
import json
import random
import argparse
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

def parse_id(img_name):
    return int(img_name.split('_')[1].split('.')[0])

def randomcolor():
    colorArr = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    color = ""
    for _ in range(6):
        color += colorArr[random.randint(0, 14)]
    return "#" + color

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="show coco json object detection annotations!")
    parser.add_argument("--new_name", type=str, default='dataset_new', help="new dataset name")  # 'train' or 'val'
    parser.add_argument("--phase", type=str, default='val')  # 'train' or 'val'
    parser.add_argument("--num_show", type=int, default=-1, help="number of images to show, -1 for all")  # -1 for all
    opts = parser.parse_args()

    # make directions
    os.makedirs("{}_anno_show/{}".format(opts.new_name, opts.phase), exist_ok=True)

    # categories
    categories = pd.read_table(os.path.join(opts.new_name, "classes.txt"), header=None)
    categories = categories.values.tolist()
    categories = [i[0] for i in categories]
    # print(categories)

    # colors for bounding boxes
    random.seed(35)
    colors = []
    for i in range(len(categories)):
        colors.append(randomcolor())
    # print(colors)

    # load the images (decide the number of images to be shown)
    images = []

    all_imgs = os.listdir(os.path.join(opts.new_name, opts.phase))
    
    if opts.num_show == -1:
        images = all_imgs.copy()
    
    elif (0 < opts.num_show <= len(all_imgs)):
        for i in range(opts.num_show):
            images.append(all_imgs[i])
    
    elif opts.num_show == 0:
        print("0 image to be annotated")
        sys.exit()
    else:
        images = all_imgs.copy()

    del all_imgs

    # load annotations in json
    f = open("{}/annotations/{}.json".format(opts.new_name, opts.phase))
    data = json.load(f)

    # plot bounding boxes for each image
    for img_name in images:

        img = Image.open(os.path.join(opts.new_name, opts.phase, img_name))
        img_id = parse_id(img_name)
        
        annos = []  # annotations for every image

        for anno in data["annotations"]:
            if anno["image_id"] == img_id:
                annos.append(anno)

        # draw bounding boxes
        draw = ImageDraw.Draw(img)

        for i in range(len(annos)):
            bbox = annos[i]["bbox"]
            cls_id = annos[i]["category_id"]
            draw.rectangle((bbox[0], bbox[1], bbox[0]+bbox[2], bbox[1]+bbox[3]), outline=colors[cls_id], width=2)
            draw.text((bbox[0] + 2, bbox[1] + 2), categories[cls_id], colors[cls_id], font = ImageFont.truetype('simhei', 20))

        # save the resulting image
        img.save("{}_anno_show/{}/{}".format(opts.new_name, opts.phase, img_name))

    print("{} set finished!".format(opts.phase))


