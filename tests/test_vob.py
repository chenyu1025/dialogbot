import unittest

from dialogbot.generator.vocabulary_generator import VocabularyGenerator


class TemplateSearchCase(unittest.TestCase):
    def test_something(self):
        generator = VocabularyGenerator()
        print(generator)

        text = '''直播间切片语音数据（不是转成文本后的数据）如何获取 宿主：汽水需求：推荐侧如果要召回用户在抖音内历史14日消费主播，用哪一个底表 站内信和关播页的数据在哪里可以取到？ 节目直播场次表离线是否有小时级的表
咱们能区分出来，因为主播连屏引流产生的关注粉丝吗？
主播平均每场pk的在线人数，如何获取'''
        r = generator.generate_vocab(text)
        print('vob', text, r)


if __name__ == '__main__':
    unittest.main()
