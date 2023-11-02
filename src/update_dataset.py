import os
import sys
import time

from datasets import Dataset, load_dataset

from stage2.labels_to_nn import LabelToNN


if __name__ == "__main__":
    dir_name = "dataset/HF_dataset/"
    files = os.listdir(dir_name)
    result = {"tokens": [], "ner_tags": []}

    for file in files:
        path = dir_name + file
        translater = LabelToNN()
        translater.load(path)
        tmp = translater.run()
        result["tokens"].extend(tmp["tokens"])
        result["ner_tags"].extend(tmp["ner_tags"])

    raw_dataset = Dataset.from_dict(result)
    raw_dataset.push_to_hub("kosta-naumenko/medflex")
    print('Total raws:', len(raw_dataset))
