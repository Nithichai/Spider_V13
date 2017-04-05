from Spider_Model import SpiderModel  # use save data
from Spider_View import SpiderView  # use GUI and sho graph
import thread  # use thread of program
import os  # use for specific file
import time


class SpiderControl:
    def __init__(self):
        print "start : init : SpiderControl"
        self.spider_model = SpiderModel()
        self.spider_view = SpiderView(self.spider_model)
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

        if "deep_save.json" not in os.listdir(os.getcwd()):  # not found deep_save.json
            file_saving = open("deep_save.json", "w+")  # open file
            file_saving.write(self.spider_model.get_json_string({}))  # save json
            file_saving.close()  # close file
        self.set_auto_indexing()
        print "complete : init : SpiderControl"

    # method that thread of searching website
    def start_search_website_thread(self):
        print "start : start_search_website_thread : SpiderControl"
        if not self.has_deep_thread:  # detect not use thread
            thread.start_new_thread(self.start_deep_website, ())  # start thread
            self.has_deep_thread = True  # set thread is used
        print "complete : start_search_website_thread : SpiderControl"

    def set_spider_update(self, state):
        self.update_spider_state = state
        self.spider_view.set_update_state(state)

    # method that start deep into web
    def start_deep_website(self):
        self.set_spider_update(self.update_dict["updating"])  # set update text = updating
        self.root_website = self.spider_view.get_root_website().encode("utf-8")  # set root website
        index_website_deep = self.spider_view.get_root_website()  # set index website
        self.total_deep = self.spider_view.get_deep()  # get total_deep from GUI

        if "deep_save.json" not in os.listdir(os.getcwd()):
            file_new = open("deep_save.json", "w+")
            file_new.write("{}")
            file_new.close()
        file_deep = open("deep_save.json", "r+")  # open file
        json_deep = self.spider_model.change_json_to_dict(file_deep.read())     # get dict from file
        file_deep.close()  # close file

        if self.root_website in json_deep:  # detect root website in dict
            n_deep_save = int(json_deep[self.root_website].items()[0][0])  # get number of deep from save
            if n_deep_save < self.total_deep:
                self.list_website = json_deep[self.root_website][unicode(n_deep_save)]  # get list website from save
                self.deep = self.total_deep - n_deep_save  # calculate deep from GUI - from save
                index_website_deep = self.list_website[0][0].encode("utf-8")  # set index website for find
                self.spider_view.set_index_website(index_website_deep)
            else:
                self.deep = self.total_deep  # set deep is deep from GUI
                self.list_website = []  # reset list of website
                self.list_website.append([self.root_website])  # set root website in child website
                self.spider_view.set_index_website(index_website_deep)
        else:
            self.deep = self.total_deep  # set deep is deep from GUI
            self.list_website = []  # reset list of website
            self.list_website.append([self.root_website])  # set root website in child website
            self.spider_view.set_index_website(index_website_deep)
        self.deep_into_website(self.deep)
        print "complete : start_search_website : SpiderControl"""

    # method that deep into website
    def deep_into_website(self, n_deep):
        print "start : deep_into_website : SpiderControl"
        list_web_in_hop = []  # set child website in that deep
        if n_deep == 0:  # deep of reaching is end
            self.when_end_deep()
            return
        self.list_website[0] = list(set(self.list_website[0]))
        for web in self.list_website[0]:  # get website in first of child website list
            if self.update_spider_state == self.update_dict["pause"]:  # detect deeping is pause
                self.when_pause_deep(list_web_in_hop, n_deep)
                return
            while (thread._count() > 100):
                pass
            print "Start thread again"
            self.set_thread_deep_thread(web, list_web_in_hop)
            time.sleep(1)
        while (thread._count() > 1):
            pass
        print "Stop all thread"
        list_web_in_hop = list(set(list_web_in_hop))
        self.list_website.append(list_web_in_hop)  # save child website in that deep in list of all child
        self.list_website.pop(0)  # delete deep that is reached
        self.deep_save(self.total_deep - n_deep + 1)  # save website is not deep
        self.deep_into_website(n_deep - 1)  # go deeper
        print "complete : deep_into_website : SpiderControl : Deep = " + str(n_deep)

    def set_thread_deep_thread(self, web, list_web_in_hop):
        thread.start_new_thread(self.deep_thread, (web, list_web_in_hop))

    def deep_thread(self, web, list_web_in_hop):
        print "start : deep_thread : SpiderControl"
        web = web.encode("utf-8")  # set website type to string

        # set index website
        if web == "":  # website no word
            return
        self.spider_view.set_index_website(web)
        self.save_webpage_data_into_dict(web)          # get data from html

        # get child website in that website
        for web_inside in self.website_dict[web]:
            if web_inside == "":  # website no word
                continue  # next loop
            list_web_in_hop.append(web_inside)  # save child website in list
        self.save_data_to_json()  # save data to json file

        # delete website that reach
        self.list_website[0].pop(self.list_website[0].index(web))
        print "complete : deep_thread : SpiderControl"

    # set pause of deep
    def pause_deep(self):
        self.set_spider_update(self.update_dict["pause"])

    # do when end deep
    def when_end_deep(self):
        while (thread._count() > 1):
            pass
        print "Stop all thread"
        self.deep_save()  # save website is not deep
        self.has_deep_thread = False  # set thread is not used
        self.spider_view.set_update_state(self.update_dict["complete"])  # set update text = complete

    # do when pause deep
    def when_pause_deep(self, list_web_in_hop, n_deep):
        while (thread._count() > 1):
            pass
        print "Stop all thread"
        if len(self.list_website) > 1:  # detect website in next deep is reach
            # merge website from save website and website is found
            self.list_website[1] = list(set(self.list_website[1]) | set(list_web_in_hop))
        elif len(self.list_website) == 1:  # detect website in next deeo is not reach
            list_web_in_hop = list(set(list_web_in_hop))
            self.list_website.append(list_web_in_hop)  # add list into list for save
        self.deep_save(self.total_deep - n_deep)  # save website is not deep
        self.has_deep_thread = False  # set thread is not used

    # save data from webpage into dict
    def save_webpage_data_into_dict(self, website):
        html_code = self.spider_model.get_html_code(website)
        all_data_str = self.spider_model.get_htmlcode_to_datastr(html_code)
        content_data = self.spider_model.get_content_from_datastr(all_data_str) \
                       + self.spider_model.get_weblink_from_datastr(all_data_str)
        website_list_data = self.spider_model.get_website_from_datastr(all_data_str)
        self.content_dict[website] = content_data
        self.website_dict[website] = website_list_data

    def save_data_to_json(self):
        json_string = self.spider_model.get_json_string_for_deep\
            (self.root_website, self.website_dict, self.content_dict)
        json_file_name = self.spider_model.get_netloc(self.root_website).replace(".", "_") + ".json"
        json_file = open(json_file_name, "w+")  # start to write file
        json_file.write(json_string)  # write json in file
        json_file.close()  # stop to use file

    def deep_save(self, deep=-1):
        print "start : deep_save : SpiderControl"
        if deep == -1:
            deep = self.total_deep
        file_saving = open("deep_save.json", "r+")  # open file to read
        dict_deep = self.spider_model.change_json_to_dict(file_saving.read())  # load json to dict
        dict_deep[self.root_website] = {deep: self.list_website}  # save dict for deep and website list
        file_saving.close()  # close file
        file_saving = open("deep_save.json", "w+")  # open file to write
        file_saving.write(self.spider_model.get_json_string(dict_deep))  # write json to file
        file_saving.close()  # close file
        print "complete : deep_save : SpiderControl"

    def start_to_show(self):
        print "complete : search_website : SpiderControl"
        self.index_website_show = self.spider_view.get_root_website().encode("utf-8")
        self.word = self.spider_view.get_word()  # set word
        json_file_name = self.spider_model.get_netloc(self.index_website_show).replace(".", "_") + ".json"
        json_file = open(json_file_name, "r+")  # open to read file
        json_dict = self.spider_model.change_json_to_dict(json_file.read())  # set json string to dict
        print type(json_dict), type(self.index_website_show)
        show_graph = self.spider_model.set_into_graph(self.index_website_show, json_dict)  # set data to graph
        n_used = self.spider_model.set_n_used(self.index_website_show, json_dict)  # set number of used in dict
        self.spider_view.set_data_showing(show_graph, n_used)
        print "complete : search_website : SpiderControl"

    # start indexing
    def start_to_indexing(self):
        print "start : start_to_indexing : SpiderControl"
        avoid_word_list = self.spider_model.set_avoid_word("avoid_word.txt")                # set avoid word from file
        print type(avoid_word_list), type(os.listdir(os.getcwd()))
        self.indexing_dict = self.spider_model.indexing(avoid_word_list, os.listdir(os.getcwd()))     # indexing
        file_json = open("indexing.json", "w+")
        file_json.write(self.spider_model.get_json_string(self.indexing_dict))
        file_json.close()
        print "complete : start_to_indexing : SpiderControl"

    def set_auto_indexing(self):
        print "start : set_auto_indexing : SpiderControl"
        file_json = open("indexing.json", "r+")
        indexing_dict = self.spider_model.change_json_to_dict(file_json.read())
        new_indexing_dict = {}
        for word in indexing_dict:
            word = word.encode("utf-8")
            for website in indexing_dict[word]:
                website = website.encode("utf-8")
                n_used = int(indexing_dict[word][website]["used"])
                n_word = int(indexing_dict[word][website]["word"])
                new_indexing_dict[word] = {website: {"used": n_used, "word": n_word}}
        self.indexing_dict = new_indexing_dict
        print "complete : set_auto_indexing : SpiderControl"

    # start searching
    def start_to_searching(self):
        print "start : start_to_searching : SpiderControl"
        rank_dict = self.spider_model.ranking(self.indexing_dict)
        self.spider_view.show_search(rank_dict)
        print "complete : start_to_searching : SpiderControl"
