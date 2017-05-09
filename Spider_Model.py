from nodebox.graphics.physics import Graph      # Library use to draw graph
import urllib2       # Library for get HTML code
import html2text    # Library for change HTML code to text
import re           # Set format or replace word
import json         # Save json format
from urlparse import urlparse       # Set website format
import operator


class SpiderModel:
    """ Manage data from webpage """
    def __init__(self):
        print "start : init : SpiderModelSaving"
        self.html2text = html2text.HTML2Text()   # set html2text
        self.html2text.ignore_links = False      # care link
        self.html2text.ignore_images = True      # don't care image
        self.html2text.ignore_tables = True      # don't care table
        self.avoid_file = ["indexing.json", "deep_save.json"]
        self.data_dict = {}
        print "complete : init : SpiderModelSaving"

    def reset_init(self):
        print "start : reset_init : SpiderModelSaving"
        self.html2text = html2text.HTML2Text()  # set html2text
        self.html2text.ignore_links = False  # care link
        self.html2text.ignore_images = True  # don't care image
        self.html2text.ignore_tables = True  # don't care table
        self.avoid_file = []
        self.data_dict = {}
        print "complete : reset_init : SpiderModelSaving"

    # Method to get HTML code (website)
    def get_html_code(self, website, t=3):
        print "start : get_html_code : SpiderModelSaving"
        if type(website) != str:
            raise TypeError("Type Error input is not string")
        if t == 0:
            return ""
        try:
            in_website = website
            in_website = self.website_formatter(in_website)
            html_code = urllib2.urlopen(in_website).read()      # use urllib for this website
            print "complete : get_html_code : SpiderModelSaving"
            html_code = html_code.decode("utf-8", "ignore").encode("ascii", "ignore")
            return html_code                        # return html code
        except:                             # Detect error
            print "Error : get_html_code : SpiderModelSaving"
            return self.get_html_code(website, t-1)                               # return no word

    # Method to get content, website from html (html2text object, html code)
    def get_html_code_to_datastr(self, website, html_code, t=3):
        if type(html_code) != str:
            raise TypeError("Type Error input is not string")
        print "start : get_htmlcode_to_datastr : SpiderModelSaving"
        if t == 0:
            return ""
        if html_code == "":     # detect no word
            print "no word : get_htmlcode_to_datastr : SpiderModelSaving"
            return ""           # exit this method
        try:
            # Set data from html code
            data_str = re.sub(r'<script(.*?)</script>', " ", html_code).strip()
            data_str = re.sub(r'<noscript(.*?)</noscript>', " ", data_str).strip()
            data_str = re.sub(r'<style(.*?)</style>', " ", data_str).strip()
            data_str = re.sub(r'<\?(.*?)\?>', " ", data_str).strip()
            data_str = self.html2text.handle(data_str).encode("ascii", "ignore")
            data_str = re.sub("[\n\t*#_]", " ", data_str).strip()  # make string
            print "complete : get_htmlcode_to_datastr : SpiderModelSaving"
            return data_str                         # Delete all space for data and return
        except:
            print "Error : get_htmlcode_to_datastr : SpiderModelSaving on " + website
            return self.get_html_code_to_datastr(website, html_code, t-1)  # return no word


    # Method to get content from datastring (data string)
    @staticmethod
    def get_content_from_datastr(datastr):
        if type(datastr) != str:
            raise TypeError("Type Error input is not string")
        print "start : get_content_from_datastr : SpiderModelSaving"
        if len(datastr) == 0:                                                 # detect no word
            print "no word : get_content_from_datastr : SpiderModelSaving"
            return ""
        data_del_website = re.sub(r'\((.*?)\)', " ", datastr)                 # delete word in (website)
        data_del_web_content = re.sub(r'\[(.*?)\]', " ", data_del_website)    # delete word in [content_weblink]
        if data_del_web_content.strip() != "":                                # detect data has word
            print "complete : get_content_from_datastr : SpiderModelSaving"
            return re.sub(r'[^a-zA-Z]', " ", data_del_web_content).strip()    # strip space and return content
        return ""

    # Method to get website from datastring (data string)
    def get_website_from_datastr(self, datastr):
        print "start : get_website_from_datastr : SpiderModelSaving"
        if type(datastr) != str:
            raise TypeError("Type Error input is not string")
        if datastr == "":                                                    # not detect word
            print "no word : get_website_from_datastr : SpiderModelSaving"
            return []
        list_website = []                                                    # list that save website
        website_list = re.findall(r'\((.*?)\)', datastr)                     # split website(in ()) to list
        for web in website_list:
            web_del_website = re.sub("\"(.*?)\"", " ", web).strip()           # delete word in ()
            web_del_website_format = self.website_formatter(web_del_website)    # Set format to website
            if web_del_website_format != "":    # detect website
                list_website.append(web_del_website_format)                  # add in list
        print "complete : get_website_from_datastr : SpiderModelSaving"
        return list_website                                                  # return list

    @staticmethod
    # Method to get content is linked from datastring (data string)
    def get_weblink_from_datastr(datastr):
        print "start : get_weblink_from_datastr : SpiderModelSaving"
        if type(datastr) != str:
            raise TypeError("Type Error input is not string")
        if datastr == "":                                           # not detect word
            print "no word : get_weblink_from_datastr : SpiderModelSaving"
            return ""                                               # return no word
        all_content = ""                                            # Save all content in this
        data_del_web = re.sub(r'\((.*?)\)', " ", datastr)           # data delete word in () or website
        content_list = re.findall(r'\[(.*?)\]', data_del_web)       # list word in [] or content that is linked
        for content in content_list:                                # get content in list
            if content.strip() != "":                               # detect content
                all_content += re.sub(r'[^a-zA-Z]', " ", content).strip() + " "                # save all content in one
        print "complete : get_weblink_from_datastr : SpiderModelSaving"
        return all_content.strip()

    # Method that set json string to text file (root website, dict of website, dict of content)
    def get_json_string_for_deep(self, root_website, website_dict, content_dict, t=3):
        print "start : get_json_string : Spider_model_saving"
        if type(root_website) != str or type(website_dict) != dict or type(content_dict) != dict:
            raise TypeError("Type Error input is not type match")
        if t == 0:
            return ""
        root_netloc = self.get_netloc(root_website)                         # get netloc of root website
        if self.data_dict == {}:
            self.data_dict = {root_website: {root_netloc: {root_website: {}}}}    # dict that save to json file
        try:
            for website in content_dict:                                        # get website in content dict.
                website_netloc = self.get_netloc(website)                       # get netloc of website
                if not website_dict.get(website):                               # no item in list
                    continue
                if website_netloc not in self.data_dict[root_website]:  # detect this netloc not in dict
                    self.data_dict[root_website][website_netloc] = {website: {}}  # set netloc in dict
                self.data_dict[root_website][website_netloc][website] = {         # set content and child-website in dict
                    "content": content_dict.get(website),                       # content
                    "website": website_dict.get(website)                        # list of child-website
                }
        except:
            print "Error : get_json_string : SpiderModelSaving"
            self.get_json_string_for_deep(root_website, website_dict, content_dict, t-1)
        print "complete : get_json_string : SpiderModelSaving"
        return self.data_dict                                                 # set dict to json string and return

    @staticmethod
    def content_website_dict_from_json(file_manager, model, website):
        content_dict = {}
        website_dict = {}
        data_dict = json.loads(file_manager.read_website_file(model, website))
        for root_website in data_dict:
            root_website = root_website.encode("ascii", "ignore")
            for netloc in data_dict[root_website]:
                netloc = netloc.encode("ascii", "ignore")
                for website in data_dict[root_website][netloc]:
                    website = website.encode("ascii", "ignore")
                    content_dict[website] = data_dict[root_website][netloc][website]["content"]
                    website_dict[website] = data_dict[root_website][netloc][website]["website"]
        return content_dict, website_dict

