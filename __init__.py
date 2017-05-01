from Spider_Control import SpiderControl    # Library for control spider
from nodebox.graphics import *              # Library for draw canvas


# Get function of deeping to set with button
def website_update(button):
    spider.start_search_website_thread()


# Get function of show graph to set with button
def show_graph(button):
    spider.start_to_show()


# Get function of indexing to set with button
def indexing(button):
    spider.start_to_indexing()


# Get function of searching to set with button
def searching_word(button):
    spider.start_to_searching()


# Get function of pause to deep website to set with button
def pause_deep(button):
    spider.pause_deep()


def prev_index(button):
    spider.prev_file()


def next_index(button):
    spider.next_file()


# Draw graph to set with button
def draw(my_canvas):
    spider.spider_view.draw_graph(my_canvas)


if __name__ == '__main__':
    spider = SpiderControl()                                    # set spider controller
    spider.spider_view.set_website_update(website_update)       # set method to deep website
    spider.spider_view.set_show_output(show_graph)              # set method to show graph
    spider.spider_view.set_indexing(indexing)                   # set method to indexing
    spider.spider_view.set_go(searching_word)                   # set method to start search
    spider.spider_view.set_pause(pause_deep)                    # set method to pause to deep
    spider.spider_view.set_prev(prev_index)
    spider.spider_view.set_next(next_index)
    spider.spider_view.set_gui(canvas)                          # set method to set GUI
    canvas.run(draw)

