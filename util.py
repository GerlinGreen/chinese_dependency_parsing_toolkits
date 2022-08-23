import os
import glob
import json

def write_file(path, data) :
    with open(path, "w", encoding="utf-8") as fw :
        json.dump(data, fw, indent=4, ensure_ascii=False)
    