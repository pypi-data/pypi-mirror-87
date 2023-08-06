# coding=utf-8

# @Time: 2020/3/2 15:28
# @Auther: liyubin

import shutil

"""
执行端环境清理
"""


def tear_down(git_case=False, snapshot=False):
    file_list = ['data', 'details', 'element', 'JUnit', 'importFiles', 'lib', 'log', 'report', 'testcase']
    if git_case:
        file_list.append('git_case')
    if snapshot:
        file_list.append('snapshot')
    for i in file_list:
        shutil.rmtree(i, ignore_errors=True)
