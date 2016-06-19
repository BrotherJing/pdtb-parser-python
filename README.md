## Usage

### Environment

- Python 2.7
- Java

```bash
#train
python parser.py train <train_file_name>

#predict
python parser.py predict <test_file_name>

#select features using MI
python parser.py feature
```
The output predict_pdtb.json is the predict result.

If you want to train from new data, delete all things under `/tmp`. If you just want to predict on new data, just delete all files whose name doesn't contains `train` or `model` under `/tmp`.

### 2016.05.29

- generate predict result in file, for later evaluation using `scorer.py`
- add command line arguments

### 2016.05.26

- use `Lemma` for word-pair feature
- add first-last-firstlast3 feature
- F1 measure up to `42.13%`

### 2016.05.24

- parserhelper

### 2016.05.21

- feature extraction
- training
- predicting
