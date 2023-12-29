from similarities import BertSimilarity


class SemanticSearchBot:
    def __init__(self, model_path="shibing624/text2vec-base-chinese"):
        self.model = BertSimilarity(model_name_or_path=model_path)

    def add_corpus(self, corpus):
        self.model.add_corpus(corpus)

    def search(self, query, topn=3):
        res = self.model.search(query, topn=topn)
        return [(self.model.corpus[key], res.get(0)[key], key) for key in res.get(0).keys()]

# bot = SemanticSearchBot()
# corpus = [
#     '花呗更改绑定银行卡',
#     '我什么时候开通了花呗',
#     '俄罗斯警告乌克兰反对欧盟协议',
#     '暴风雨掩埋了东北部；新泽西16英寸的降雪',
#     '中央情报局局长访问以色列叙利亚会谈',
#     '人在巴基斯坦基地的炸弹袭击中丧生',
# ]
# bot.add_corpus(corpus)
# query = '如何更换花呗绑定银行卡'
# results = bot.search(query, topn=3)
# for result in results:
#     print(f"Text: {result[0]}, Score: {result[1]}")