from Spider_Model import SpiderModel
import unittest
import json
import os
from nodebox.graphics.physics import Graph      # Library use to draw graph

class SpiderModelSavingTestCase(unittest.TestCase):
    def setUp(self):
        self.spider = SpiderModel()

    def test_get_html_code_error(self):
        self.assertRaises(TypeError, self.spider.get_html_code, 123)

    def test_get_htmlcode_to_datastr(self):
        data_from_code = self.spider.get_html_code_to_datastr('', '<a href="http://www.google.com">Test</a>')
        self.assertEqual(data_from_code, "[Test](http://www.google.com)")
        data_from_code = self.spider.get_html_code_to_datastr("", "<h1>My Test</h1>")
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
        self.assertDictEqual(data_from_json, json_dict)

    def test_set_n_used_Error(self):
        self.assertRaises(TypeError, self.spider.set_n_used, ['789'], ['AA'])

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
                            "http://www.youtube.com",
                            "http://www.nintendo.com",
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

    """def test_set_n_used_for_indexing(self):
        self.assertRaises(TypeError, self.spider.set_n_used_for_indexing, {})"""

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

    def test_total(self):
        root_website = "http://www.meawnam.com"
        file_data = open(os.getcwd() + "\\Spider\\other\\test_total.html", "r+")
        html_code = file_data.read()
        file_data.close()
        data_str_html = self.spider.get_html_code_to_datastr(root_website, html_code)
        self.assertEqual(data_str_html, "GAMEBOY  [GOOGLE](http://www.google.com) "
                                        "[electric](http://www.electric.com) "
                                        "[spotlight](http://www.spotlight.com)")
        content_html = self.spider.get_content_from_datastr(data_str_html)
        self.assertEqual(content_html, "GAMEBOY")
        weblink_html = self.spider.get_weblink_from_datastr(data_str_html)
        self.assertEqual(weblink_html, "GOOGLE electric spotlight")
        website_list = self.spider.get_website_from_datastr(data_str_html)
        self.assertListEqual(website_list, ["http://www.google.com", "http://www.electric.com",
                                            "http://www.spotlight.com"])
        dict_json = {
            root_website: {
                self.spider.get_netloc(root_website): {
                    root_website: {
                        "content": content_html + " " + weblink_html,
                        "website": website_list
                    }
                }

            }
        }
        content_dict = {
            root_website: content_html + " " + weblink_html
        }
        website_dict = {
            root_website: website_list
        }
        self.assertDictEqual(self.spider.get_json_string_for_deep(root_website, website_dict, content_dict), dict_json)

        graph = Graph()
        graph.add_node("www.meawnam.com")
        graph.add_node("www.google.com")
        graph.add_node("www.electric.com")
        graph.add_node("www.spotlight.com")
        graph.add_edge("www.meawnam.com", "www.google.com")
        graph.add_edge("www.meawnam.com", "www.electric.com")
        graph.add_edge("www.meawnam.com", "www.electric.com")
        graph.add_edge("www.meawnam.com", "www.spotlight.com")
        self.assertEqual(graph, self.spider.set_into_graph(root_website, dict_json))

        dict_n_used = {
            "www.meawnam.com": 0,
            "www.google.com": 1,
            "www.electric.com": 1,
            "www.spotlight.com": 1
        }
        self.assertEqual(dict_n_used, self.spider.set_n_used(root_website, dict_json))

        save_file = open(os.getcwd() + "\\Spider\\other\\test_index_total.json", "w+")
        save_file.write(json.dumps(dict_json, indent=4, sort_keys=True))
        save_file.close()
        file_list = [os.getcwd() + "\\Spider\\other\\test_index_total.json"]
        index_dict = self.spider.indexing({}, file_list)
        my_indexing = {
            "gameboy": {
                "http://www.meawnam.com": {
                    "used": 0,
                    "word": 1
                }
            },
            "google": {
                "http://www.meawnam.com": {
                    "used": 0,
                    "word": 1
                }
            },
            "electric": {
                "http://www.meawnam.com": {
                    "used": 0,
                    "word": 1
                }
            },
            "spotlight": {
                "http://www.meawnam.com": {
                    "used": 0,
                    "word": 1
                }
            }
        }
        self.assertDictEqual(index_dict, my_indexing)

        ranking_dict = self.spider.ranking(index_dict)
        my_ranking = {
            "gameboy":
                [
                    (
                        "http://www.meawnam.com", {
                            "used": 0,
                            "word": 1
                        }
                    )
                ],
            "google":
                [
                    (
                        "http://www.meawnam.com", {
                            "used": 0,
                            "word": 1
                        }
                    )
                ],
            "electric":
                [
                    (
                        "http://www.meawnam.com", {
                            "used": 0,
                            "word": 1
                        }
                    )
                ],
            "spotlight":
                [
                    (
                        "http://www.meawnam.com", {
                            "used": 0,
                            "word": 1
                        }
                    )
                ]
        }
        self.assertDictEqual(ranking_dict, my_ranking)

if __name__ == '__main__':
    unittest.main()
