from Spider_Model import SpiderModel
import unittest
import json


class SpiderModelSavingTestCase(unittest.TestCase):
    def setUp(self):
        self.spider = SpiderModel()

    def test_get_html_code_error(self):
        self.assertRaises(TypeError, self.spider.get_html_code, 123)

    def test_get_htmlcode_to_datastr(self):
        data_from_code = self.spider.get_htmlcode_to_datastr('<a href="http://www.google.com">Test</a>')
        self.assertEqual(data_from_code, "[Test](http://www.google.com)")
        data_from_code = self.spider.get_htmlcode_to_datastr("<h1>My Test</h1>")
        self.assertEqual(data_from_code, "My Test")

    def test_get_htmlcode_to_datastr_Error(self):
        self.assertRaises(TypeError, self.spider.get_html_code, ["12323"])

    def test_get_content_from_datastr_Error(self):
        self.assertRaises(TypeError, self.spider.get_content_from_datastr, [])

    def test_get_content_from_datastr(self):
        data_from_html2text = self.spider.get_content_from_datastr("test case[website](http://www.nintendo.com)")
        self.assertEqual(data_from_html2text, "test case")

    def test_get_website_from_datastr_Error(self):
        self.assertRaises(TypeError, self.spider.get_website_from_datastr, [])

    def test_get_website_from_datastr(self):
        data_from_html2text = self.spider.get_website_from_datastr("test case[website](http://www.nintendo.com)")
        self.assertEqual(data_from_html2text, ["http://www.nintendo.com"])

    def test_get_weblink_from_datastr_Error(self):
        self.assertRaises(TypeError, self.spider.get_weblink_from_datastr, [])

    def test_get_weblink_from_datastr(self):
        data_from_html2text = self.spider.get_weblink_from_datastr("test case[website](http://www.nintendo.com)")
        self.assertEqual(data_from_html2text, "website")

    def test_website_formatter_Error(self):
        self.assertRaises(TypeError, self.spider.website_formatter, [])

    def test_website_formatter(self):
        data_from_formatter = self.spider.website_formatter("http://www.youtube.com/nintendo?id=mario")
        self.assertEqual(data_from_formatter, "http://www.youtube.com/nintendo")
        data_from_formatter = self.spider.website_formatter("/zelda")
        self.assertEqual(data_from_formatter, "")
        data_from_formatter = self.spider.website_formatter("")
        self.assertEqual(data_from_formatter, "")

    def test_get_json_string_for_deep_Error(self):
        self.assertRaises(TypeError, self.spider.get_json_string_for_deep, ['123'],['69'],['re'])

    def test_get_json_string_for_deep(self):
        content_dict = {
            "http://www.nintendo.com": "nintendo",
            "http://www.youtube.com": "youtube"
        }
        website_dict = {
            "http://www.nintendo.com": [
                "http://www.google.com"
            ],
            "http://www.youtube.com": [
                "http://www.facebook.com"
            ]
        }
        data_from_json = self.spider.get_json_string_for_deep("http://www.nintendo.com", website_dict, content_dict)
        json_dict = {
            "http://www.nintendo.com": {
                "www.nintendo.com": {
                    "http://www.nintendo.com": {
                        "content": "nintendo",
                        "website": [
                            "http://www.google.com"
                        ]
                    }
                },
                "www.youtube.com": {
                    "http://www.youtube.com": {
                        "content": "youtube",
                        "website": [
                            "http://www.facebook.com"
                        ]
                    }
                }
            }
        }
        self.assertDictEqual(json.loads(data_from_json), json_dict)

    def test_set_n_used_Error(self):
        self.assertRaises(TypeError, self.spider.set_n_used, ['789'],['AA'])

    def test_set_n_used(self):
        root_website = "http://www.nintendo.com"
        data_dict = {
            "http://www.nintendo.com": {
                "www.nintendo.com": {
                    "http://www.nintendo.com": {
                        "content": "nintendo0 nintendo1",
                        "website": [
                            "http://unity3d.com",
                            "http://www.facebook.com"
                        ]
                    },
                    "http://www.nintendo.com/mario": {
                        "content": "nintendo0",
                        "website": [
                            "http://unity3d.com",
                            "http://www.facebook.com"
                        ]
                    }
                },
                "www.youtube.com": {
                    "http://www.youtube.com": {
                        "content": "youtube0",
                        "website": [
                            "http://www.facebook.com"
                        ]
                    },
                    "http://www.youtube.com/games": {
                        "content": "youtube1",
                        "website": [
                            "http://www.google.com",
                            "http://www.nintendo.com"
                        ]
                    }
                }
            }
        }
        correct_dict = {
            "www.nintendo.com": 1,
            "unity3d.com": 2,
            "www.facebook.com": 3,
            "www.youtube.com": 0,
            "www.google.com": 1
        }
        self.assertDictEqual(self.spider.set_n_used(root_website, data_dict), correct_dict)

    def test_set_avoid_word(self):
        self.assertRaises(TypeError, self.spider.set_avoid_word, {})

    def test_set_n_used_for_indexing(self):
        self.assertRaises(TypeError, self.spider.set_n_used_for_indexing, {})

    def test_indexing_error(self):
        self.assertRaises(TypeError, self.spider.indexing, 123, {})

    def test_change_json_to_dict_Error(self):
        self.assertRaises(TypeError, self.spider.change_json_to_dict, [])

    def test_change_json_to_dict(self):
        json_str = '{' + \
                       '"www.nintendo.com": 1,' + \
                       '"unity3d.com": 2,' + \
                       '"www.facebook.com": 3,' + \
                       '"www.youtube.com": 0,' + \
                       '"www.google.com": 1' + \
                   '}'
        correct_dict = {
                            "www.nintendo.com": 1,
                            "unity3d.com": 2,
                            "www.facebook.com": 3,
                            "www.youtube.com": 0,
                            "www.google.com": 1
                        }
        self.assertDictEqual(self.spider.change_json_to_dict(json_str), correct_dict)

    def test_get_json_string_Error(self):
        self.assertRaises(TypeError, self.spider.get_json_string, ['dota'])

    def test_get_json_string(self):
        correct_dict = {
            u'www.nintendo.com': 1,
            u'unity3d.com': 2,
            u'www.facebook.com': 3,
            u'www.youtube.com': 0,
            u'www.google.com': 1
        }
        self.assertDictEqual(correct_dict, json.loads(self.spider.get_json_string(correct_dict)))

    def test_ranking_Error(self):
        self.assertRaises(TypeError, self.spider.ranking, ['Com'])

    def test_ranking(self):
        data_dict = {
            "nintendo":
                {
                    "http://www.nintendo.com":
                        {
                            "used": 10,
                            "word": 100
                        },
                    "http://www.facebook.com":
                        {
                            "used": 5,
                            "word": 100
                        },
                    "http://twitter.com":
                        {
                            "used": 10,
                            "word": 300
                        },
                }
        }
        correct_dict = {
            "nintendo":
                [
                    (
                        "http://twitter.com", {
                            "used": 10,
                            "word": 300
                        }
                    ),
                    (
                        "http://www.nintendo.com", {
                            "used": 10,
                            "word": 100
                        }
                    ),
                    (
                        "http://www.facebook.com", {
                            "used": 5,
                            "word": 100
                        }
                    )
                ]
        }
        self.assertDictEqual(self.spider.ranking(data_dict), correct_dict)

    def test_get_netloc_Error(self):
        self.assertRaises(TypeError, self.spider.get_netloc, [])

    def test_get_netloc(self):
        website = "http://www.nintendo.com/mario"
        self.assertEqual(self.spider.get_netloc(website), "www.nintendo.com")


if __name__ == '__main__':
    unittest.main()
