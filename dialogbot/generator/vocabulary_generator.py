import os

import jieba
from collections import Counter

class VocabularyGenerator:
    def __init__(self, path="../dialogbot/data/coral/new", file_name='vocab.txt'):
        self.path = path
        self.file_name = file_name

    def generate_vocab(self, text):
        word_counts = self.extract_words(text)
        # Check if the directory exists, if not create it
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        # Check if the file exists, if not create it and write words into it
        # If it exists, append words at the end of the file
        file_path = os.path.join(self.path, self.file_name)
        result = ""
        with open(file_path, 'a') as f:
            for word, count in word_counts:
                f.write(word + '\t' + str(count) + '\n')
                result = result + word + '\t' + str(count) + '\n'
        return result

    def extract_words(self, text):
        # Use jieba to segment the text
        words = jieba.lcut(text)
        word_counts = Counter(words)
        word_counts = word_counts.most_common()
        return word_counts
