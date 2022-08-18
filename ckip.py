import os
import glob
import json
import transformers
from argparse import ArgumentParser
from transformers import pipeline, PreTrainedTokenizer


def write_file(path, data) :
    with open(path, "w", encoding="utf-8") as fw :
        json.dump(data, fw, indent=4, ensure_ascii=False)
    

def word_entity(ckiptask, tokens) :
    token_list = []
    entities = {}
    tmp_token = ""      
    pre_token = {'entity': '', 
                'score': 0,
                'index': 0, 
                'word': '',
                'start': 0,
                'end': 0}

    for t, token in enumerate(tokens) :
        if pre_token["entity"] != "" :
            if token["entity"] == pre_token["entity"] :
                tmp_token = tmp_token + token["word"]
            else :
                if pre_token["entity"] not in list(entities.keys()) :
                    entities[pre_token["entity"]] = []
                tmp = [tmp_token, t-len(tmp_token), t]
                entities[pre_token["entity"]].append(tmp)
                # print(entities)
                token_list.append(tmp_token)
                tmp_token = token["word"]
        else :
            tmp_token = token["word"]
        pre_token = token

    return token_list, entities


parser = ArgumentParser()
parser.add_argument('-t', '--task', default="pos", help='pos, ws, fill-mask')
parser.add_argument('-i', '--input_dir', help='path to the input folder (ltf files)')
parser.add_argument('-o', '--output_dir', help='path to the output folder (json files)')
parser.add_argument('--lang', default='chinese', help='Model language')

args = parser.parse_args()

ckiptask=args.task
input_path=args.input_dir
output_path=args.output_dir
language=args.lang

print("ckiptask>>", ckiptask)
print("input_path>>", input_path)
print("output_path>>", output_path)
print("language>>", language)

pipeline_results = {}

filenames = glob.glob(os.path.join(input_path, "*.txt"))
print(filenames)

if ckiptask == "fill-mask" :
    task = ckiptask
    model_name="ckiplab/bert-base-" + language
else :
    task = "token-classification"
    if ckiptask == "ws" :
        model_name="ckiplab/bert-base-" + language + "-ws"
    else :
        model_name="ckiplab/bert-base-" + language + "-pos"

classifier = pipeline(task, model=model_name)

for doc in filenames :
    data = open(doc, "r", encoding="utf-8").read()
    data = [s.strip() for s in data.split('\n') if s.strip()]
    # print(data)
    output = {}

    for text in data :
        tokens = classifier(text)
        if ckiptask == "pos" :
            token_list, entities = word_entity(ckiptask, tokens)
            output["token_list"] = token_list
            output["entities"] = entities

        output["sentence"] = text
        output["tokens"] = tokens

    output = str(output)
    while "'" in output :
        output = output.replace("'", '"')
    try :
        output_ = json.loads(output)
    except :
        raise AssertionError("output>>", output)
    outfilename = doc.split("\\")[-1].replace(".txt", ".json")

    write_file(output_path + "/" + outfilename, output_)