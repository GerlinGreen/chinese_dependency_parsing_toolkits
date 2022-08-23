import glob
import json
import os
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-s', '--standard', default="CKIP", help='CKIP/UD')
parser.add_argument('-t', '--target', default="Verb", help='Abbreviation lookup: https://www.sketchengine.eu/chinese-symbol-part-of-speech-tagset/')
parser.add_argument('-i', '--input_dir', help='path to the input folder (ltf files)')
parser.add_argument('-o', '--output_dir', help='path to the output folder (json files)')

args = parser.parse_args()

standard = args.standard
target=args.target
input_path=args.input_dir
output_path=args.output_dir


if standard == "CKIP" :
    """
    target samples (CKIP):
    1. Verb (which can be found in POS.keys())
    2. Nfb (which can be found in POS[Measure(keyname)]
                        [Corresponded symbols in CKIP])
    3. Nfb, Nfc, Nhaa (whichs can be found in 
                        POS[Measure(keyname)][Corresponded symbols in CKIP]
                        and POS[Pronoun(keyname)][Corresponded symbols in CKIP])
    """
    POS = {
        "Adjective": {
            "Abbreviation": ["A"],
            "Corresponded symbols in CKIP": ["A"],
            "Interpretation": ["Non-predicative adjective"]
        }, 
        "Conjunction": {
            "Abbreviation": [],
            "Corresponded symbols in CKIP": [],
            "Interpretation": []
        }, 
        "Adverb": {        
            "Abbreviation": [],
            "Corresponded symbols in CKIP": [],
            "Interpretation": []
        }, 
        "的-Construction": {
            "Abbreviation": [],
            "Corresponded symbols in CKIP": [],
            "Interpretation": []
        },
        "Foreign Word": {
            "Abbreviation": [],
            "Corresponded symbols in CKIP": [],
            "Interpretation": []
        },
        "Interjection": {
            "Abbreviation": ["I"],
            "Corresponded symbols in CKIP": ["I"],
            "Interpretation": ["Interjection"]
        },
        "Noun": {
            "Abbreviation": [],
            "Corresponded symbols in CKIP": [],
            "Interpretation": []
        },
        "Determiner": {
            "Abbreviation": [],
            "Corresponded symbols in CKIP": [],
            "Interpretation": []
        },
        "Measure": {
            "Abbreviation": ["Nf"],
            "Corresponded symbols in CKIP": [
                ["Nfa", "Nfb", "Nfc", "Nfd", "Nfe", "Nfg", "Nfh", "Nfi"]
            ],
            "Interpretation": ["Measure"]
        },
        "Postposition": {
            "Abbreviation": ["Ng"],
            "Corresponded symbols in CKIP": ["Ng"],
            "Interpretation": ["Postposition"]
        },
        "Pronoun": {
            "Abbreviation": ["Nh"],
            "Corresponded symbols in CKIP": [
                ["Nhaa", "Nhab", "Nhac", "Nhb", "Nhc"]
            ],
            "Interpretation": ["Pronoun"]
        },
        "Preposition": {
            "Abbreviation": ["P"],
            "Corresponded symbols in CKIP": ["P*"],
            "Interpretation": ["Preposition"]
        },
        "verb是": {
            "Abbreviation": ["SHI"],
            "Corresponded symbols in CKIP": [""],
            "Interpretation": ["是"]
        },
        "Particle": {
            "Abbreviation": ["T"],
            "Corresponded symbols in CKIP": [
                ["Ta", "Tb", "Tc", "Td"]
            ],
            "Interpretation": ["Particle"]
        },
        "Verb": {
            "Abbreviation": ["VA", "VAC", "VB", "VC", "VCL", "VD", "VE", 
                "VF", "VG", "VH", "VHC", "VI", "VJ", "VK", "VL", "V_2"],
            "Corresponded symbols in CKIP": [
                ["VA11","VA12","VA13","VA3","VA4"], 
                "VA2", 
                ["VB11", "VB12", "VB2"],
                ["VC2", "VC31", "VC32", "VC33"], 
                "VC1", 
                ["VD1", "VD2"], 
                ["VE11", "VE12", "VE2"], 
                ["VF1", "VF2"], 
                ["VG1", "VG2"], 
                ["VH11", "VH12", "VH13", "VH14", "VH15", "VH17", "VH21"], 
                ["VH16", "VH22"], 
                ["VI1", "VI2", "VI3"], 
                ["VJ1", "VJ2", "VJ3"], 
                ["VK1", "VK2"], 
                ["VL1", "VL2", "VL3", "VL4"], 
                "V_2"
            ],
            "Interpretation": [
                "Active Intransitive Verb",
                "Active Causative Verb", 
                "Active Pseudo-transitive Verb",
                "Active Transitive Verb",
                "Active Verb with a Locative Object",
                "Ditransitive Verb",
                "Active Verb with a Sentential Object",
                "Active Verb with a Verbal Object",
                "Classificatory Verb",
                "Stative Intransitive Verb",
                "Stative Causative Verb",
                "Stative Pseudo-transitive Verb",
                "Stative Transitive Verb",
                "Stative Verb with a Sentential Object",
                "Stative Verb with a Verbal Object",
                "有"
            ]
        },
        "Punctuation": {
            "Abbreviation": [],
            "Corresponded symbols in CKIP": [],
            "Interpretation": []

        }
    }

    posKeys = [key for key in POS.keys()]
    targets = []
    if target in posKeys :
        targets = POS[target]["Corresponded symbols in CKIP"]
    else :
        if "," in target :
            targets = targets.split[","]
        else :
            targets = target
    print("targets>>>", targets)

    filenames = glob.glob(os.path.join(input_path, "*.json"))

    for doc in filenames :
        data = open(doc, "r", encoding="utf-8").read()
        jdata = json.loads(data)

        extract_results = {}

        for dataid in jdata :
            extract_results[dataid] = {}
            extract_results[dataid]["sentence"] = jdata[dataid]["sentence"]
            extract_results[dataid][target] = {}

            j_entity_keys = [keys for keys in jdata[dataid]["entities"].keys()]
            # print("j_entity_keys>>>", j_entity_keys)

            for tar in targets :
                if type(tar) == list :
                    for tar_ in tar :
                        if tar_ in j_entity_keys :
                            print(tar_)
                            extract_results[dataid][target][tar_] = jdata[dataid]["entities"][tar_]
                else :
                    if tar in j_entity_keys :
                        print((tar))
                        extract_results[dataid][target][tar] = jdata[dataid]["entities"][tar]


        wpath = doc.replace(input_path, output_path)
        print("wpath>>>", wpath)
        with open(wpath, "w", encoding="utf-8") as fw :
            json.dump(extract_results, fw, indent=4, ensure_ascii=False)

