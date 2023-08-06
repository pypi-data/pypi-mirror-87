# coding:utf-8

# @Time: 2020/3/5 10:57
# @Auther: liyubin

import json

"""
公共读写方法 / 配置读写
"""


def read_lib_app_config(app_config_file='./lib/app_config.json'):
    """
    # 读取./lib/app_config.json配置文件
    :param app_config_file: json配置路径
    :return:
    """
    try:
        with open(app_config_file, 'r', encoding='utf-8') as fp:
            app_config = eval(fp.read())
    except:
        # 未配置json文件时读取默认或在运行程序中配置得dict
        DESIRED_CAPS_DEMO = {"DESIRED_CAPS": {
                                                "platformName": "Air_Android",
                                                "deviceName": "23fdgdg",
                                                "platformVersion": "9",
                                                "appPackage": "com.app.packagename",
                                                "connect_type_list": ["", "javacap"],
                                                "stop_app": "True",
                                                "appActivity": "com.name.name.ui.MainActivity",
                                                "noReset": "True",
                                                "chromeOptions": {
                                                    "androidProcess": "com.tencent.mm:appbrand0"}
                                            },
                                                "SERVER_URL": "http://127.0.0.1:4723/wd/hub"
                                            }

        print('未获取到 ./lib/app_config.json 配置文件或内容，请在json文件配置或在运行程序中配置如下信息：\n{}'.format(DESIRED_CAPS_DEMO))
        return None, None
    # 环境配置信息
    return app_config.get('DESIRED_CAPS'), app_config.get('SERVER_URL')


def sync_connect(logger):
    """
     同步connect_type信息到平台
    :return:
    """
    import requests
    host = 'http://atp.leedarson.com' # 需配置自动化平台IP
    connect_url = host + '/software/sweetest/mobile/collect/'
    connect_type_ = read_data('./connect_type.json', flag='', mode='r')
    data_ = {'connect_type': connect_type_}
    res = requests.post(connect_url, data_).json()
    logger.info('--- %s ---'%res)


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
