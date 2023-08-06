# coding:utf-8

# @Time: 2020/3/10 16:42
# @Auther: liyubin


from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from super_sweetest.servers.common import read_data, write_data

########################################
# from airtest.core.settings import Settings
# 全局伐值

# Settings.THRESHOLD_STRICT = 0.6  # assert_exists语句的默认阈值，一般比THRESHOLD更高一些
# Settings.THRESHOLD = 0.6  # 其他语句的伐值
# Settings.OPDELAY = 1  # 每一步操作后等待1秒再进行下一步操作
# Settings.FIND_TIMEOUT = 10  # 图像查找超时时间
# Settings.CVSTRATEGY = ["surf", "tpl", "brisk"]  # 修改图片识别算法顺序，只要成功匹配任意一个符合设定阙值的结果，程序就会认为识别成功

########################################

"""
airtest android  服务
"""


class AirAndroid():

    def setup_air_android(self, device_name, app_package, desired_caps):
        """
        connect_type_list: list
        connect_device airtest， init poco
        通过ADB连接本地Android设备
        init_device("Android")
        或者使用connect_device函数
        cap_method=JAVACAP&&ori_method=ADBORI&&touch_method=ADBTOUCH 对应 'javacap', 'ADB orientation', 'ADB touch'
        """

        auto_setup(__file__)

        # 通过不同method连接手机
        global CONNECT_TYPE_LIST, desired_caps_g
        desired_caps_g = desired_caps
        CONNECT_TYPE_LIST = desired_caps_g.get('connect_type_list', '未配置')
        assert isinstance(CONNECT_TYPE_LIST, list), "格式错误 正确格式-> 'connect_type_list':['', 'javacap', 'adbori', 'adbtouch'],"
        c_t = [C_T.lower() for C_T in CONNECT_TYPE_LIST]

        if 'javacap' in c_t and 'adbori' in c_t and 'adbtouch' in c_t:
            method = "?cap_method=JAVACAP&&ori_method=ADBORI&&touch_method=ADBTOUCH"
        elif 'adbori' in c_t and 'adbtouch' in c_t:
            method = "?ori_method=ADBORI&&touch_method=ADBTOUCH"
        elif 'javacap' in c_t and 'adbtouch' in c_t:
            method = "?cap_method=JAVACAP&&touch_method=ADBTOUCH"
        elif 'javacap' in c_t and 'adbori' in c_t:
            method = "?cap_method=JAVACAP&&ori_method=ADBORI"
        elif 'javacap' in c_t:
            method = "?cap_method=JAVACAP"
        else:
            method = ''

        connect_device("Android:///" + device_name + method)

        # install("your apk")
        AirAndroid.put_full(device_name)

        # poco实例化,需先连接设备
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

        sleep(3)
        start_app(app_package)
        sleep(8)
        return poco

    @staticmethod
    def teardown_air_android(g):
        """
        关闭app，停止poco实例
        :param g:
        """
        AirAndroid.put_null(g.deviceName)
        g.poco.stop_running()
        # os.system('adb -s {} usb'.format(g.deviceName))
        if desired_caps_g.get('stop_app', True):
            stop_app(g.appPackage)
        AirAndroid.sync_connect_log(g.deviceName, CONNECT_TYPE_LIST)

    # 无device_name时只适用首次启动执行端时，否则多次执行导致adb命令异常,不支持多设备连接使用
    # 如提示adb版本不同，将airtest的adb.exe替换android sdk
    @staticmethod
    def put_full(device_name):
        """隐藏指定手机状态栏通知栏"""
        os.system('adb -s {} shell settings put global policy_control immersive.full=*'.format(device_name))

    @staticmethod
    def put_null(device_name):
        """恢复指定手机状态栏导航栏"""
        os.system('adb -s {} shell settings put global policy_control null'.format(device_name))

    @staticmethod
    def sync_connect_log(device_name, method):
        """
        更新添加已运行的log
        :param device_name:
        :param method:
        """
        connect_type_file = './connect_type.json'
        # 首次运行不存在先创建再读取
        if not os.path.exists(connect_type_file):
            write_data(connect_type_file, {}, 'json', 'w+')
        # 读取最新配置
        connect_type = read_data(connect_type_file, 'json', 'r+')
        # 更新/新增 配置
        connect_type[device_name] = method
        # 更新写入配置key：value
        write_data(connect_type_file, connect_type, 'json', 'w+')
