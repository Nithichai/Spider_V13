import os
import json


class FileManager:
    def __init__(self):
        if "website" not in os.listdir(os.getcwd()):
            os.mkdir("website")
        if "indexing" not in os.listdir(os.getcwd()):
            os.mkdir("indexing")
        if "other" not in os.listdir(os.getcwd()):
            os.mkdir("other")

        if "deep_save.json" not in os.listdir(os.getcwd() + "\\other"):
            file_save = open(os.getcwd() + "\\other\\deep_save.json", "w+")
            file_save.close()

    @staticmethod
    def write_indexing(json_dict):
        alphabets_dict = {}
        for i in range(ord('a'), ord('z') + 1):
            alphabets_dict[chr(i)] = {}

        for word in json_dict:
            first_letter = word[0]
            if first_letter not in alphabets_dict:
                continue
            alphabets_dict[first_letter][word] = json_dict[word]

        new_alphabets_dict = alphabets_dict.copy()
        for letter in alphabets_dict:
            if len(alphabets_dict[letter]) < 200:
                continue
            list_alphabets = list(alphabets_dict[letter])
            word_counter = 0
            index = 0
            for word in list_alphabets:
                letter_index = letter + "_" + str(index)
                if letter_index not in new_alphabets_dict:
                    new_alphabets_dict[letter_index] = {}
                new_alphabets_dict[letter_index][word] = alphabets_dict[letter][word]
                del(new_alphabets_dict[letter][word])
                word_counter += 1
                if word_counter > 200:
                    index += 1
                    word_counter = 0
            if len(new_alphabets_dict[letter]) == 0:
                del(new_alphabets_dict[letter])
        alphabets_dict = new_alphabets_dict

        for letter in alphabets_dict:
            word_dict = alphabets_dict[letter]
            file_name = "\\indexing\\indexing_" + letter + ".json"
            file_save = open(os.getcwd() + file_name, "w+")
            file_save.write(json.dumps(word_dict, indent=4, sort_keys=True))
            file_save.close()

    def read_indexing(self):
        indexing_dict = {}
        for file_name in os.listdir(os.getcwd() + "\\indexing"):
            file_read = open(os.getcwd() + "\\indexing\\" + file_name, "r+")
            indexing_dict.update(json.loads(file_read.read()))
            file_read.close()
        return indexing_dict

    def read_deep_save(self):
        file_read = open(os.getcwd() + "\\other\\deep_save.json", "r+")
        data = file_read.read()
        file_read.close()
        return data

    def write_deep_save(self, data):
        file_write = open(os.getcwd() + "\\other\\deep_save.json", "w+")
        file_write.write(data)
        file_write.close()

    def list_website_file(self):
        list_data = os.listdir(os.getcwd() + "\\website")
        return [os.getcwd() + "\\website\\" + data for data in list_data]

    def read_website_file(self, model, website):
        file_name = model.get_website_no_scheme(website).replace(".", "_").replace("/", "#") + ".json"
        file_write = open(os.getcwd() + "\\website\\" + file_name, "r+")
        data = file_write.read()
        file_write.close()
        return data

    def write_website_file(self, model, website, data):
        file_name = model.get_website_no_scheme(website).replace(".", "_").replace("/", "#") + ".json"
        file_write = open(os.getcwd() + "\\website\\" + file_name, "w+")
        file_write.write(json.dumps(data, indent=4, sort_keys=True))
        file_write.close()

    def delete_indeixng(self):
        file_list = os.listdir(os.getcwd() + "\\indexing")
        for file_name in file_list:
            os.remove(os.getcwd() + "\\indexing\\" + file_name)

    def get_website_deep_list(self):
        file_open = open(os.getcwd() + "\\other\\weblist.txt", "r+")
        list_website = []
        for website in file_open:
            list_website.append(website.strip())
        return list_website
