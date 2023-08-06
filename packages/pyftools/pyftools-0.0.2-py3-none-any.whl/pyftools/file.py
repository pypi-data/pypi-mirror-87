# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 11:17:48 2020

@author: Jason Hu
"""
import os
import sys
import chardet
import shutil

def get_text_charset(filename):
    """
    :param filename: Text file path
    :return: A character-encoded string for text
    """
    fp = open(file=filename, mode='rb') # 以二进制模式读取文件
    data = fp.read()
    fp.close()
    result = chardet.detect(data)
    #{'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}
    return result['encoding']

def walk_files(path, func, arg):
    """
    walk all files in path, and call 'func' with arg in each file
    ----
    :path string: dir path
    :func callback: function callback
    :arg mixed: arg for func
    :return: return a list what 'func' return
    """
    retval = []
    lsdir = os.listdir(path)
    dirs = [n for n in lsdir if os.path.isdir(os.path.join(path, n))]
    if dirs:
        for n in dirs:
            retval += walk_files(os.path.join(path, n), func, arg) # recursion
    
    files = [n for n in lsdir if os.path.isfile(os.path.join(path, n))]
    for fname in files: 
        fpath = os.path.join(path, fname)
        data = func(fpath, arg)
        if data != None:
            retval.append(data)
    return retval

def __load_txt(path):
    try:
       fp = open(path, 'r',encoding=('utf-8'))
       data = fp.read()
       fp.close()
    except Exception:
        try:
            fp = open(path, 'r',encoding=('gbk'))
            data = fp.read()
            fp.close()
        except Exception:
            print("pyftools: open file", path, "failed!")
            print("pyftools: stop serverce!")
            sys.exit()
    return data

def load_file(path, types = None):
    """
    load file in path if file format in types list
    ----
    :param path: file path
    :param code: file type list, if None, load all files, or not load the files in the list, such as ['txt', 'xlsx']
    :return: a list is [path, data]
    """
    ext = path.split(".")[-1]
    if types != None:
        if ext not in types: # filter this file
            return None 
        
    if ext == "txt":
        return [path, __load_txt(path)]
    else:
        print("pyftools: format", ext, "not support!")
        return None

def load_files(path, types = None):   
    """
    load all files in path if file format in types list
    ----
    :param path: file path
    :param code: file type list, if None, load all files, or not load the files in the list, such as ['txt', 'xlsx']
    :return: a list, each item is [path, data]
    """  
    return walk_files(path, load_file, types)

def __convert_file_encoding(path, arg):
    data = __load_txt(path)
    with open(path, 'w+',encoding=(arg)) as fp:
        fp.write(data)

def convert_file_encoding(path, code):       
    """
    :param path: dir path
    :param code: the format will convert to. (utf-8, gbk...)
    :return: None
    """     
    walk_files(path, __convert_file_encoding, code)

def save_file(file_path, data, _encoding='utf-8'):
    """
    save data to file path
    ----
    :param file_path: file path
    :param data: file data
    :param _encoding: The code of the file to be saved
    :return: None
    """  
    with open(file_path, "w", encoding=_encoding) as fp:
        fp.write(data)

def wash_file(file_path, wash_arg):
    """
    clean one file with callback, and save the buf return from callback func
    ----
    :param file_path: file path dir
    :param callback: call back func. 
        exp:    def wash_func(pathname, arg):
                    ...
                    return None
    :return: None
    """    
    callback = wash_arg[0]
    arg = wash_arg[1]
    if callback == None:
        print("Error: pyftoolsf: wash_file: callback is None!")
        return
    file_data = load_file(file_path)
    if file_data == None:
        return
    buf = callback(file_data[0], file_data[1], arg)
    if buf != None:
        save_file(file_path, buf)

def wash_files(file_path, callback, arg):
    """
    clean one file with callback func
    ----
    :param file_path: file path dir
    :param callback: call back func. 
        exp:    def wash_func(pathname, arg):
                    ...
                    return None
    :return: None
    """    
    walk_files(file_path, wash_file, [callback, arg])

def get_filename(pathname, split_char='/'):
    """
    :param pathname: path name
    :param split_char: Path interval character
    :return: file name
    """
    pathname = pathname.split(split_char)
    return pathname[-1]

def remove_files(filepath, file_list = None):
    """
    Deletes all files and folders in a directory
    ----
    :param filepath: The path to the file to delete if not ""
    :param file_list: Remove files in file if file_list not None
    :return: None
    """
    if filepath != None:
        del_list = os.listdir(filepath)
        for f in del_list:
            file_path = os.path.join(filepath, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    if file_list != None:
        for file in file_list:
            os.remove(file)