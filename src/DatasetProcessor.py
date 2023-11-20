import os
import sys
import time
import json
import random

from datasets import Dataset

from stage2.labels_to_nn import LabelToNN


DATASET_PATH = "/home/knaumenko/private_data/AIm-Finder-2023/dataset/HF_dataset/"
RANDOM_SEED = 42


class DatasetProcessor():
    def __init__(self, dataset_path=DATASET_PATH) -> None:
        self.dataset_path = dataset_path
        
    def make_dataset(self):
        train_dir = self.dataset_path + 'train/'
        files = os.listdir(train_dir)
        train_data = {"tokens": [], "ner_tags": []}

        for file in files:
            path = train_dir + file
            translater = LabelToNN()
            translater.load(path)
            tmp = translater.run()
            train_data["tokens"].extend(tmp["tokens"])
            train_data["ner_tags"].extend(tmp["ner_tags"])
        
        

        with open(self.dataset_path + 'augmentation.json') as user_file:
            aug_data = json.load(user_file)[0]

        # with open(self.dataset_path + 'aug_test.json') as user_file:
        #     aug_test_data = json.load(user_file)[0]

        with open(self.dataset_path + 'aug_test_big.json') as user_file:
            aug_test_data = json.load(user_file)[0]
        

        aug_num = len(aug_data["tokens"])
        print(aug_num)
        
        tmp_test = Dataset.from_dict(train_data).train_test_split(test_size=0.2, seed=RANDOM_SEED)['test']
        # aug_test = Dataset.from_dict(aug_data).train_test_split(test_size=0.01, seed=RANDOM_SEED)['test']

        # inds = random.Random(RANDOM_SEED).sample(range(0, aug_num), 1000)
        # train_data["tokens"].extend(
        #     [token for i, token in enumerate(aug_data["tokens"]) if i in inds]
        #     )
        # train_data["ner_tags"].extend(
        #     [tag for i, tag in enumerate(aug_data["ner_tags"]) if i in inds]
        #     )

        train_data["tokens"].extend(aug_data["tokens"])
        train_data["ner_tags"].extend(aug_data["ner_tags"])
        train_dataset = Dataset.from_dict(train_data)
        print('Total train raws:', len(train_dataset))

        test_file = self.dataset_path + 'test/test.json'
        translater = LabelToNN()
        translater.load(test_file)
        test_data = translater.run()

        test_data["tokens"].extend(tmp_test["tokens"])
        test_data["ner_tags"].extend(tmp_test["ner_tags"])

        # test_data["tokens"].extend(aug_test["tokens"])
        # test_data["ner_tags"].extend(aug_test["ner_tags"])

        test_data["tokens"].extend(aug_test_data["tokens"])
        test_data["ner_tags"].extend(aug_test_data["ner_tags"])

        test_dataset = Dataset.from_dict(test_data)
        print('Total test raws:', len(test_dataset))

        return train_dataset, test_dataset

    def save_dataset(self):
        train, test = self.make_dataset()
        train.push_to_hub("kosta-naumenko/medflex")
        test.push_to_hub("kosta-naumenko/medflex-test")
        print('Saved to HuggingFace')


if __name__ == "__main__":
    processor = DatasetProcessor()
    processor.save_dataset()