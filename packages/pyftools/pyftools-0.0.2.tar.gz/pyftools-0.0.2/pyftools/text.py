import re
from . file import *

def load_stopwords(file_path):
    """
    :param file_path: Stop word file path
    :return: Stop word list
    """
    stopwords = [line.strip() for line in open(file_path, 'r', encoding='utf-8').readlines()]
    return stopwords

def remove_stopwords(sentence, stopwords):
    """
    :param sentence: List of sentences
    :param stopwords： Stop word list
    :return: Stop word list
    """
    words_list =[x for x in sentence if len(x) >1 and x not in stopwords]
    return words_list

def convert_list2str(list_data, space_mark = ''):
    """
    :param list_data: One-dimensional list data
    :param space_mark: The spacing symbol between string
    :return: List of converted strings
    """
    s = ""
    list_len = len(list_data)
    for i in range(list_len):
        data = list_data[i]
        s += str(data)
        if i < list_len - 1:
            s += space_mark
    return s

def convert_str2list(str_data, space_mark = ' '):
    """
    :param str_data: The data for the string to be converted is separated by spacek_mark
    :param space_mark: The spacing symbol between string
    :return: A list of strings, each of which is a string
    """
    return str_data.split(space_mark)

def load_synonym(file_path, space_mark='→', file_encoding='utf-8'):
    """
    :param file_path: Synonym file path
    :param space_mark: The spacing symbol between synonyms
    :param file_encoding: The encoding format of the file
    :return: List of synonyms. exp: [['abc', 'def'], ['tom', 'jack'],]
    """
    synonym = [line.strip().split(space_mark) for line in open(file_path, 'r', encoding=file_encoding).readlines()]
    return synonym

def __pair_in_list(pair, list_head):
    for item in list_head:
        if (pair[0] == item[0] and pair[1] == item[1]) or (pair[0] == item[1] and pair[1] == item[0]):
            return True
    return False

def wash_synonym(input_path, output_path, space_mark='→'):
    """
    :param input_path:  Synonym library file path
    :param output_path:  After cleaning the synonym library file path 
    :param space_mark: The spacing symbol between synonyms
    :return: None
    """
    synonym_list = load_synonym(input_path)    
    synonym_pair = []
    for pair in synonym_list:
        if not __pair_in_list(pair, synonym_pair):
            synonym_pair.append(pair)
        
    synonym_str = ""
    for pair in synonym_pair:
        synonym_str += pair[0] + space_mark + pair[1] + '\n'
    save_file(output_path, synonym_str)

def remove_synonym(sentence, synonym, right=False):
    """
    :param sentence: Sentence string, each word separated by a space. exp: "abc def tom jack"
    :param synonym: Synonym list. exp: [['abc', 'def'], ['tom', 'jack'], ...]
    :param right: By default, the value on the left is replaced by the value on the right, and if True is passed in, 
                the value on the right is replaced by the value on the left.
    :return: The string after converting the synonyms
    """
    word_list = convert_str2list(sentence.strip())
    list_range = range(len(word_list))
    if right:
        # trans right to left
        for group in synonym:
            for i in list_range:         
                if group[1] == word_list[i]:
                    word_list[i] = group[0]
    else:
        # trans left to right
        for group in synonym:
            for i in list_range:       
                if group[0] == word_list[i]:                  
                    word_list[i] = group[1]
    return convert_list2str(word_list, ' ')

def remove_website(buf):
    """
    :param buf: text buf
    :return: the text after del websites
    """
    re_rule = re.compile(r'[http|https]*://[a-zA-Z0-9.?/&=:]*', re.S)
    _buf = re.sub(re_rule, '', buf)
    return _buf
