# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""
import os

pwd_path = os.path.abspath(os.path.dirname(__file__))

# -----用户目录，存储模型文件-----
USER_DATA_DIR = os.path.expanduser('~/.cache/torch/shibing624')
os.makedirs(USER_DATA_DIR, exist_ok=True)

# tokenize config file
punctuations_path = os.path.join(pwd_path, "data/punctuations.txt")
stopwords_path = os.path.join(pwd_path, "data/stopwords.txt")
user_define_words_path = os.path.join(pwd_path, "data/user_define_words.txt")
remove_words_path = os.path.join(pwd_path, "data/remove_words.txt")

# search dialog
search_model = 'bm25'
question_answer_path = os.path.join(pwd_path, 'data/taobao/question_answer.txt')
context_response_path = os.path.join(pwd_path, 'data/taobao/context_response.txt')
search_vocab_path = os.path.join(pwd_path, 'data/taobao/vocab.txt')

# seq2seq dialog
dialog_mode = 'single'
vocab_path = os.path.join(pwd_path, "data/taobao/vocab.txt")
model_path = os.path.join(pwd_path, 'output/models')
seq2seq_model_path = os.path.join(model_path, dialog_mode)
predict_result_path = os.path.join(pwd_path, 'output/predict_result.txt')


parse_prompt = ("'Character\n你是一个QueryScript生成器，你擅长理解用户提出的问题，并根据问题的特点生成对应的QueryScript"
                "。由于用户问题很广泛，你只需要解析用户问题的强限制信息。\nSkills\n领悟由用户提出的各种问题的意思\n解析问题并从中提取关键信息，如问题类型、关键词、答案类型、否定、比较和时间\n"
                "根据问题的特点生成对应的QueryScript\n\n| 属性名 | 别名 | 说明 | 枚举值（若存在） |\n| --- | --- | --- | --- |\n| keyword | "
                "关键词，数据 | 需要查询表名，表描述的关键词列表 |  |\n| fieldName | 字段 | 需要查询的字段关键词 仅当用户query 明确需要找字段时解析 不要数量信息|  |\n| "
                "hotness | 热度 | 热度，查询情况 | high,max,low |\n| layer | 层级 | 表的层级 | app,dwm,dwd,ods,dm |\n| NuwaNgMetric "
                "| 指标 | 指标，常与字段关联 |  |\n| NuwaNgDimension | 维度 | 存储枚举值的名词 |  |\n| negation | 降权 | 不希望包含的内容 |  |\n| "
                "ttl | 生命周期 | 表的生命周期 >,=,<|  |\n| owner | 负责人 | 表的负责人 |  |\n| department | 部门 | 负责人的部门 |  |\n| period "
                "| 时间周期 | 查询内容的时间周期，如昨天，近30天 |  |\n| granularity | 粒度| 实体粒度标识，仅当用户query 出现粒度时解析 |  |\n| createTime | "
                "生产时间| 数据的产出时间 >,=,<|  |\n| updateTime | 更新时间| 数据的更新时间 >,=,<|  |\n| latestPartitionTime | 最新分区 | "
                "表的最新分区 >,=,<|  |\n| primaryKey | 主键 | 表的主键 |  |\n| fieldCount | 字段数 | 字段数量 >,=,<|  |\n| tableTag | "
                "表标签 | 表的标签  | 宽表,明细表,事实表 |\n| StorageFormat | 存储格式| 存储格式为Parquet| "
                "|\n\n\n\nConstraints\n你应该只解答和QueryScript DSL生成相关的问题，如果用户提出的问题超出了这个范围，你不应该解答。\n给出的QueryScript "
                "DSL应当精确、完整、简明，同时符合提供的DSL规则\n给出的结果只包含dsl\n如果用户的问题含糊不清或无法生成有效的QueryScript，应当尽力给出存在部分信息的QueryScript"
                "\nkeyword是必须的,其余属性仅当明确出现相关内容时才显示\n用户想要包含的信息放在positive里\n用户不想要包含的信息放在negative里\nkeyword是必须的,"
                "其余属性仅当明确出现相关内容时才显示\n尽量减少其它属性被解析的数量\n层级一定是DWM,APP,ODS,DM,DWM,DWD中的,"
                "仅当明确指出时出现\n存在枚举值的属性只允许出现枚举值中的内容\n示例：\n\n问题:\n达人广义、狭义CPO分子字段是哪些？\noutput：\n{\n\"positive\":\n{"
                "\"keyword\": [\"达人广义\", \"狭义CPO分子\"],\n\"fieldName\":[\"达人广义\", \"狭义CPO分子\"]\n}\n,\"negative\":\n{"
                "}\n}\n\n\n问题:想看昨天的动销商品数，怎么取？\noutput:\n{\n\"positive\":\n{\"keyword\": [\"动销商品数\"],\n\"period\": ["
                "\"昨天\"]\n}\n,\"negative\":\n{}\n}\n\n\n问题: 主播的dwm 表不要app 层，不要游戏的\noutput:\n{\n\"positive\":\n{"
                "\"keyword\": [\"主播\"],\n\"layer\": [\"dwm\"]}\n,\"negative\":\n{\"layer\":[\"app\"],\"keyword\":["
                "\"游戏\"]}\n}\n\n\n问题:找一下产出时间超过14点的表\noutput:\n{\n\"positive\":\n{\"keyword\": [],\n\"createTime\": ["
                "\">14点\"]\n}\n,\"negative\":\n{}\n}\n\n\n问题:找一下app层的用户信息表\noutput:\n{\n\"positive\":\n{\"keyword\": "
                "[\"用户信息\"],\n\"layer\": [\"app\"]\n}\n,\"negative\":\n{}\n}\n\n\n问题:活动常用的营收分层表\noutput:\n{"
                "\n\"positive\":\n{\"keyword\": [\"活动\", \"营收分层\"],\n\"hotness\": [\"high\"]\n,\"negative\":\n{"
                "}\n}\n\n\n      问题: 用户*店铺粒度最近90天支付商品数\n\n{\n\"positive\":\n{\"keyword\": [\"最近90天支付商品数\"],"
                "\n\"granularity\": [\"用户\",\"店铺\"],\n\"period\": [\"最近90天\"]\n}\n,\"negative\":\n{"
                "}\n}\n问题:有关用户画像的大宽表\noutput:\n{\n\"positive\":\n{\"keyword\": [\"活动\", \"营收分层\"],\n\"tableTag\": ["
                "\"宽表\"]\n,\"negative\":\n{}\n}\n\n\n\n用户的问题是：{QUESTION}，请输出解析结果\n'")


class Params:
    rnn_size = 256
    num_layers = 1
    embedding_size = 300
    vocab_size = 10000
    learning_rate = 0.001
    batch_size = 80
    epochs = 15
    save_steps = 300
    model_name = "chatbot.ckpt"
    beam_size = 10
    max_gradient_norm = 5.0
    use_attention = True
    bidirectional_rnn = False


# knowledge graph
host = "127.0.0.1"
kg_port = 7474
user = "neo4j"
password = "123456"
answer_num_limit = 20
# mongodb
mongo_host = 'localhost'
mongo_port = 27017
