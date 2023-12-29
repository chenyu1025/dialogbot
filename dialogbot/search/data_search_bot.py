import os
from collections import deque

from loguru import logger

from dialogbot.search.data_search.search_engine import DataSearchEngine


class DataSearchBot:
    def __init__(
            self,
            search_model='template-search',
            last_txt_len=100,
            search_type='data',
            intention='FIND_TABLE_HIVE_TABLE'
    ):
        self.search_model = search_model
        self.last_txt = deque([], last_txt_len)
        self.search_type = search_type
        self.intention = intention
        # search engine
        self.data_answers_inst = DataSearchEngine()

    def answer(self, query, business_line=""):
        self.last_txt.append(query)
        if self.search_type == 'data':
            response, score = self.data_search(query, business_line)
            if response:
                self.last_txt.append(response)
                return response, score

    def search_k(self, query, business_line=""):
        data_answers = self.data_answers_inst.search(query, business_line, self.intention)
        if data_answers:
            response = data_answers[0]
            return response, response['rankingScore']
        return "", 0.0

    def data_search(self, query, business_line):
        data_answers = self.data_answers_inst.search(query, business_line, self.intention)
        if data_answers:
            response = data_answers[0]
            return response, response['rankingScore']
        return "", 0.0
