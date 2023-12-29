import unittest

from dialogbot.search.data_search_bot import DataSearchBot


class TemplateSearchCase(unittest.TestCase):
    def test_something(self):
        bot = DataSearchBot()
        print(bot)

        msgs = [['dwm trd ecom shop order', "中国区电商"],
                ]
        for msg in msgs:
            r = bot.answer(msg[0],msg[1])
            print('search', msg, r[0])


if __name__ == '__main__':
    unittest.main()
