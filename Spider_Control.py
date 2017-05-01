from Spider_Model import SpiderModel  # use save data
from Spider_View import SpiderView  # use GUI and sho graph
from File_Manager import FileManager
import thread  # use thread of program
import time
import json
import os


class SpiderControl:
    def __init__(self):
        self.spider_model = SpiderModel()
        self.spider_view = SpiderView(self.spider_model)
        self.file_manager = FileManager()
        self.root_website = ""
        self.index_website_show = ""
        self.word = ""
        self.content_dict = {}
        self.website_dict = {}
        self.indexing_dict = {}
        self.list_website = []
        self.deep = 0
        self.total_deep = 0
        self.update_dict = {"start": 0, "updating": 1, "complete": 2, "pause": 3}
        self.update_spider_state = self.update_dict["start"]
        self.has_deep_thread = False
        self.thread_deep_count = 0
        self.set_auto_indexing()
        self.file_website_list = self.file_manager.list_website_file()
        self.file_index = -1
        self.max_thread = 100
        self.time_delay = 1
        self.list_web_in_hop = []

        # self.gather_website_all()

    # method that thread of searching website
    def start_search_website_thread(self, website=None):
        if not self.has_deep_thread:  # detect not use thread
            self.spider_model.reset_init()
            thread.start_new_thread(self.start_deep_website, (website, ))  # start thread
            # self.has_deep_thread = True  # set thread is used

    # method that start deep into web
    def start_deep_website(self, website=None):
        self.set_spider_update(self.update_dict["updating"])  # set update text = updating
        self.has_deep_thread = True

        if website is None:
            self.root_website = self.spider_view.get_root_website().encode("ascii", "ignore")  # set root website
            self.root_website = self.spider_model.website_formatter(self.root_website)
            index_website_deep = self.root_website                  # set index website
            self.total_deep = self.spider_view.get_deep()           # get total_deep from GUI
        else:
            self.root_website = website.encode("ascii", "ignore")             # set root website
            self.root_website = self.spider_model.website_formatter(self.root_website)
            index_website_deep = self.root_website                  # set index website
            self.total_deep = 2                                     # get total_deep from GUI

        self.list_web_in_hop = []
        json_data = self.file_manager.read_deep_save()
        if json_data == "":
            json_deep = self.spider_model.change_json_to_dict("{}")     # get dict from file
        else:
            json_deep = self.spider_model.change_json_to_dict(json_data)
        if self.root_website in json_deep:  # detect root website in dict
            n_deep_save = int(json_deep[self.root_website].items()[0][0])  # get number of deep from save
            if n_deep_save < self.total_deep:
                self.list_website = json_deep[self.root_website][unicode(n_deep_save)]  # get list website from save
                self.deep = self.total_deep - n_deep_save  # calculate deep from GUI - from save
                if len(self.list_website) == 0 or len(self.list_website[0]) == 0:
                    self.deep = self.total_deep  # set deep is deep from GUI
                    self.content_dict = {}
                    self.website_dict = {}
                    self.list_website = []  # reset list of website
                    self.list_website.append([self.root_website])  # set root website in child website
                    self.spider_view.set_index_website(index_website_deep)
                else:
                    index_website_deep = self.list_website[0][0].encode("ascii", "ignore")  # set index website for find
                    self.content_dict, self.website_dict = self.spider_model.content_website_dict_from_json(
                        self.file_manager, self.spider_model, self.root_website)
                    self.spider_view.set_index_website(index_website_deep)
            else:
                self.deep = self.total_deep  # set deep is deep from GUI
                self.content_dict = {}
                self.website_dict = {}
                self.list_website = []  # reset list of website
                self.list_website.append([self.root_website])  # set root website in child website
                self.spider_view.set_index_website(index_website_deep)
        else:
            self.deep = self.total_deep  # set deep is deep from GUI
            self.content_dict = {}
            self.website_dict = {}
            self.list_website = []  # reset list of website
            self.list_website.append([self.root_website])  # set root website in child website
            self.spider_view.set_index_website(index_website_deep)
        self.deep_into_website(self.deep)

    # method that deep into website
    def deep_into_website(self, n_deep):
        self.list_web_in_hop = []
        if n_deep == 0:  # deep of reaching is end
            while self.thread_deep_count > 0:
                pass
            self.when_end_deep()
            return
        self.list_website[0] = list(set(self.list_website[0]))
        for web in self.list_website[0]:  # get website in first of child website list
            if self.update_spider_state == self.update_dict["pause"]:  # detect deeping is pause
                self.when_pause_deep(self.list_web_in_hop, n_deep)
                return
            web = web.encode("ascii", "ignore")
            web = self.spider_model.website_formatter(web)
            # self.set_thread_deep_thread(web, self.list_web_in_hop)
            while self.thread_deep_count > self.max_thread:
                pass
            thread.start_new_thread(self.deep_thread, (web, self.list_web_in_hop))
            time.sleep(self.time_delay)
        while self.thread_deep_count > 0:
            pass
        self.recheck_gather_website(n_deep)
        self.list_web_in_hop = list(set(self.list_web_in_hop))
        self.list_website.append(self.list_web_in_hop)  # save child website in that deep in list of all child
        self.list_website.pop(0)  # delete deep that is reached
        self.deep_save(self.total_deep - n_deep + 1)  # save website is not deep
        self.deep_into_website(n_deep - 1)  # go deeper

    def deep_thread(self, web, list_web_in_hop):
        self.thread_deep_count += 1
        web = web.encode("ascii", "ignore")  # set website type to string
        # set index website
        if web == "":  # website no word
            self.thread_deep_count -= 1
            return
        self.spider_view.set_index_website(web)
        self.save_webpage_data_into_dict(web)          # get data from html
        # get child website in that website
        self.list_web_in_hop = list(set(self.list_web_in_hop) | set(self.website_dict[web]))
        self.save_data_to_json()  # save data to json file

        # delete website that reach
        self.list_website[0].pop(self.list_website[0].index(web))
        self.thread_deep_count -= 1

    def recheck_gather_website(self, n_deep):
        for web in self.list_website[0]:  # get website in first of child website list
            if self.update_spider_state == self.update_dict["pause"]:  # detect deeping is pause
                self.when_pause_deep(self.list_web_in_hop, n_deep)
                return
            web = web.encode("ascii", "ignore")
            web = self.spider_model.website_formatter(web)
            self.spider_view.set_index_website(web)
            self.save_webpage_data_into_dict(web)  # get data from html
            self.list_web_in_hop = list(set(self.list_web_in_hop) | set(self.website_dict[web]))
            self.save_data_to_json()  # save data to json file
            self.list_website[0].pop(0)

    # set pause of deep
    def pause_deep(self):
        self.set_spider_update(self.update_dict["pause"])

    # do when end deep
    def when_end_deep(self):
        self.deep_save()  # save website is not deep
        self.has_deep_thread = False  # set thread is not used
        self.file_website_list = self.file_manager.list_website_file()
        self.file_index = -1
        self.spider_view.set_update_state(self.update_dict["complete"])  # set update text = complete

    # do when pause deep
    def when_pause_deep(self, list_web_in_hop, n_deep):
        while self.thread_deep_count > 0:
            pass
        if len(self.list_website) > 1:  # detect website in next deep is reach
            # merge website from save website and website is found
            self.list_website[1] = list(set(self.list_website[1]) | set(self.list_web_in_hop))
        elif len(self.list_website) == 1:  # detect website in next deeo is not reach
            self.list_web_in_hop = list(set(self.list_web_in_hop))
            self.list_website.append(self.list_web_in_hop)  # add list into list for save
        self.deep_save(self.total_deep - n_deep)  # save website is not deep
        self.has_deep_thread = False  # set thread is not used

    # save data from webpage into dict
    def save_webpage_data_into_dict(self, website):
        html_code = self.spider_model.get_html_code(website)
        all_data_str = self.spider_model.get_html_code_to_datastr(website, html_code)
        content_data = self.spider_model.get_content_from_datastr(all_data_str) \
                       + " " + self.spider_model.get_weblink_from_datastr(all_data_str)
        website_list_data = self.spider_model.get_website_from_datastr(all_data_str)
        self.content_dict[website] = content_data.strip()
        self.website_dict[website] = website_list_data

    def save_data_to_json(self):
        json_dict = self.spider_model.get_json_string_for_deep(self.root_website, self.website_dict, self.content_dict)
        self.file_manager.write_website_file(self.spider_model, self.root_website, json_dict)

    def deep_save(self, deep=-1):
        """ data = self.spider_model.recheck_website_dict()
        self.file_manager.write_website_file(self.spider_model, self.root_website, data) """
        if deep == -1:
            deep = self.total_deep
        json_data = self.file_manager.read_deep_save()
        if json_data == "":
            dict_deep = self.spider_model.change_json_to_dict("{}")  # get dict from file
        else:
            dict_deep = self.spider_model.change_json_to_dict(json_data)
        dict_deep[self.root_website] = {deep: self.list_website}            # save dict for deep and website list
        self.file_manager.write_deep_save(self.spider_model.get_json_string(dict_deep))
        # print self.list_web_in_hop

    def start_to_show(self):
        self.index_website_show = self.spider_view.get_root_website().encode("ascii", "ignore")
        self.word = self.spider_view.get_word()  # set word
        json_file_name = self.spider_model.get_website_no_scheme(self.index_website_show)\
                             .replace("/", "#").replace(".", "_") + ".json"
        json_file = open(os.getcwd() + "\\website\\" + json_file_name, "r+")  # open to read file
        json_dict = self.spider_model.change_json_to_dict(json_file.read())  # set json string to dict
        show_graph = self.spider_model.set_into_graph(self.index_website_show, json_dict)  # set data to graph
        n_used = self.spider_model.set_n_used(self.index_website_show, json_dict)  # set number of used in dict
        self.spider_view.set_data_showing(show_graph, n_used)

    def set_n_used_for_indexing(self):
        self.index_website_show = self.spider_view.get_root_website().encode("ascii", "ignore")  # set root website
        self.index_website_show = self.spider_model.website_formatter(self.index_website_show)
        self.word = self.spider_view.get_word()  # set word
        json_string = self.file_manager.read_website_file(self.spider_model, self.index_website_show)
        json_dict = self.spider_model.change_json_to_dict(json_string)
        show_graph = self.spider_model.set_into_graph(self.index_website_show, json_dict)  # set data to graph
        n_used = self.spider_model.set_n_used(self.index_website_show, json_dict)  # set number of used in dict
        self.spider_view.set_data_showing(show_graph, n_used)

    # start indexing
    def start_to_indexing(self):
        t = time.time()
        avoid_word_list = self.spider_model.set_avoid_word("avoid_word.txt")          # set avoid word from file
        file_list = self.file_manager.list_website_file()
        self.file_manager.delete_indeixng()
        self.indexing_dict = self.spider_model.indexing(avoid_word_list, file_list, self.indexing_dict)     # indexing
        self.file_manager.write_indexing(self.indexing_dict)
        print time.time() - t

    def set_auto_indexing(self):
        indexing_dict = self.file_manager.read_indexing()
        self.indexing_dict = {}
        for word in indexing_dict:
            word = word.encode("ascii", "ignore")
            if word not in self.indexing_dict:
                self.indexing_dict[word] = {}
            for website in indexing_dict[word]:
                website = website.encode("ascii", "ignore")
                n_used = int(indexing_dict[word][website]["used"])
                n_word = int(indexing_dict[word][website]["word"])
                if website not in self.indexing_dict[word]:
                    self.indexing_dict[word][website] = {}
                self.indexing_dict[word][website] = {"used": n_used, "word": n_word}

    # start searching
    def start_to_searching(self):
        rank_dict = self.spider_model.ranking(self.indexing_dict)
        self.spider_view.show_search(rank_dict)

    def prev_file(self):
        self.file_index -= 1
        if self.file_index < 0:
            self.file_index = len(self.file_website_list) - 1
        if len(self.file_website_list) > 0:
            file_open = open(self.file_website_list[self.file_index], "r+")
            dict_data = json.loads(file_open.read())
            file_open.close()
            file_name = dict_data.keys()[0].encode("ascii").strip()
            self.spider_view.set_root_website(file_name)

    def next_file(self):
        self.file_index += 1
        if self.file_index >= len(self.file_website_list):
            self.file_index = 0
        if len(self.file_website_list) > 0:
            file_open = open(self.file_website_list[self.file_index], "r+")
            dict_data = json.loads(file_open.read())
            file_open.close()
            file_name = dict_data.keys()[0].encode("ascii").strip()
            self.spider_view.set_root_website(file_name)

    def set_spider_update(self, state):
        while self.thread_deep_count > 0:
            pass
        self.update_spider_state = state
        self.spider_view.set_update_state(state)

    def gather_website_all(self):
        weblist = self.file_manager.get_website_deep_list()
        for website in weblist:
            website = website.strip()
            if website[0] == "#" or website[0] == "-":
                continue
            print website
            self.start_search_website_thread(website)
            time.sleep(5)
            while self.has_deep_thread:
                pass
        print "GATHER ALL WEBSITE COMPLETE"
