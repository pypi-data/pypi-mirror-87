# coding=utf-8

# @Time: 2020/3/5 10:57
# @Auther: liyubin

"""
elements 辅助定位
"""


def tap_or_input_elements_index(g, element_location, data_=None):
    """
    处理elements 的 index 点击 和 输入
    :param g: 全局变量
    :param element_location: dict 所需elements/value/index
    :param data_: 输入时参数
    mobile中 input /tap 调用
    """
    if element_location.get('elements') == 'class_name' and isinstance(int(element_location.get('index_')), int):
        if data_:
            g.driver.find_elements_by_class_name(element_location.get('value'))[element_location.get('index_')].clear()
            g.driver.find_elements_by_class_name(element_location.get('value'))[
                element_location.get('index_')].send_keys(data_['text'])
        else:
            g.driver.find_elements_by_class_name(element_location.get('value'))[element_location.get('index_')].click()
