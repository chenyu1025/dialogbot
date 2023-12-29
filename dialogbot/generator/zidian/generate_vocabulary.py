import json
import re

from dialogbot.generator.vocabulary_generator import VocabularyGenerator

with open('data/category_dict_l1.json', 'r') as f:
    category_dict_l1 = json.load(f)

vocabulary_generator = VocabularyGenerator(path="category", file_name='vocab.txt')
text = ""
for item in category_dict_l1:
    text = text + category_dict_l1[item]

text = re.sub(r'[^\w\s]', ' ', text)
vocabulary_generator.generate_vocab(text)
