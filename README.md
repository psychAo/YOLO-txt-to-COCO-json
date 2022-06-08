# YOLO txt to COCO json
Last Update:

> 2022-06-08

Suppose there is now a set of image datasets called **dataset** annotated in YOLO format

The project has the following functions:

1. Shuffle the order of images and labels
2. Batch rename images and labels
3. Divide the dataset into training set and validation set
4. Adjust the annotation format from YOLO's txt format to COCO's json format
5. Visualize bounding boxes according to json format

Note: You can also change the code in this project according to your specific needs

# requirements
```
python == 3.7.9
pandas == 1.3.4
pillow == 8.1.0
```
# original:
original file must have this type of structure:
```
dataset
    images
        xxx.jpg
        ...
        xxx.jpg
    labels 
        xxx.txt
        ...
        xxx.txt
    classes.txt
```
and classes.txt:
```
class_name_1
...
class_name_n

```
# step 1:
```
python SRD.py
```
after step 1, file structure like this:
```
dataset_new
    annotations 
        xxx.txt
        ...
        xxx.txt
    train
        xxx.jpg
        ...
        xxx.jpg
    val
        xxx.jpg
        ...
        xxx.jpg
    classes.txt
```
# step 2:
```
python yolo2coco.py --phase train
python yolo2coco.py --phase val
```
# step 3:
```
python show_coco_anno.py --phase train
python show_coco_anno.py --phase val
```
# step 4:
rename the folder "dataset_new" with new name (your wanted name)
# step 5
enjoy the object detection~

