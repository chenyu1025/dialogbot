import jieba

from dialogbot.config import parse_prompt
from dialogbot.gpt.gptClient import GptClient
from dialogbot.search.data_search.search_engine import DataSearchEngine
from dialogbot.search.match_search_bot import ExactMatchBot
from dialogbot.search.semantic_search_bot import SemanticSearchBot
from dialogbot.utils.text_util import parse_result_from_str, read_txt_file


class ChatBot:
    def __init__(self, business_line="中国区电商", granularity_corpus_path="", granularity_match_corpus_path=""):
        self.field_search_bot = None
        self.conversation = []
        self.middle_result = []
        self.round = 0
        self.search_bot = DataSearchEngine()

        self.gpt_client = GptClient()
        self.business_line = business_line
        print("coral 对话机器人 业务线： ", business_line)

        self.body = {"templateName": "CORAL_LLM", "query": "", "offset": 0, "limit": 10,
                     "typeNames": ["HiveTable"],
                     "attributeValuesMap": {"businessLine": ["中国区电商"]}}
        self.granularity_corpus = read_txt_file(granularity_corpus_path)
        self.granularity_match_corpus = read_txt_file(granularity_match_corpus_path)
        self.granularity_bot = ExactMatchBot(self.granularity_corpus, self.granularity_match_corpus)
        self.current_parse_query = {}

    def get_granularity(self, question):
        granularity = None
        if 'positive' in self.current_parse_query:
            if 'granularity' in self.current_parse_query['positive']:
                granularity = self.current_parse_query['positive']['granularity']
        if granularity is None:
            granularity = []
        granularity_list = []
        granularity_result = []
        if len(granularity) > 0:
            for word in granularity:
                temp = jieba.lcut(word, cut_all=False)
                granularity_list = granularity_list + temp
                granularity_result = self.granularity_bot.search(granularity_list)
            print("识别到粒度:", granularity_list)
            print("对应主键: ", granularity_result)
            # 在这里处理用户的问题并返回答案
        # 这只是一个示例，所以我们只是简单地返回用户的问题

        return granularity_result, granularity_list

    def get_granularity_result(self, question, search_result):
        granularity_result, granularity_list = self.get_granularity(question)
        granularity_hit_dict = {}
        for item in search_result:
            if item['qualifiedName'] not in granularity_hit_dict:
                granularity_hit_dict[item['qualifiedName']] = 0
            fields = item['fields']
            for field in fields:
                for word in granularity_result:
                    if word == field['name']:
                        granularity_hit_dict[item['qualifiedName']] += 1
        max_granularity = 0
        for item in granularity_hit_dict:
            if granularity_hit_dict[item] > max_granularity:
                max_granularity = granularity_hit_dict[item]
        return granularity_hit_dict, max_granularity

    def get_answer(self, question):
        self.current_parse_query = self.parse_query(question)
        search_result = self.search_metadata(question)
        granularity_hit_dict, max_granularity = self.get_granularity_result(question, search_result)
        print(granularity_hit_dict)
        k = self.search_field(search_result)
        return k

    def search_field(self, search_result):
        keywords = None
        if 'positive' in self.current_parse_query:
            if 'keyword' in self.current_parse_query['positive']:
                keywords = self.current_parse_query['positive']['keyword']
        if keywords is None:
            keywords = []
        keyword_str = " ".join(keywords)
        field_search_bot, corpus_list, name_list, type_list = self.generate_table_corpus(search_result)
        result = field_search_bot.search(keyword_str, 10)
        for field_result in result:
            item, score, index = field_result
            print(field_result, name_list[index])
        return result

    def generate_table_corpus(self, search_result):
        corpus_list = []
        name_list = []
        type_list = []
        for table in search_result:
            corpus_list.append(table['name'])
            name_list.append(table['qualifiedName'])
            type_list.append('name')
        for table in search_result:
            corpus_list.append(table['alias'])
            name_list.append(table['qualifiedName'])
            type_list.append('alias')

        for table in search_result:
            fields = table['fields']
            for field in fields:
                corpus_list.append(field['name'])
                name_list.append(table['qualifiedName'])
                type_list.append('fieldName')
                corpus_list.append(field['comment'])
                name_list.append(table['qualifiedName'])
                type_list.append('fieldComment')
        field_search_bot = SemanticSearchBot()
        field_search_bot.add_corpus(corpus_list)
        for i in range(len(corpus_list)):
            if corpus_list[i] == 0:
                corpus_list[i] = ""
        return field_search_bot, corpus_list, name_list, type_list

    def clear_conversation(self):
        self.conversation = []
        self.middle_result = []
        self.round = 0
        print("对话已清空")

    def add_to_conversation(self, question, answer):
        self.round += 1
        self.conversation.append((question, answer))
        self.middle_result.append((self.parse_query, []))

    def print_conversation(self):
        print("对话记录: ")
        for i, (question, answer) in enumerate(self.conversation):
            print(f"{i + 1}. 问题: {question}, 回答: {answer}")

    def search_metadata(self, query):
        body = self.body
        body['query'] = query
        search_result = self.search_bot.search_with_body(body)
        return search_result

    def parse_query(self, query):
        prompt = parse_prompt.replace("{QUESTION", query)
        msg = [{"role": "user", "content": prompt}]
        answer = self.gpt_client.get_answer(msg)
        parse_answer = parse_result_from_str(answer)
        return parse_answer

    def run(self):
        while True:
            user_input = input("请输入你的问题 (clear 清空对话 exit 关闭程序): ")
            if user_input.lower() == "clear":
                self.clear_conversation()
            elif user_input.lower() == "exit":
                print("程序已关闭")
                break
            else:
                answer = self.get_answer(user_input)
                self.add_to_conversation(user_input, answer)
                print(answer)
                self.print_conversation()


if __name__ == "__main__":
    bot = ChatBot("中国区电商", "../data/coral/granularity/ecom/corpus.txt",
                  "../data/coral/granularity/ecom/corpus_match.txt")
    bot.run()
