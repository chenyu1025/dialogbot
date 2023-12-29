import unittest

from dialogbot.gpt.gptClient import GptClient
from dialogbot.gpt.prompt.prompt import query_understanding_prompt


class TemplateSearchCase(unittest.TestCase):
    def test_something(self):
        bot = GptClient()
        print(bot)
        prompt = query_understanding_prompt
        msg = [{"content": prompt.replace("{QUESTION}", "直播间切片语音数据（不是转成文本后的数据）如何获取"), "role": "user"}]
        r = bot.get_answer(msg)
        print('gpt answer', msg, r)


if __name__ == '__main__':
    unittest.main()
