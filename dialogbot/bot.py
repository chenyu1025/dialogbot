# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: chat bot main process.
"""
import os

from dialogbot import config
from dialogbot.gpt.gptbot import GPTBot
from dialogbot.search.searchbot import SearchBot
from dialogbot.utils.io import save_json, load_json
from dialogbot.utils.log import logger
from dialogbot.utils.text_util import ch_count


class Bot:
    def __init__(self,
                 vocab_path=config.vocab_path,
                 search_model=config.search_model,
                 question_answer_path=config.question_answer_path,
                 context_response_path=config.context_response_path,
                 gpt_model_dir=config.gpt_model_dir,
                 use_cache=True,
                 cache_path=config.cache_path,
                 cache_save_per_size=10,
                 context=None
                 ):
        self.context = context if context else []
        self.search_bot = SearchBot(question_answer_path, context_response_path,
                                    vocab_path=vocab_path,
                                    search_model=search_model)

        self.gpt_bot = GPTBot(gpt_model_dir)
        self.use_cache = use_cache
        self.cache_save_per_size = cache_save_per_size
        self.cache_path = cache_path
        self.cache = {}
        if use_cache and os.path.exists(cache_path):
            self.cache = load_json(cache_path)
            logger.info("use cache, cache file: %s" % cache_path)

    def set_context(self, v):
        if isinstance(v, list):
            self.context = v
        elif isinstance(v, str):
            self.context = [v]
        else:
            self.context = []

    def answer(self, query, use_search=True, use_gen=False, use_task=False):
        """
        Dialog strategy: use sub-task to handle dialog firstly,
        if failed, use retrieval or generational func to handle it.
        :param query: str, input query
        :param use_search: bool, weather or not use search bot, include local search and internet search
        :param use_gen: bool, weather or not use seq2seq bot
        :param use_task: bool, weather or not use task bot
        :return: (response, details) str, []
        """
        self.context.append({'user:': query})
        response = {}
        if self.use_cache and query in self.cache:
            response = self.cache[query]
        else:
            if use_task:
                task_response = ''
                response['task_response'] = task_response

            # Search response
            if use_search:
                if len(self.context) >= 3 and ch_count(query) <= 4:
                    # user_msgs = self.context[::2][-3:]
                    # msg = "<s>".join(user_msgs)
                    # mode = "cr"
                    mode = "qa"
                else:
                    mode = "qa"
                search_response, sim_score = self.search_bot.answer(query, mode=mode)
                response['search_response'] = search_response

            # GPT2 response
            if use_gen:
                gen_response = self.gpt_bot.answer(query)
                response['gen_response'] = gen_response

        self.context.append({'bot:': response})
        if self.use_cache:
            self.cache[query] = response
            if len(self.cache) % self.cache_save_per_size == 0:
                save_json(self.cache, self.cache_path)

        return response
