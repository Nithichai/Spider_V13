from nodebox.gui import *       # Library for GUI
from nodebox.graphics import *  # Library for draw canvas
from nodebox.graphics.physics import Graph      # Library use to draw graph
import math                     # Library for calculate distance mouse and node
import networkx     # Library use save website in graph

update_website_func = None
show_output_func = None
indexing_func = None
go_func = None
pause_func = None
prev_func = None
next_func = None


class SpiderView:
    def __init__(self, spider_model):
        print "start : init : SpiderView"
        self.spider_model = spider_model        # get data from spider model
        self.show_graph = Graph()  # graph to draw
        self.dict_used = {}
        self.index_panel = Panel("Indexing", fixed=False, modal=True)
        self.search_panel = Panel("Search..", x=450, fixed=False, modal=True)
        self.result_text = Text("")             # set text to show result
        self.update_complete_text = Text("")    # set text to update status
        self.update_state = 0                   # State of update
        self.index_website = ""
        self.deep = 0
        self.graph_website = ""
        self.website_field = ""
        print "complete : init : SpiderView"

    def set_data_showing(self, show_graph, dict_used):
        self.show_graph = show_graph  # graph to draw
        self.dict_used = dict_used
        self.deep = self.get_deep()
        self.graph_website = self.get_root_website()

    # method to set GUI for
    def set_gui(self, my_canvas):
        print "start : set_gui : SpiderView"
        layout = Rows(width=250, height=720)    # set layout
        layout.extend([                         # add object in layout
            # add field to insert website
            ("Website", Field(value="", id="web_text", wrap=True)),
            ("Deep", Field(value="1", id="deep_text", wrap=True)),         # add field to get deep of searching website
            Button("Update Website", action=update_website_func),          # add button to update website
            Button("Pause", action=pause_func),                            # add button to update website
            Button("Show output", action=show_output_func),                # add button to show output
            Button("Indexing", action=indexing_func),                      # add button to indexing
            Row(controls=[
                Button("<prev", action=prev_func),
                Button("next>", action=next_func)
            ])
        ])
        self.index_panel.append(layout)         # add layout to index_panel
        self.index_panel.pack()                 # show index_panel
        my_canvas.append(self.index_panel)      # add index_panel into canvas

        layout = Rows(width=500, height=300)    # set layout
        layout.extend([                         # add object in layout
            # add field to insert website
            ("Search", Field(value="tracer", id="word_text", wrap=True)),   # add field to insert word to search
            Field(id="web_list_text", width=500, height=100, wrap=True),    # add file to show result after search
            Button("Go", action=go_func),       # add button to indexing
        ])
        self.search_panel.append(layout)        # add layout to index_panel
        self.search_panel.pack()                # show index_panel
        my_canvas.append(self.search_panel)     # add index_panel into canvas
        print "complete : set_gui : SpiderView"

    def draw_graph(self, my_canvas):
        # print "start : draw_graph : SpiderView"
        my_canvas.size = 1080, 720              # set size of canvas
        my_canvas.clear()                       # clear canvas
        offset_x = my_canvas.width / 2          # set offset x of graph
        offset_y = my_canvas.height / 2         # set offset y of graph
        push()  # push matrix
        background(Color(255))                  # set background = white
        translate(offset_x, offset_y)           # move graph to offset

        mx = my_canvas.mouse.x - offset_x       # get x of mouse
        my = my_canvas.mouse.y - offset_y       # get y of mouse

        if len(self.show_graph.nodes) > 0:
            root_node_id = self.spider_model.get_netloc(self.graph_website)
            node_deep_list = self.show_graph.node(root_node_id).flatten(depth=self.deep)

            for node in self.show_graph.nodes:
                if node not in node_deep_list:
                    self.show_graph.remove(node)

            for node in self.show_graph.nodes:      # get node from graph
                num = self.dict_used[node.id]       # get number of used (netloc)
                node.radius = 8 + int(num * 0.05)   # set radius
                node.stroke = Color(255)            # set node stroke color
                node.fill = Color(0)                # set node color
                if node.id != "":                   # detect no word node
                    node.text.fill = None           # set node text = ""
                if node.id == root_node_id:
                    node.text.fill = Color(0)
                    node.fill = Color(255, 0, 0)
                else:
                    node.text.fill = Color(0)

                # detect mouse on node
                if math.sqrt((mx - node.x) * (mx - node.x) + (my - node.y) * (my - node.y)) < node.radius:
                    if node.id != "":                                       # detect node has value
                        self.draw_result_text(my_canvas, node.id, num)      # set text of result

            for edge in self.show_graph.edges:  # get edge from graph
                edge.length = 20                    # set edge length
                edge.stroke = Color(0)              # set stroke color
                edge.strokewidth = 2                # set stroke width

            self.show_graph.update()             # update graph
            self.show_graph.draw(directed=True)  # draw grpah
        pop()                                                           # pop matrix
        self.result_text.draw(x=20, y=my_canvas.height - 70)  # draw result text
        self.draw_update_text(my_canvas)                                # draw update text
        # print "complete : draw_graph : SpiderView"

    # method that set result text from node (netloc, n_used, n_word)
    def draw_result_text(self, my_canvas, netloc="", n_used=""):
        # print "start : draw_result_text : SpiderView"
        self.result_text.fill = Color(0)  # set color result text
        self.result_text.text = netloc + "\n\nWeb is used : " + str(n_used)
        # print "complete : draw_result_text : SpiderView"

    # method that set update text state
    def draw_update_text(self, my_canvas):
        # print "start : draw_update_text : SpiderView"
        self.update_complete_text.x = my_canvas.width - 250  # set x of update text
        self.update_complete_text.y = my_canvas.height - 70  # set y of update text
        try:
            # print "start : draw_update_text : SpiderView"
            self.update_complete_text.fontsize = 8  # set font size
            self.update_complete_text.fill = Color(0)  # set update text color
            if self.update_state == 0:
                self.update_complete_text.text = "Welcome to Spider"  # set text update_complete
            elif self.update_state == 1:  # spider update complete
                index_website = str(self.index_website)
                self.update_complete_text.text = "Updating....\n" + index_website
            elif self.update_state == 2:  # spider update not complete
                self.update_complete_text.text = "Update Complete"  # set text update_complete
            elif self.update_state == 3:
                self.update_complete_text.text = "Update Pause"  # set text update_complete
            self.update_complete_text.draw()  # draw update text
            # print "complete : draw_update_text : SpiderView"
        except UnicodeError:
            print "Error : draw_update_text : SpiderView"

    # show data after search
    def show_search(self, rank_dict):
        print "start : show_search : SpiderView"
        word = self.search_panel.word_text.value.strip().lower()        # set word to lower
        word_list = word.split()                                        # get list word from GUI
        if len(word_list) == 1:                                         # Found only one word
            if word in rank_dict:                                       # detect word is in word dict
                index = 1                                               # start index
                str_write_to_panel = ""
                print rank_dict[word]
                for data_pack in rank_dict[word]:                       # loop data pack from dict of word
                    website = data_pack[0]                              # get website
                    n_used = data_pack[1]["used"]                       # get number of used
                    n_word = data_pack[1]["word"]                       # get number of word

                    # set data to search panel
                    str_write_to_panel += str(index) + ".) Website : " \
                                                     + str(website.encode("ascii", "ignore")) \
                                                     + "\n\t" + "Used : " + str(n_used) \
                                                     + "\n\t" + "Found : " + str(n_word) + "\n"
                    index += 1                                          # increase index
                self.search_panel.web_list_text.value = str_write_to_panel
            else:
                # Set datd not found
                self.search_panel.web_list_text.value = "Data Not Found"
        elif len(word_list) > 1:                                        # Word more than 1
            list_set_website = []                                       # Set list of website set
            index_set = 0                                               # Set index of set
            for word in word_list:                                      # Loop word in word list
                if word in rank_dict:                                   # Detect word is in list
                    list_set_website.append(set())                      # Add set to list
                    for data_pack in rank_dict[word]:                   # get data pack from dict of word
                        website = data_pack[0]                          # get website
                        list_set_website[index_set].add(website)        # Set website into set
                else:
                    del word_list[word_list.index(word)]                # delete word that not found
                index_set += 1                                          # add index of set

            if len(word_list) == 0 or len(list_set_website) == 0:
                self.search_panel.web_list_text.value = "Data Not Found"
                return
            else:
                total_set = list_set_website[0]                         # get set of first word
                for i in range(1, len(list_set_website)):               # loop to get all set
                    total_set = total_set & list_set_website[i]         # find website is same
                self.search_panel.web_list_text.value = ""              # reset search panel
                index = 1                                               # start index
                str_write_to_panel = ""
                for data_pack in rank_dict[word_list[0]]:               # get data pack
                    website = data_pack[0]                              # get website
                    if website in total_set:                            # website in set
                        n_used = data_pack[1]["used"]                   # get number of used
                        n_word = data_pack[1]["word"]                   # get number of word

                        # show data in search panel
                        str_write_to_panel += str(index) + ".) Website : " + str(website.encode("ascii", "ignore")) \
                                                + "\n\t" + "Used : " + str(n_used) \
                                                + "\n\t" + "Found : " + str(n_word) + "\n"
                        index += 1                                      # increase index
                self.search_panel.web_list_text.value = str_write_to_panel
        print "complete : show_search : SpiderView"

    @staticmethod
    # method set function for search website
    def set_website_update(update_website):
        print "start : set_website_update : SpiderView"
        global update_website_func
        update_website_func = update_website
        print "complete : set_website_update : SpiderView"

    @staticmethod
    # method that set function show GUI and graph
    def set_show_output(show_output):
        print "start : set_show_output : SpiderView"
        global show_output_func
        show_output_func = show_output
        print "complete : set_show_output : SpiderView"

    @staticmethod
    # method that set function start indexing
    def set_indexing(indexing):
        print "start : set_indexing : SpiderView"
        global indexing_func
        indexing_func = indexing
        print "complete : set_indexing : SpiderView"

    @staticmethod
    # method that set function start indexing
    def set_go(go):
        print "start : set_go : SpiderView"
        global go_func
        go_func = go
        print "complete : set_go : SpiderView"

    @staticmethod
    # method that set function start indexing
    def set_pause(pause):
        print "start : set_pause : SpiderView"
        global pause_func
        pause_func = pause
        print "complete : set_pause : SpiderView"

    @staticmethod
    # method that set function start indexing
    def set_prev(prev):
        print "start : set_prev : SpiderView"
        global prev_func
        prev_func = prev
        print "complete : set_prev : SpiderView"

    @staticmethod
    # method that set function start indexing
    def set_next(next):
        print "start : set_next : SpiderView"
        global next_func
        next_func = next
        print "complete : set_next : SpiderView"

    # method that get root website in field
    def get_root_website(self):
        # print "complete : get_root_website : SpiderView"
        return self.index_panel.web_text.value.encode("ascii", "ignore")

    def set_root_website(self, data):
        # print "complete : get_root_website : SpiderView"
        self.index_panel.web_text.value = data.encode("ascii", "ignore")

    # method that get word in field
    def get_word(self):
        # print "complete : get_word : SpiderView"
        return self.search_panel.word_text.value.encode("ascii", "ignore")

    # method that get deep in field
    def get_deep(self):
        # print "complete : get_deep : SpiderView"
        return int(self.index_panel.deep_text.value)

    # method that return update state
    def get_update_state(self):
        return self.update_state

    # method that set update state
    def set_update_state(self, state):
        self.update_state = state

    def set_index_website(self, website):
        self.index_website = website
