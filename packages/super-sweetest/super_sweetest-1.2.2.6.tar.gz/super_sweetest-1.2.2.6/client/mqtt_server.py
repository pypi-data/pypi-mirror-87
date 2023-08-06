# coding:utf-8

import os
import sys
import time
import configparser
from pathlib import Path
from client.mqtt_server_run import MqttRun


def mqtt_workspace(sys_name, data):
    """
    创建mqtt自动化测试执行工作空间并自动/手动执行
    """
    data_dict = {
        'name': data['name'],
        'platform_url': data['platform_url'],
        'git_url': data['git_url'],
        'redis_ip': data['redis_ip'],
        'redis_key': data['redis_key'],
        'redis_port': data['redis_port'],
        'execution_id': data['execution_id'],
    }
    current_path = os.path.abspath(__file__)
    current_dir = Path(os.path.dirname(current_path))
    cwd_dir = Path.cwd()
    work_space = cwd_dir / ('x_atp_mqtt_server_%s' % data_dict['name'])
    os.mkdir(str(work_space))
    create_profile(data=data_dict, work_space=work_space, current_dir=current_dir)
    print('\n###   工作空间   ###\nx_atp_mqtt_server_%s\n' % data_dict['name'])
    # 后台执行atp执行端
    if sys_name == 'Linux':
        daemon_start(data=data_dict, work_space=work_space)
        print('###   X-ATP自动化测试执行端服务已在后台运行   ###')
    else:
        print('###   您需要手动启动执行端服务   ###\ncd x_atp_mqtt_server_%s\npython mqtt_server_run.py\n'
              % data_dict['name'])


def create_profile(data, work_space, current_dir):
    """
    在程序执行的当前目录下创建配置文件和执行程序
    """
    # 处理GIT仓库URL里的特殊字符
    data['git_url'] = data['git_url'].replace('%40', '@')
    config = configparser.ConfigParser()
    # 创建config配置文件
    file = 'config.ini'
    config.read(work_space / file)
    config.add_section('ATP-Server')
    # 平台URL、GIT仓库URL、工作空间名、队列IP、队列KEY、队列端口号、注册ID
    config.set('ATP-Server', 'platform_url', data['platform_url'])
    config.set('ATP-Server', 'name', data['name'])
    config.set('ATP-Server', 'git_url', data['git_url'])
    config.set('ATP-Server', 'redis_ip', data['redis_ip'])
    config.set('ATP-Server', 'redis_key', str(data['redis_key']))
    config.set('ATP-Server', 'redis_port', str(data['redis_port']))
    config.set('ATP-Server', 'execution_id', str(data['execution_id']))
    # 保存config配置文件
    with open(work_space / file, 'w', encoding='utf-8') as configfile:
        config.write(configfile)
    # 拷贝mqtt_server_run执行文件到工作空间
    with open(work_space / 'mqtt_server_run.py', 'w', encoding='utf-8') as file_obj:
        with open(current_dir / 'mqtt_server_run.py', 'r', encoding='utf-8') as mqtt_run:
            file_obj.write(mqtt_run.read())
    # 拷贝runcase.py
    with open(work_space / 'run_case.py', 'w', encoding='utf-8') as file_obj:
        with open(current_dir / 'run_case.py', 'r', encoding='utf-8') as mqtt_run:
            file_obj.write(mqtt_run.read())


def daemon_start(data, work_space, stdin='/dev/null', stdout='/dev/null', stderr='/var/log/x-client-mqtt-server.error'):
    """
    启动守护进程
    """
    # fork出一个子进程，父进程退出
    try:
        pid = os.fork()
        # 父进程退出函数
        if pid > 0:
            return
    except OSError as e:
        sys.stderr.write("[mqtt Server Error]> 第一次 fork 失败, " + e.strerror)
        os._exit(1)
    # 创建日志存放目录，设置日志输出文件
    log_file = Path("atp_log")
    if not log_file.is_dir():
        os.mkdir(str(log_file))
    sys.stdin = open(stdin, 'r')
    sys.stdout = open(stdout, 'a+')
    sys.stderr = open(stderr, 'a+')
    # 等待父进程结束
    time.sleep(2)
    # 父进程退出后，子进程由init收养
    # setsid使子进程成为新的会话首进程和进程组的组长，与原来的进程组、控制终端和登录会话脱离
    os.setsid()
    # 防止在类似于临时挂载的文件系统下运行，例如/mnt文件夹下，这样守护进程一旦运行，临时挂载的文件系统就无法卸载了，这里我们推荐把当前工作目录切换到根目录下
    os.chdir(work_space)
    # 设置用户创建文件的默认权限，设置的是权限“补码”，这里将文件权限掩码设为0，使得用户创建的文件具有最大的权限。否则，默认权限是从父进程继承得来的
    os.umask(0)
    # 第二次进行fork,为了防止会话首进程意外获得控制终端
    try:
        pid = os.fork()
        if pid > 0:
            # 父进程退出
            os._exit(0)
    except OSError as e:
        sys.stderr.write("[mqtt Server Error]> 第二次 fork 失败, " + e.strerror)
        os._exit(1)
    # 此时改程序已经是守护进程了，再执行需要后台执行的程序即可
    r = MqttRun(data)
    r.run()
