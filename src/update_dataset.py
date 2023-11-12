import os
import sys
import time
import json

from datasets import Dataset

from stage2.labels_to_nn import LabelToNN


def update_dataset(push_to_hub=True, return_dataset=False):
    dir_name = "/home/knaumenko/private_data/AIm-Finder-2023/dataset/HF_dataset/"
    files = os.listdir(dir_name)
    result = {"tokens": [], "ner_tags": []}

    for file in files:
        path = dir_name + file
        translater = LabelToNN()
        translater.load(path)
        tmp = translater.run()
        result["tokens"].extend(tmp["tokens"])
        result["ner_tags"].extend(tmp["ner_tags"])

    with open('/home/knaumenko/private_data/AIm-Finder-2023/dataset/augmentation.json') as user_file:
        aug_data = json.load(user_file)[0]

    result["tokens"].extend(aug_data["tokens"])
    result["ner_tags"].extend(aug_data["ner_tags"])

    raw_dataset = Dataset.from_dict(result)
    print('Total raws:', len(raw_dataset))

    if push_to_hub:
        raw_dataset.push_to_hub("kosta-naumenko/medflex")
    
    if return_dataset:
        return raw_dataset


if __name__ == "__main__":
    update_dataset()