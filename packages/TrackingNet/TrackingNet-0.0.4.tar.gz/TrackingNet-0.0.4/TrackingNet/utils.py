
from pathlib import Path
import json
import os


def getListSplit():
    return ["TEST", "TRAIN_0", "TRAIN_1", "TRAIN_2", "TRAIN_3", "TRAIN_4", "TRAIN_5", "TRAIN_6", "TRAIN_7", "TRAIN_8", "TRAIN_9", "TRAIN_10", "TRAIN_11"]


def getDimensionSplit(split):

    jsonGamesFile = Path(__file__).parent / \
        f"data/{split}.json"

    with open(jsonGamesFile, "r") as json_file:
        return json.load(json_file)["size_bytes"]
            # list_sequence.append(os.path.join(spl, youtube_id))

    # return ["TEST", "TRAIN_0", "TRAIN_1", "TRAIN_2", "TRAIN_3", "TRAIN_4", "TRAIN_5", "TRAIN_6", "TRAIN_7", "TRAIN_8", "TRAIN_9", "TRAIN_10", "TRAIN_11"]

def getListSequence(split="all"):

    # if an element is "all", convert to train_{i}/test
    if split.upper() == "ALL":
        split = [f"TRAIN_{i}" for i in range(12)]
        split.append("TEST")
    elif split.upper() == "TRAIN":
        split = [f"TRAIN_{i}" for i in range(12)]
    elif split.upper() == "TEST":
        split = ["TEST"]
    else: 
        split = [split]
    # print(split)

   
    list_sequence = []
    # loop over splits
    for spl in split:
        jsonGamesFile = Path(__file__).parent / \
            f"data/{spl}.json"
           
        with open(jsonGamesFile, "r") as json_file:
            for youtube_id in json.load(json_file)["sequences"]:
                list_sequence.append(os.path.join(spl, youtube_id))

    return list_sequence


if __name__ == "__main__":
    print(len(getListSequence("TRAIN_0")))
    # print(getListSequence("TRAIN_0"))