elif standard == "UD" :    
    """
    target samples (UD):
    1. VERB (which can be found in POS.keys())
    2. VERB, ADP (whichs can be found in POS.keys())
    """
    POS = {
        "ADJ": "adjective",
        "ADP": "adposition",
        "ADV": "adverb",
        "AUX": "auxiliary",
        "CCONJ": "coordinating conjunction",
        "DET": "determiner",
        "INTJ": "interjection",
        "NOUN": "noun",
        "NUM": "numeral",
        "PART": "particle",
        "PRON": "pronoun",
        "PROPN": "proper noun",
        "PUNCT": "punctuation",
        "SCONJ": "subordinating conjunction",
        "SYM": "symbol",
        "VERB": "verb",
        "X": "other"
    }

    posKeys = [key for key in POS.keys()]
    targets = []

    if target in posKeys :
        targets.append(target)
    else :
        if "," in target :
            targets = targets.split[","]
        else :
            raise AssertionError("Unknown POS tag(s)>>>", target)

    print("targets>>>", targets)

    filenames = glob.glob(os.path.join(input_path, "*.json"))

    for doc in filenames :
        data = open(doc, "r", encoding="utf-8").read()
        jdata = json.loads(data)

        extract_results = {}

        for dataid in jdata :
            extract_results[dataid] = {}
            extract_results[dataid]["sentence"] = jdata[dataid]["sentence"]
            extract_results[dataid][target] = {}

            j_entity_keys = [keys for keys in jdata[dataid]["entities"].keys()]
            # print("j_entity_keys>>>", j_entity_keys)

            for tar in targets :
                if type(tar) == list :
                    for tar_ in tar :
                        if tar_ in j_entity_keys :
                            print(tar_)
                            extract_results[dataid][target][tar_] = jdata[dataid]["entities"][tar_]
                else :
                    if tar in j_entity_keys :
                        # print((tar))
                        extract_results[dataid][target][tar] = jdata[dataid]["entities"][tar]

        wpath = doc.replace(input_path, output_path)
        print("wpath>>>", wpath)
        with open(wpath, "w", encoding="utf-8") as fw :
            json.dump(extract_results, fw, indent=4, ensure_ascii=False)
else :
    raise AssertionError("Unknown parsing standard>>", standard)