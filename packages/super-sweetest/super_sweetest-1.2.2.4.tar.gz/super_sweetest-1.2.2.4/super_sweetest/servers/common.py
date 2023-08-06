# coding=utf-8

# @Time: 2020/3/5 10:57
# @Auther: liyubin

import json

"""
公共读写方法
"""

def write_data(file_name, data_, flag='', mode='w+'):
    if flag.lower() == 'json' and mode.lower() == 'w+':
        with open(file_name, 'w+', encoding='utf-8') as fp:
            json.dump(data_, fp)
    elif flag.lower() == 'eval' and mode.lower() == 'w+':
        with open(file_name, 'w+', encoding='utf-8')as fp:
            fp.write(eval(data_))
    elif mode.lower() == 'w+':
        with open(file_name, 'w+', encoding='utf-8')as fp:
            fp.write(data_)
    else:
        with open(file_name, 'a+', encoding='utf-8')as fp:
            fp.write(data_)
    return True


def read_data(file_name, flag='json', mode='r'):
    if mode == 'r':
        with open(file_name, 'r', encoding='utf-8')as fp:
            data_ = fp.read()
    elif mode == 'rb':
        with open(file_name, 'rb')as fp: # 不加encoding
            data_ = fp.read()
    else:
        with open(file_name, 'r+', encoding='utf-8')as fp:
            data_ = fp.read()
    if flag == 'json':
        try:
            return json.loads(data_)
        except Exception as e:
            raise 'Json文件内容格式错误' + str(e)
    elif flag == 'eval':
        return eval(data_)
    else:
        return data_
