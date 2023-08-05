#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : zb
# @Time    : 2020/11/18 13:20
# @Blog    : https://blog.zbmain.com
import pandas as pd


def __merge(datas: list):
    '''添加多个数据文件时使用'''
    with open('all_datas.txt', 'w', encoding='utf-8') as outfile:
        for file in datas:
            with open(file, 'r') as infile:
                outfile.write(infile.read())
    with open('all_datas.txt', 'r', encoding='utf-8') as f:
        data = f.read()
    return data


def read_txt(data):
    if isinstance(data, list):
        data = __merge(data)
    elif isinstance(data, str):
        with open(data, 'r', encoding='utf-8') as f:
            data = f.read()
    else:
        data = ''

    return data


def dataframe():
    df = pd.read_csv('all_datas.txt', sep='\n', names=['w'])
    df["w_length"] = list(map(lambda x: len(x), df["w"]))
    return df


if __name__ == '__main__':
    data = read_txt(['./jay_chou.txt'])
    print(len(data))
    print(dataframe())
