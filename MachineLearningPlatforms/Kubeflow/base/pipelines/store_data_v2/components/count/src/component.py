#!/usr/bin/env python3

# component.py
# component is a simple component wrapper of data preparation step
# Notice: In this case I assume to read data from Cloud Storage.
# You have both pure storage APIs or tf. gfile.
# For portability, I prefer tf.gfile because you can debug your model
# locally and train it on cloud without changing a single line.

from tensorflow import gfile

# Helpers --------------------------------------------------------------------------------------------------------------
def load_text(file_path: str) -> str:
    with gfile.Open(file=file_path, mode='r') as file:
        text = file.read().replace("\n", " ")
    file.close()
    return text

def store_data(word_list: list, out_path_pkl: str):
    with gfile.Open(out_path_pkl, 'w') as file:
        pickle.dump(word_list, file)


    text_path = args.text_path
    out_path_pkl = args.path_pkl
    text = load_text(file_path=text_path)