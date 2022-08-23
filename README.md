# chinese_dependency_parsing_toolkits
Collection of CKIP transformers, Spacy, UD-Kanbun, DDparser, for turning texts into structured data. (save in json)


## CKIP Han Transformers
- Sample input direction: `testin/`
- Sample output direction: `testout/shiji_max128_ckip/`
- Sample command: `python ckip.py -i testin -o testout --lang han-chinese`

## UD-Kanbun
- Requirement: 
  ```
  # Ubuntu (for windows, suggest to create an anaconda environment)
  pip install udkanbun
  pip install spacy==2.1.0
  pip install MeCab
  pip install supar
  ```
- Sample input direction: `testin/`
- Sample output direction: `testout/shiji_max128_udkb/`
- Sample command: `python .\run_udkanbun.py -i testin/ -o testout/shiji_max128_udkb`
