import unittest
from AddPhoneticSymbolForArticel import youdao



class TestYouDao(unittest.TestCase):
    def test_basicFunction(self):
        testWords = ["hello","it's"]
        expectedResults = ["[həˈlo]", "[ɪts]"]
        for (word,expectedResult) in zip(testWords, expectedResults):
            self.assertEqual(youdao.CheckSymbolFromYoudao(word), expectedResult)
