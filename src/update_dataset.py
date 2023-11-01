import os

from datasets import Dataset, load_dataset


if __name__ == "__main__":
    dir_name = "../dataset/HF_dataset/"
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

    loaded_dataset = load_dataset("kosta-naumenko/medflex")

    assert len(raw_dataset) == len(loaded_dataset["train"])
