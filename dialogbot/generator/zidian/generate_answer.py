import json
import os
import re
import numpy as np
import jieba

with open('data/category_dict_l2.json', 'r') as f:
    category_dict_l2 = json.load(f)

path = "category"
file_name = "question_answer.txt"
voca_file = "category/vocab.txt"
with open(voca_file, 'r') as f:
    voca = f.readlines()
voca_list = []
for item in voca:
    voca_list.append(item.split("\t")[0])
file_path = os.path.join(path, file_name)
with open(file_path, 'a') as f:
    for item in category_dict_l2:
        text = category_dict_l2[item]
        text = re.sub(r'[^\w\s]', ' ', text)
        words = jieba.lcut(text)
        if not os.path.exists(path):
            os.makedirs(path)

        # Check if the file exists, if not create it and write words into it
        # If it exists, append words at the end of the file
        file_path = os.path.join(path, file_name)
        for word in words:
            if word == " ":
                continue
            word = word.replace('\t','')
            word = word.replace('\n','')
            if word not in voca_list:
                continue
            f.write(word + ' ')

        f.write('\t' + item + '\n')
