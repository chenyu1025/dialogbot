# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description:
"""
import sys

sys.path.append('..')
from dialogbot.search.searchbot import SearchBot

if __name__ == '__main__':
    bm25bot = SearchBot(question_answer_path='../dialogbot/data/coral/background/question_answer.txt',
                        vocab_path='../dialogbot/data/coral/background/vocab.txt',
                        search_model="bm25",
                        top_k=1)

    msgs = ['分区问题删除']
    for msg in msgs:
        search_response, sim_score = bm25bot.answer(msg, use_internet=False, use_local=True)
        print('bm25bot', msg, search_response, sim_score)

