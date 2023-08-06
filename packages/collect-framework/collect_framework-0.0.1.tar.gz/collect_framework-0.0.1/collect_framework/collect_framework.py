import argparse
import functools
import collections


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--string', type=str, help="Enter string")
    parser.add_argument('--file', type=str, help="Enter path to file")
    args = parser.parse_args()
    return args


@functools.lru_cache
def get_unique(string):
    counter = collections.Counter(string)
    res = [value for value in counter.values() if value == 1]
    return len(res)


def get_data(path):
    f = open(path, 'r')
    file_data = f.read()
    f.close()
    return file_data


def file_handler(path):
    data = get_data(path).split()
    result_list = []
    for string in data:
        result_list.append(get_unique(string))
    return result_list


def cli():
    arguments = get_args()
    if arguments.file:
        print(file_handler(arguments.file))
    elif arguments.string:
        print(get_unique(arguments.string))


if __name__ == '__main__':
    cli()