########################################################################################################################

    """ Manage data for showing """
    def set_into_graph(self, root_website, json_dict):
        print "start : set_into_graph : SpiderModelShowing"
        if type(root_website) != str or type(json_dict) != dict:
            raise TypeError("Type Error input is not type match")
        show_graph = Graph()  # graph to draw

        for netloc_uni in json_dict[root_website]:  # use netloc in json_dict
            netloc = netloc_uni.encode("ascii", "ignore")  # change unicode to string
            for website_uni in json_dict[root_website][netloc]:  # use website in json_dict
                website = website_uni.encode("ascii", "ignore")  # change unicode to string
                if self.get_netloc(website) != "":  # netloc has word
                    show_graph.add_node(self.get_netloc(website))  # add netloc in draw graph

                # use child website
                for child_website_uni in json_dict[root_website][netloc][website]["website"]:
                    child_website = child_website_uni.encode("ascii", "ignore")

                    # add netloc of child website into draw graph
                    if self.get_netloc(child_website) != "":
                        show_graph.add_node(self.get_netloc(child_website))

                    # detect netloc of website and child-website is not same
                    if self.get_netloc(website) != self.get_netloc(child_website) \
                            and self.get_netloc(website) != "" \
                            and self.get_netloc(child_website) != "":

                        # add edge website to child-website to draw graph
                        show_graph.add_edge(self.get_netloc(website), self.get_netloc(child_website))
        print "complete : set_into_graph : SpiderModelShowing"
        return show_graph

    def set_n_used(self, root_website, json_dict):
        print "start : set_n_used : SpiderModelShowing"
        dict_netloc_used = {}
        if type(root_website) != str or type(json_dict) != dict:
            raise TypeError("Type Error input is not type match")
        for netloc in json_dict[root_website]:  # use netloc in json_dict
            netloc = netloc.encode("ascii", "ignore")  # change unicode to string
            if netloc not in dict_netloc_used:  # netloc not in dict used
                dict_netloc_used[netloc] = 0  # set netloc in dict and set 0
            for website in json_dict[root_website][netloc]:  # get website in dict
                website = website.encode("ascii", "ignore")  # change unicode to string
                # netloc has word
                if self.get_netloc(website) != "" and self.get_netloc(website) not in dict_netloc_used:
                    dict_netloc_used[self.get_netloc(website)] = 0
                # get child website in list
                for child_website in json_dict[root_website][netloc][website]["website"]:
                    child_website = child_website.encode("ascii", "ignore")  # encode website
                    # child's netloc not in dict used
                    if self.get_netloc(child_website) not in dict_netloc_used:
                        dict_netloc_used[self.get_netloc(child_website)] = 0  # set netloc in dict and set 0
                    # child's netloc and website's netloc is not same
                    if self.get_netloc(child_website) != netloc:
                        dict_netloc_used[self.get_netloc(child_website)] += 1  # add value in used dict
        print "complete : set_n_used : SpiderModelShowing"
        return dict_netloc_used

    """ Manage for indexing """
    # save avoid word from text file into dict
    @staticmethod
    def set_avoid_word(file_name):
        print "start : set_avoid_word : SpiderModelIndexing"
        if type(file_name) != str:
            raise TypeError("Type Error input is not string")
        avoid_word_file = open(file_name, "r+")  # open file
        avoid_word = {}  # dict of words
        for word in avoid_word_file:  # get word from avoid word file
            word = word.strip()  # delete space
            avoid_word[word] = {}  # set word in list
        avoid_word_file.close()  # close file
        print "complete : set_avoid_word : SpiderModelIndexing"
        return avoid_word

    # method is used to set number of this website is used
    def set_n_used_for_indexing(self, file_list):
        print "start : set_n_used : SpiderModelIndexing"
        if type(file_list) != list:
            raise TypeError("Type Error input is not list")
        dict_n_ref = {}                                                     # reset dict of n_ref
        for file_name in file_list:                                         # get file in current file
            surname_file = file_name[file_name.find(".") + 1:]              # get surname of file
            if surname_file == "json" and file_name not in self.avoid_file: # detect python name
                read_file = open(file_name, "r+")                           # read file
                try:
                    json_dict = json.loads(read_file.read())                    # set json dict
                except ValueError:
                    print "Value Error at Indexing"
                    return dict_n_ref
                for root_website in json_dict:                              # get root website
                    root_website = str(root_website.decode("ascii", "ignore"))        # change type of string
                    for netloc in json_dict[root_website]:                  # use netloc in json_dict
                        netloc = netloc.encode("ascii", "ignore")           # change unicode to string
                        for website in json_dict[root_website][netloc]:     # get website in dict
                            website = website.encode("ascii", "ignore")               # change unicode to string
                            if website not in dict_n_ref:              # detect website in dict
                                dict_n_ref[website] = 0                # set website in dict and set 0
                            # get child website in list
                            # print root_website, netloc, website
                            if "website" not in json_dict[root_website][netloc][website]:
                                continue
                            for child_website in json_dict[root_website][netloc][website]["website"]:
                                child_website = child_website.encode("ascii", "ignore")
                                # child website not in dict used
                                if child_website not in dict_n_ref:
                                    dict_n_ref[child_website] = 0      # set website in dict and set 0
                                # child's netloc and website's netloc is not same
                                child_netloc = self.get_netloc(child_website)
                                # detect child netloc not same website netloc
                                if child_netloc != netloc:
                                    dict_n_ref[child_website] += 1     # add value in used dict
                read_file.close()                                           # close file
        print "complete : set_n_used : SpiderModelIndexing"
        return dict_n_ref

    def indexing(self, avoid_word, file_list, indexing_dict=None):
        print "start : indexing : SpiderModelIndexing"
        if type(avoid_word) != dict or type(file_list) != list:
            raise TypeError("Type Error some input is not list")
        if indexing_dict is None:
            indexing_dict = {}
        dict_n_ref = self.set_n_used_for_indexing(file_list)

        print file_list

        for file_name in file_list:                         # get file in current file
            surname_file = file_name[file_name.find("."):]  # get surname of file
            if surname_file != ".json" or file_name in self.avoid_file:  # detect python name
                continue
            read_file = open(file_name, "r+")  # read file\
            data = read_file.read()
            if data == "":
                continue
            json_dict = self.change_json_to_dict(data)        # set json dict
            update_dict = {}
            for root_website in json_dict:  # get root website
                root_website = str(root_website.decode("ascii", "ignore"))  # get root website in string
                for netloc in json_dict[root_website]:  # netloc list
                    netloc = str(netloc.decode("ascii", "ignore"))  # get netloc string
                    for website in json_dict[root_website][netloc]:  # get website list
                        website = str(website.decode("ascii", "ignore"))  # get website string

                        if "content" not in json_dict[root_website][netloc][website]:
                            continue
                        content = json_dict[root_website][netloc][website]["content"]  # get content
                        content = content.encode("ascii", "ignore").lower()  # encode and lower
                        list_word = content.split()  # list of word in content
                        for word in list_word:  # loop word in list
                            word = re.sub(r'[^a-zA-Z]', " ", word)  # remove non-word and non-digit
                            if word == "" or word == "\s" or word in avoid_word:
                                continue
                            n_ref = dict_n_ref[website]  # get n_ref
                            n_word = content.count(word)  # get number of word in website into dict
                            if word not in indexing_dict:
                                indexing_dict[word] = {}
                            indexing_dict[word][website] = {"used": n_ref, "word": n_word}

                            if word not in update_dict:
                                update_dict[word] = {}
                            update_dict[word].update({website: {}})

                        for word in update_dict:
                            if website not in update_dict[word] and website in update_dict[word]:
                                del(indexing_dict[word][website])
            read_file.close()  # close file
        print "complete : indexing : SpiderModelIndexing"
        return indexing_dict

    @staticmethod
    def change_json_to_dict(json_str):
        print "start : change_json_to_dict : SpiderModelIndexing"
        if type(json_str) != str:
            raise TypeError("Type Error input is not list")
        json_dict = json.loads(json_str)        # change string to dict
        print "complete : change_json_to_dict : SpiderModelIndexing"
        return json_dict

    # save in indexing into string
    @staticmethod
    def get_json_string(indexing_dict):
        print "start : get_json_string : SpiderModelIndexing"
        if type(indexing_dict) != dict:
            raise TypeError("Type Error input is not dict")
        json_str = json.dumps(indexing_dict, indent=4, sort_keys=True)  # change dict to string json
        print "complete : get_json_string : SpiderModelIndexing"
        return json_str

    """ Manage data for ranking """
    @staticmethod
    def ranking(indexing_dict):
        print "start : ranking : SpiderModelRanking"
        if type(indexing_dict) != dict:
            raise TypeError("Type Error input is not dict")
        ranking_dict = {}
        for word in indexing_dict:  # get word from list
            # sort data
            ranking_dict[word] = sorted(indexing_dict[word].items(), key=operator.itemgetter(1), reverse=True)
        print "complete : ranking : SpiderModelRanking"
        return ranking_dict

    # method that get netloc from website (website)
    @staticmethod
    def get_netloc(website):
        if type(website) != str:
            raise TypeError("Type Error input is not string")
        # print "complete : get_netloc : SpiderModelSaving"
        return urlparse(website).netloc.encode("ascii")

    @staticmethod
    # Method that set website format (scheme, netloc and path)
    def website_formatter(website):
        # print "start : website_formatter : SpiderModelSaving"
        if type(website) != str:
            raise TypeError("Type Error input is not string")
        if len(website) > 0:  # Detect website
            parsed_uri = urlparse(website)  # Get website par
            if parsed_uri.scheme == "" or parsed_uri.netloc == "":  # Detect website has not scheme or netloc
                # print "no word : website_formatter : SpiderModelSaving"
                return ""  # return no word

            # Set website format that has scheme, netloc, path only and return it
            # print "complete : website_formatter : SpiderModelSaving"
            return ('{uri.scheme}://{uri.netloc}{uri.path}'.format(uri=parsed_uri)).strip("/")
        # print "no word : website_formatter : SpiderModelSaving"
        return ""

    # method that get website no scheme from website (website)
    @staticmethod
    def get_website_no_scheme(website):
        if type(website) != str:
            raise TypeError("Type Error input is not string")
        # print "complete : get_netloc : SpiderModelSaving"
        parsed_uri = urlparse(website)
        return ('{uri.netloc}{uri.path}'.format(uri=parsed_uri)).strip("/")
