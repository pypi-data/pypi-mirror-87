import os
import sys


def get_path(*paths):
    '''
    获取程序运行根目录，传参可拼接。
    '''

    me = os.path.realpath(sys.argv[0])
    folder = os.path.dirname(me)
    return os.path.join(folder, *paths)


def get_configuration():
    '''
    '''


def load_content(path):
    '''
    加载文件内容。
    '''

    with open(path, 'r', encoding='utf-8') as reader:
        return reader.read()


def list_files(folder):
    '''
    列举目录的所有文件。
    '''

    files = []
    for name in os.listdir(folder):
        path = os.path.abspath(folder + '/' + name)
        if os.path.isdir(path):
            files.extend(list_files(path))
        elif os.path.isfile(path):
            files.append(path)
    return files
