# coding:utf-8

import os
import re
import sys
import uuid
import json
import zipfile
import argparse
import platform
import requests
from pathlib import Path
from client.mqtt_server import mqtt_workspace


def main():
    """
    创建命令： super_mqtt -r http://127.0.0.1 -mqtt -n 执行端名称
    api 0 / android 1 / ios 2 / web 3 / mqtt 4
    """
    if len(sys.argv) == 1:
        sys.argv.append('--help')
    parser = argparse.ArgumentParser(description='X ATP CLI Client (X 自动化测试平台命令行客户端)')
    parser.add_argument('-v', '--version', help='输出客户端版本信息', action='version', version='%(prog)s v1.1.9.7')
    parser.add_argument('-d', '--demo', help='在当前目录下创建Demo项目 `sweetest_example`', action='store_true')
    parser.add_argument('-r', '--run', dest='atp_server_url', help='创建 X-ATP 自动测试执行端服务: super_sweetest -r http://127.0.0.1 -m -n 执行端名称', action='store')
    parser.add_argument('-m', '--mqtt', help='运行 mqtt 测试执行端 (used with parameter -r)', action='store_true', default=False)
    parser.add_argument('-n', '--name', dest='workspace_name', help='执行端工作区的标识名称 (used with parameter -r)', action='store', default='')
    parser.add_argument('-a', '--app', help='在当前目录下创建Android/Ios执行端主程序 `x-atp-app`', action='store_true')
    args = parser.parse_args()
    if args.demo or args.app:
        # 解压demo项目/Android/Ios执行端主程序
        if args.demo:
            zip_name = 'sweetest_example'
            msg1 = '\n\n生成 Demo项目 `sweetest_example` 成功\n快速体验，请输入如下命令(进入示例目录，启动运行脚本):\n\ncd sweetest_example\npython start.py'
        else:
            zip_name = 'x-atp-app'
            msg1 = '\n\n生成 super_sweetest 创建Android/Ios执行端主程序 `x-atp-app` 成功\n快速体验，请查看 README.md'
        sweetest_dir = Path(__file__).resolve().parents[0]
        example_dir_ = sweetest_dir / 'example' / '{}.py'.format(zip_name)
        if os.path.exists(example_dir_):
            new_example_dir = sweetest_dir / 'example' / '{}.zip'.format(zip_name)
            os.rename(example_dir_, new_example_dir)
        example_dir = sweetest_dir / 'example' / '{}.zip'.format(zip_name)
        extract(str(example_dir), Path.cwd())

        print('\n文档: https://sweeter.io\n公众号：喜文测试\nsuper_sweetest自动化Q Q 群：630589174 (验证码：python)注意首字母小写')
        print(msg1)

    if args.atp_server_url:
        if not re.match(r'(http|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?', args.atp_server_url, re.IGNORECASE):
            print('[Cli Error]> 这不是有效的URl地址')
            return
        if args.mqtt:
            data_json = get_initialization(test_type=4, platform_url=args.atp_server_url, workspace_name=args.workspace_name)
            mqtt_workspace(sys_name=platform.system(), data=data_json['data'])
        else:
            print('[Cli Error]> 缺少 -api|-mqtt|-android|-ios|-web 参数')


def extract(z_file, path):
    """
    解压缩文件到指定目录
    """
    f = zipfile.ZipFile(z_file, 'r')
    for file in f.namelist():
        f.extract(file, path)


def get_initialization(test_type, platform_url, workspace_name):
    # 对输入的URL做判断，末尾没加"/" 统一处理加上"/"
    if not platform_url.endswith('/'):
        platform_url += '/'
    # ATP平台端初始化执行端的mqtt接口
    initialization_mqtt_url = platform_url + 'software/execution/initialization/'
    # 如果执行工作区名称为默认值，生成随机数
    if workspace_name == '':
        # 根据当前网卡和时间组成随机数
        workspace_name = uuid.uuid4().hex
    # mqtt、android、ios、web执行端的通用参数
    up_data = {'name': workspace_name, 'execution_type': test_type}
    # mqtt执行端的特殊参数
    if test_type == 4:
        up_data['information'] = json.dumps({'system': platform.system()})
    # 向ATP平台端发送初始化执行端请求
    requests_data = requests.post(initialization_mqtt_url, data=up_data)
    requests_json = requests_data.json()
    print('[Cli info]> ' + str(requests_json))
    # 判断平台端初始化结果
    if requests_json['code'] != 200:
        print('[Cli Error]> 执行端服务初始化失败')
        sys.exit()
    # 附带上经过上面处理的ATP平台URl
    requests_json['data']['platform_url'] = platform_url
    requests_json['data']['redis_ip'] = platform_url.replace('http://', '').replace('/', '')
    requests_json['data']['test_type'] = test_type
    return requests_json


if __name__ == '__main__':
    main()
