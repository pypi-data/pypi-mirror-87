# coding=utf-8

# @Time: 2020/7/23 15:14
# @Auther: liyubin

import os
import unittest
from super_sweetest import Autotest
from super_sweetest.servers.common import write_data, read_data

"""
独立执行模块
"""

class TESTCASE(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        case_data = read_data('./run_case_data.json', 'json', 'r+')
        cls.test_name = case_data.get('test_name', '')

    def test_run(self):
        """
        测试主方法
        项目名称，和测试用例、页面元素表文件名称中的项目名称必须一致
        """
        global msg
        plan_name = self.test_name

        # 环境配置信息
        if os.path.exists('testcase/' + plan_name + '-TestCase.xlsx'):
            # 测试用例集文件里的Sheet表单名称
            sheet_name = '*'
            desired_caps_ = {'platformName': 'mqtt'}
            desired_caps = desired_caps_
            server_url = ''

            msg = '数据准备正常'
        else:
            desired_caps = {}
            server_url = ''
            sheet_name = ''
            msg = '未获取有效数据'

        # 初始化自动化实例
        sweet = Autotest(plan_name, sheet_name, desired_caps, server_url)
        # 执行自动化测试
        sweet.plan()
        # 保存txt格式的详情信息
        write_data('details/details.txt', sweet.report_data, 'json', 'w+')

    @classmethod
    def tearDownClass(cls):
        # 写入执行完成状态，数据处理模块确认状态后上传报告
        write_data('./run_case_data.json', {'status': True, 'msg': msg}, flag='json', mode='w+')


if __name__ == '__main__':
    unittest.main()
