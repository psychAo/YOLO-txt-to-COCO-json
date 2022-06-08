# SRD.py, SRD for
# Shuffle the entire dataset 
# Rename all files to the same format
# Divide the dataset into training and validation sets
import os
import random
import shutil

def zero_padding(num_str):
    str_len = len(num_str)
    if str_len == 1:
        return '0000000' + num_str
    elif str_len == 2:
        return '000000' + num_str
    elif str_len == 3:
        return '00000' + num_str
    elif str_len == 4:
        return '0000' + num_str
    elif str_len == 5:
        return '000' + num_str
    elif str_len == 6:
        return '00' + num_str
    elif str_len == 7:
        return '0' + num_str
    elif str_len == 8:
        return num_str
    else:
        print("wrong input string of number!")
        return None

def new_name_gene(prefix, ds_len):
    """
    prefix: string
    ds_len: int, length of the dataset
    """
    new_images_name = [prefix+'_'+zero_padding('{}'.format(i))+'.jpg' for i in range(ds_len)]
    new_labels_name = [prefix+'_'+zero_padding('{}'.format(i))+'.txt' for i in range(ds_len)]

    return new_images_name, new_labels_name

if __name__ == "__main__":
    # parameters
    dataset_path = "dataset"  # path of the dataset
    prefix = 'ds'
    shuffle = True  # whether to shuffle the dataset
    val_num = 10
    # parameters end

    images_path = os.path.join(dataset_path, "images")
    labels_path = os.path.join(dataset_path, "labels")

    images_list = os.listdir(images_path)
    labels_list = os.listdir(labels_path)

    new_images_name, new_labels_name = new_name_gene(prefix, len(images_list))

    if len(images_list) <= 50:
        print("before:")
        print(images_list)
        print(labels_list)

    # S phase
    if shuffle:
        random.seed(35)
        random.shuffle(new_images_name)
        random.seed(35)
        random.shuffle(new_labels_name)

    print("shuffle = ", shuffle)
    if len(images_list) <= 50:
        print("after:")
        print(new_images_name)
        print(new_labels_name)

    # R phase
    os.makedirs(dataset_path+"_new", exist_ok=True)
    os.makedirs(os.path.join(dataset_path+"_new", "images"), exist_ok=True)
    os.makedirs(os.path.join(dataset_path+"_new", "labels"), exist_ok=True)

    for i in range(len(images_list)):
        shutil.copyfile(
            os.path.join(dataset_path, "images", images_list[i]),
            os.path.join(dataset_path+"_new", "images", new_images_name[i])
        )
        
        shutil.copyfile(
            os.path.join(dataset_path, "labels", labels_list[i]),
            os.path.join(dataset_path+"_new", "labels", new_labels_name[i])
        )

    # D phase
    os.rename(
        os.path.join(dataset_path+"_new", "images"),
        os.path.join(dataset_path+"_new", "train")
    )
    os.rename(
        os.path.join(dataset_path+"_new", "labels"),
        os.path.join(dataset_path+"_new", "train_labels")
    )

    os.makedirs(os.path.join(dataset_path+"_new", "val"), exist_ok=True)
    os.makedirs(os.path.join(dataset_path+"_new", "val_labels"), exist_ok=True)

    random.seed(35)
    val_images = random.sample(new_images_name, val_num)
    random.seed(35)
    val_labels = random.sample(new_labels_name, val_num)

    if len(images_list) <= 50:
        print("validation:")
        print(val_images)
        print(val_labels)

    for i in range(val_num):
        shutil.move(
            os.path.join(dataset_path+"_new", "train", val_images[i]),
            os.path.join(dataset_path+"_new", "val", val_images[i])
        )
        
        shutil.move(
            os.path.join(dataset_path+"_new", "train_labels", val_labels[i]),
            os.path.join(dataset_path+"_new", "val_labels", val_labels[i])
        )

    shutil.copyfile(
        os.path.join(dataset_path+"", "classes.txt"),
        os.path.join(dataset_path+"_new", "classes.txt")
    )

    print("finished!")


