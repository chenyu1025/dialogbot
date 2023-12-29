# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""
import sys

sys.path.append('..')
from dialogbot.search.searchbot import SearchBot

if __name__ == '__main__':
    bm25bot = SearchBot(question_answer_path='../dialogbot/data/coral/category_generate/question_answer.txt',
                        vocab_path='../dialogbot/data/coral/category_generate/vocab.txt',
                        search_model="tfidf",
                        top_k=3)
    granularityBot = SearchBot(question_answer_path='../dialogbot/data/coral/granularity/question_answer.txt',
                        vocab_path='../dialogbot/data/coral/granularity/vocab.txt',
                        search_model="bm25",
                        top_k=3)

    msgs = ['咱们能区分出来，因为主播连屏引流产生的关注粉丝吗？','主播平均每场pk的在线人数，如何获取','汽水需求：推荐侧如果要召回用户在抖音内历史14日消费主播，用哪一个底表','哪张表可以找到的用户的送礼时间','用户打赏主播的明细表，需要知道用户具体的打赏时刻(分钟级别)']
    for msg in msgs:
        search_response, sim_score = bm25bot.answer(msg, use_internet=False, use_local=True)
        print('categoryBot', msg, search_response, sim_score)
        # search_response, sim_score = granularityBot.answer(msg, use_internet=False, use_local=True)
        # print('granularityBot', msg, search_response, sim_score)
