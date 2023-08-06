# coding:utf-8

import os
import sys
import time
import shutil
import json
import configparser
import requests
import redis
from git import Repo
import platform
import datetime
from super_sweetest.servers.common import write_data, read_data


class MqttRun:
    """
    mqtt自动化测试执行端
    """

    def __init__(self, run_data):
        # 工作空间名
        self.NAME = run_data['name']
        # 平台URL
        self.PLATFORM_URL = run_data['platform_url']
        # 队列IP、队列KEY、队列端口号
        self.REDIS_IP = run_data['redis_ip']
        self.REDIS_KEY = int(run_data['redis_key'])
        self.REDIS_PORT = int(run_data['redis_port'])
        # GIT仓库URL
        self.GIT_URL = run_data['git_url']
        if self.GIT_URL.count('@') - 1 != 0:
            self.GIT_URL = self.GIT_URL.replace('@', '%40', self.GIT_URL.count('@') - 1)
        # 执行端注册ID
        self.EXECUTION_ID = int(run_data['execution_id'])
        # 通过队列IP、队列KEY、队列端口号参数连接Redis数据库
        self.POOL = redis.ConnectionPool(host=self.REDIS_IP, port=self.REDIS_PORT, db=self.REDIS_KEY,
                                         decode_responses=True)
        self.REDIS_POOL = redis.Redis(connection_pool=self.POOL)
        # 初始日志文件的起始行号
        self.initial_log_line = 0
        # 初始日志文件的日期前缀
        self.initial_log_time = ''

    @staticmethod
    def mkdir_and_del(src_path):
        """
        删除旧文件夹再创建新文件夹
        """
        if os.path.isdir(src_path):
            shutil.rmtree(src_path)
        os.mkdir(src_path)

    @staticmethod
    def reset_file_tree(file_name, project_name, test_environment):
        """
        将Git用例仓库里的project_name项目目录中的file_name文件复制到执行目录中
        """
        case_path = os.path.join(os.getcwd(), "git_case")
        lib_dst_path = os.path.join(
            case_path, project_name + "-Project-mqtt", test_environment, file_name)
        # 确定Git用例存储库中是否有一个lib_dst_path目录
        if os.path.isdir(lib_dst_path):
            lib_src_path = os.path.join(os.getcwd(), file_name)
            # 确定执行目录下是否有一个lib_src_path目录
            if os.path.isdir(lib_src_path):
                shutil.rmtree(lib_src_path)
            shutil.copytree(lib_dst_path, lib_src_path)

    def pull_case(self):
        """
        clone（拉取）和pull（更新）测试用例仓库的内容
        """
        try:
            git_case_path = os.path.join(os.getcwd(), "git_case")
            if os.path.isdir(git_case_path):
                print("[mqtt Server Run Info]> 发现 git_case 目录, 执行更新最新测试用例流程")
                repo = Repo.init(path=git_case_path)
                remote = repo.remote()
                remote.pull()
                print("[mqtt Server Run Info]> 已更新 GitLab 仓库中 git_case 项目的测试用例")
            else:
                print("[mqtt Server Run Info]> 找不到 git_case 目录, 执行下载新测试用例流程")
                Repo.clone_from(url=self.GIT_URL, to_path=git_case_path)
                print("[mqtt Server Run Info]> 已下载 GitLab 仓库中 git_case 项目的测试用例")
        except:
            pass

    def all_mkdir_copy(self, test_project, test_environment):
        """
        复制指定测试项目、测试类型、测试环境中的相关目录到自动化运行目录下
        """
        self.reset_file_tree(file_name="lib", project_name=test_project, test_environment=test_environment)
        self.reset_file_tree(file_name="data", project_name=test_project, test_environment=test_environment)
        self.reset_file_tree(file_name="element", project_name=test_project, test_environment=test_environment)
        self.reset_file_tree(file_name="testcase", project_name=test_project, test_environment=test_environment)
        self.reset_file_tree(file_name="files", project_name=test_project, test_environment=test_environment)
        MqttRun.mkdir_and_del(src_path=os.path.join(os.getcwd(), "JUnit"))
        MqttRun.mkdir_and_del(src_path=os.path.join(os.getcwd(), "report"))
        MqttRun.mkdir_and_del(src_path=os.path.join(os.getcwd(), "details"))


    def write_testdata_and_run(self, test_name):
        """
         写入测试所需数据
        :param test_name:
        """
        if test_name:
            sys = platform.system()  # 操作系统
            # MQTT
            run_case_data = {'test_name': test_name, 'status': False}
            write_data('./run_case_data.json', run_case_data, 'json', 'w+')
            if sys.lower() in ('windows'):
                # windows 启动run_case模块
                os.popen('start python ./run_case.py')
            else:
                # 其他系统启动
                os.system('nohup python3 ./run_case.py &')

        # 如果运行结束状态status：True，继续下一步
        # 隐式等待/避免执行端假死
        now_time_flag = datetime.datetime.now()
        while True:
            time.sleep(5)
            if (datetime.datetime.now() - now_time_flag).seconds > 3600:
                break
            else:
                status = read_data('./run_case_data.json', 'json', 'r')
                if status['status']:
                    return status.get('msg', '')


    def read_log_file(self):
        """
        从以日期为维度统计的日志中提取出本次的日志文件，保存至log/new.log
        """
        # 如果日志文件的日期前缀不是当天的日期
        if self.initial_log_time != time.strftime('%Y%m%d'):
            # 重置日志文件的前缀、起始行数
            self.initial_log_time = time.strftime('%Y%m%d')
            self.initial_log_line = 0
        # 读取日志文件的全部字符串
        with open(os.path.join(os.getcwd(), 'log', time.strftime('%Y%m%d.log')), "r", encoding='utf-8') as f:
            # 将日志字符串按换行符拆成列表
            log_file_data = f.read().split('\n')
        # 如果起始日志行反而比最大行数都大的话
        if self.initial_log_line > len(log_file_data):
            # 重置日志文件的起始行数
            self.initial_log_line = 0
        # 按行号增量取出本次测试的日志
        log_file_list = log_file_data[self.initial_log_line:]
        # 更新日志文件的起始行号
        self.initial_log_line = len(log_file_data)
        # 存储日志信息的字典
        log_file_dict = {}
        # 用这个变量控制每一行都是不重复的
        previous_row = ''
        # 整理每一行日志
        for i in range(len(log_file_list)):
            # 不读取空行
            if log_file_list[i] == '':
                continue
            # 不读取和上一行重复的数据
            if log_file_list[i] == previous_row:
                continue
            # 判断当前行是否包含特殊分割符
            if ']: #  ' in log_file_list[i]:
                # 将日志信息按用途分类
                log_file_dict[i] = {
                    'time': log_file_list[i][:23],
                    'grade': log_file_list[i][25:log_file_list[i].find(']')],
                    'message': log_file_list[i][log_file_list[i].find(']')+6:],
                }
            else:
                # 如果是错误信息，上传特殊格式
                log_file_dict[i] = {
                    'time': '',
                    'grade': '',
                    'message': log_file_list[i].replace(' ', '&nbsp;'),
                }
            # 更新上一行的数据
            previous_row = log_file_list[i]
        # 在log目录下写入新的日志文件
        with open(os.path.join('log', 'new.log'), "w", encoding='utf-8') as file:
            file.write(json.dumps(log_file_dict))

    def post_heartbeat(self, status, localtime=None, task_dict=None, remark=None):
        """
        # 描述:
            发送心跳请求到ATP服务器（失败重试，直至恢复连接）
        # 用法0（第一次）:
            self.post_heartbeat(status=0)
        # 用法1（正常）:
            self.post_heartbeat(status=1, localtime=[调用时间])
        # 用法2（任务无法完成/放弃任务，需要在备注中提交错误信息）:
            self.post_heartbeat(status=2, localtime=[调用时间], task_dict=[任务字典], remark=[备注])
        # 用法3（开始执行任务）:
            self.post_heartbeat(status=3, localtime=[调用时间], task_dict=[任务字典])
        # 用法4（任务执行完成，上传测试报告）:
            self.post_heartbeat(status=4, localtime=[调用时间], task_dict=[任务字典])
        # 用法5（执行端异常，需要在备注中提交异常信息）:
            self.post_heartbeat(status=5, remark=[备注])
        # 用法6（执行端离线）:
            self.post_heartbeat(status=6)
        # 用法7（执行端变更信息，需要在备注中提交变更信息字典字符串）:
            self.post_heartbeat(status=7, remark=[备注])
        """
        if not localtime:
            localtime = time.asctime(time.localtime(time.time()))
        # ATP平台端上执行端心跳的mqtt接口
        heartbeat_mqtt_url = self.PLATFORM_URL + 'software/execution/heartbeat/'
        # 心跳请求连接次数
        connect = 0
        # 开始发送心跳请求（不成功便成仁，真男人从不回头看爆炸）
        while True:
            # 捕获异常
            try:
                # 执行端心跳参数
                up_data = {'id': self.EXECUTION_ID, 'status': status, 'task_dict': json.dumps(task_dict),
                           'remark': remark}
                # 状态为4时，组织待上传的次数报告文件
                if status == 4:
                    # 拔高变量的层级
                    files_report = None
                    files_junit = None
                    # 取出XXX-Report@XXXXXX_XXX.xlsx的测试报告文件名
                    for _root, _dirs, files in os.walk(os.path.join('report', task_dict['test_name'])):
                        files_report = files[0]
                    # 取出XXX-Report@XXXXXX_XXX.xml的测试汇总文件名
                    for _root, _dirs, files in os.walk('JUnit'):
                        files_junit = files[0]
                    # 读取测试报告文件
                    with open(os.path.join('report', task_dict['test_name'], files_report), 'rb') as fp1:
                        files_report_obj = fp1.read()
                    # 读取测试汇总文件
                    with open(os.path.join('JUnit', files_junit), 'rb') as fp2:
                        files_junit_obj = fp2.read()
                    # 读取测试详情文件
                    with open(os.path.join('details', 'details.txt'), 'rb') as fp3:
                        files_details_obj = fp3.read()
                    # 读取测试日志文件
                    self.read_log_file()
                    with open(os.path.join('log', 'new.log'), 'rb') as fp4:
                        files_log_obj = fp4.read()
                    # 汇总XXX-Report@XXXXXX_XXX.xlsx、XXX-Report@XXXXXX_XXX.xml、details.txt、new.log文件对象
                    files_obj = {
                        'file_obj': (str(task_dict['queue_id']) + '.xlsx', files_report_obj),
                        'file_obj_junit': (str(task_dict['queue_id']) + '.xml', files_junit_obj),
                        'file_obj_details': (str(task_dict['queue_id']) + '.txt', files_details_obj),
                        'file_obj_log': (str(task_dict['queue_id']) + '.log', files_log_obj)
                    }
                else:
                    files_obj = {}
                # 向ATP平台端发送执行端心跳请求
                requests_data = requests.post(heartbeat_mqtt_url, data=up_data, files=files_obj)
                requests_json = requests_data.json()
                # 判断平台端心跳状态处理结果
                if requests_json['code'] == 200:
                    # 心跳请求响应成功，结束死循环
                    print('[Heartbeat][' + localtime + ']> ' + str(requests_json['data']))
                    break
                # 服务器内部错误错误
                else:
                    print('[Heartbeat Error][' + localtime + ']> > ' + str(requests_json))
            # 网络请求错误
            except Exception as exc:
                print('[Heartbeat Error][' + localtime + ']> ' + str(exc))
            # 30秒后重新发送心跳请求
            time.sleep(30)
            connect += 1
            print('[Heartbeat Error][' + localtime + ']> 进行第 ' + str(connect) + ' 次重新连接')
            # 防止 异常后文件找不到 进入死循环 join argument must be str or bytes, not 'NoneType'
            if connect > 2:
                break


    def run(self):
        self.mkdir_and_del(src_path=os.path.join(os.getcwd(), "log"))
        self.mkdir_and_del(src_path=os.path.join(os.getcwd(), "snapshot"))
        self.pull_case()
        print('[mqtt Server Run Info]> 检测是否有历史任务未完成')
        # 上报第一次/刚启动执行端的心跳
        self.post_heartbeat(status=0)
        while True:
            time.sleep(10)
            try:
                # 获取Redis任务队列的信息长度
                length = self.REDIS_POOL.llen(self.EXECUTION_ID)
                # 生成当前时间字符串，用于打印输出
                localtime = time.asctime(time.localtime(time.time()))
                # 如果Redis任务队列的信息长度小于0，那就说明没有任务
                if length > 0:
                    print('[mqtt Server Run Info][' + localtime + ']> ' + '发现新的任务信息')
                    self.pull_case()
                    value_dict = json.loads(self.REDIS_POOL.lpop(self.EXECUTION_ID))
                    # 上报开始执行任务的心跳
                    self.post_heartbeat(status=3, localtime=localtime, task_dict=value_dict)
                    try:
                        print('[Queue Task Dict]> ' + str(value_dict))
                        print('[mqtt Server Run Info]> 重置 X-Sweetest 测试运行环境')
                        self.all_mkdir_copy(test_project=value_dict['test_project'],
                                            test_environment=value_dict['test_environment'])
                        print('[mqtt Server Run Info]> X-Sweetest 测试运行环境就绪')
                        self.write_testdata_and_run(test_name=value_dict['test_name'])
                        print('[mqtt Server Run Info]> X-Sweetest 测试完成并上传测试报告')
                        # 上报任务执行完成的心跳
                        self.post_heartbeat(status=4, localtime=localtime, task_dict=value_dict)
                        print('[mqtt Server Run Info]> 测试报告上传完毕')
                    except Exception as exc:
                        # 上报任务无法完成的心跳
                        self.post_heartbeat(status=2, localtime=localtime, task_dict=value_dict, remark=str(exc))
                        print('[mqtt Server Run Error]> ' + str(exc))
                else:
                    # 上报正常的心跳
                    self.post_heartbeat(status=1, localtime=localtime)
                # 调用Flush，从内存中刷入日志文件
                sys.stdout.flush()
            except Exception as exc:
                # 上报执行端异常的心跳
                self.post_heartbeat(status=5, remark=str(exc))
                print('[mqtt Server Run Error]> ' + str(exc))


if __name__ == '__main__':
    # 读取工作空间目录下的config配置文件
    config_file = 'config.ini'
    config = configparser.RawConfigParser()
    config.read(config_file, encoding='utf-8')
    # 读取配置中的ATP-Server内容
    data = dict(config.items('ATP-Server'))
    # 创建mqtt自动化测试执行端对象
    r = MqttRun(run_data=data)
    # 启动mqtt自动化测试执行端
    r.run()
