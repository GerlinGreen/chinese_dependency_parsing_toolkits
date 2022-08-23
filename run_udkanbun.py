import os
import glob
import json
import udkanbun
from util import write_file
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument('-i', '--input_dir', help='path to the input folder')
parser.add_argument('-o', '--output_dir', help='path to the output folder')
parser.add_argument('--bert', default=None, help='None/guwenbert-base/guwenbert-large\n>>> See https://github.com/KoichiYasuoka/UD-Kanbun/blob/master/udkanbun/udkanbun.py (line 204)')

args = parser.parse_args()

input_path=args.input_dir
output_path=args.output_dir
bert=args.bert

print("input_path>>", input_path)
print("output_path>>", output_path)
print("bert_model>>", bert)

filenames = glob.glob(os.path.join(input_path, "*.txt"))
print(filenames)

lzh = udkanbun.load(BERT=bert)

pipeline_results = {}

for doc in filenames :
    data = open(doc, "r", encoding="utf-8").read()
    data = [s.strip() for s in data.split('\n') if s.strip()]
    output = {}

    for t, text in enumerate(data) :
        docid = doc.split(".")[0] + "_" + str(t)
        rows = lzh(text)

        output[docid] = {}
        output[docid]["sentence"] = text
        output[docid]["tokens"] = []
        output[docid]["token_list"] = []
        output[docid]["entities"] = {}

        span_indx = 0
        for i, token in enumerate(rows) :
            if i > 0 :
                token = str(token).split("\t")
                word_span = [token[2], span_indx, span_indx + len(token[2])]
                span_indx = span_indx + len(token[2])
                output[docid]["tokens"].append(token)
                output[docid]["token_list"].append(token[2])
                if token[3] not in output[docid]["entities"]:
                    output[docid]["entities"][token[3]] = []
                output[docid]["entities"][token[3]].append(word_span)

    outfilename = doc.split("\\")[-1].replace(".txt", ".json")
    print("output>>>", output)
    # print("output_path>>>", output_path)
    write_file(output_path + "/" + outfilename, output)
