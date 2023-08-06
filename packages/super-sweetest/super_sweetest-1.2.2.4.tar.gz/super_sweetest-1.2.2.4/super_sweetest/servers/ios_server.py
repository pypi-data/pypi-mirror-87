# coding=utf-8

# @Time: 2020/4/14 11:00
# @Auther: liyubin

import re
import os
import time
import requests
from super_sweetest.config import BASE_DIR

"""
使用xcodebuild,启动WebDriverAgent托管测试服务
devicename 不建议使用名称：iphone，否则将kill所有iphone名称服务
首次启动需xcode安装 WebDriverAgent app，并授权描述文件
"""


def run_iproxy8100():
    """
    启动条件 必须在ios_tagent 前启动，否则出现不可估计的错误
    使用iproxy做端口转发, 使用http://127.0.0.1:8100连接airtest
    http://127.0.0.1:8100/status      json串
    http://127.0.0.1:8100/inspector   手机屏幕的投影
    :return:
    """
    iproxy_code = 'nohup iproxy 8100 8100 &'
    os.popen(iproxy_code)
    time.sleep(3)


def post_iproxy_status():
    """
    发送请求到iproxy http://127.0.0.1:8100/status 判断是否连接成功的标示
    :return:
    """
    try:
        res = requests.get(url='http://127.0.0.1:8100/status').json()
        state = res.get('value').get('state') if res else '未获取到返回值'
        state = 'success' if state == 'success' else 'fail'
        return state
    except:
        return '未获取到返回值'


def localtime():
    """获取当前时间"""
    localtime_ = time.asctime(time.localtime(time.time()))
    return localtime_


def get_ios_devices():
    """
    get ios devices
    :return: devices_list  [str,]
    :return: device_desc_list   [dict,dict1]
    """
    ins_devices = 'Instruments -s devices'
    ios_device_text = list(os.popen(ins_devices).readlines())

    device_list = []
    device_desc_list = []
    for devi in ios_device_text:
        device_ = devi.strip('\n')
        if 'Known Devices:' not in device_ and 'Mac' not in device_ and 'Simulator' not in device_:
            version = re.findall(r'[(](.*?)[)]', device_)[0]
            device = device_.split(' (')[0]
            assert device.lower() != 'iphone', '名称不能为：iphone， 请重新设置'
            device_list.append(device)
            device_desc_list.append({'device_name': device, 'version': version})
    print(localtime() + ' --- device list online: {} --- '.format(device_list))
    return device_list, device_desc_list


def logs_path():
    """项目路径 join build_logs"""
    path_ = os.path.join(BASE_DIR, 'build_logs')
    os.mkdir(path_) if not os.path.exists(path_) else path_
    return path_


def get_server_url(devicename):
    """
    获取ios_tagent_server输出信息中ServerURLHere
    :return: server_url
    :用法：connect_device("ios:///" + server_url)
    """

    print("----------- %s Get Server URL ----------------" % devicename)
    build_log = os.path.join(logs_path(), '{}_build_log.txt'.format(devicename))
    with open(build_log, 'rb')as fp:
        build_log = str(fp.read())

    serverurl = re.findall(r"http://(.+?)<-ServerURLHere", build_log)
    if serverurl:
        print("----------- %s ServerURLHere is %s ----------------" % (devicename, serverurl[0]))
        url = serverurl[0]
    else:
        print("----------- %s ServerURLHere is no ----------------" % devicename)
        url = 'retry server'
        time.sleep(8)
    return url


def run_ios_tagent_server(iostagen_file, platform, devicename):
    """
    非阻塞方式脱离终端在后台运行托管测试服务："nohup "+build_code
    通过xcodebuild 托管指定的手机的iOS-Tagent测试服务

    :-derivedDataPath：产生的缓存文件放在./output目录下
    :  configuration：编译环境，选择Debug/Release
    :-destination :选择test时的目标设备和系统版本号
    """

    assert devicename.lower() != 'iphone', '名称不能为：iphone， 请重新设置'
    build_log = os.path.join(logs_path(), '{}_build_log.txt'.format(devicename))
    # 实时写入日志
    build_code = "xcodebuild test \
                 -project %s/WebDriverAgent.xcodeproj \
                 -scheme WebDriverAgentRunner  \
                 -destination 'platform=%s,name=%s' > $'%s'" % (
        iostagen_file, platform, devicename, build_log)

    print("----------- %s WebDriverAgent Server Start ----------------" % devicename)
    # 非阻塞方式脱离终端在后台运行托管测试服务
    os.popen("nohup %s &" % build_code)
    time.sleep(15)


def kill_ios_tagent_server(devicename):
    """
    kill devicename 对应的WebDriverAgentRunner服务进程
    非阻塞
    """

    assert devicename.lower() != 'iphone', '名称不能为：iphone， 请重新设置'
    print("----------- %s WebDriverAgent Server Stop ----------------" % devicename)
    kill_code = "ps -ef | grep '%s' | grep -v grep | awk '{print $2}' | xargs kill -9" % devicename
    os.popen("nohup %s &" % kill_code)

    # kill iproxy
    kill_iproxy_code = "ps -ef | grep '%s' | grep -v grep | awk '{print $2}' | xargs kill -9" % 'iproxy'
    os.popen("nohup %s &"%kill_iproxy_code)

    build_log = os.path.join(logs_path(), '{}_build_log.txt'.format(devicename))
    if os.path.exists(build_log):
        os.remove(build_log)
    time.sleep(10)


if __name__ == '__main__':

    iostagen_file_ = '/Users/liyubin1/Desktop/iOS-Tagent11'
    # platform_ = 'iOS Simulator'  # 模拟器
    # deviceName_ = 'iPhone 11'


    platform_ = 'iOS'
    deviceName_ = 'LDS-Z-C5197'
    run = 2

    if run == 1:
        for i in range(3):
            print(i)
            run_iproxy8100()
            run_ios_tagent_server(iostagen_file_, platform_, deviceName_)
            # print(get_server_url(deviceName_))

            print('开始手动连接手机')
            status = post_iproxy_status()
            print('status: ', status, i)
            time.sleep(15)
    elif run == 2:
        kill_ios_tagent_server(deviceName_)

    else:
        status = post_iproxy_status()
        print('status: ', status)