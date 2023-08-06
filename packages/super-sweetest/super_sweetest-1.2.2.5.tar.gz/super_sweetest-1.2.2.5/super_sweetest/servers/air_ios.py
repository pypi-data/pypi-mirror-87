# coding=utf-8

# @Time: 2020/4/10 16:42
# @Auther: liyubin


from airtest.core.api import *
from poco.drivers.ios import iosPoco
from super_sweetest.servers.ios_server import kill_ios_tagent_server
from super_sweetest.servers.ios_server import run_ios_tagent_server
from super_sweetest.servers.ios_server import run_iproxy8100
from super_sweetest.servers.ios_server import post_iproxy_status

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
airtest ios  服务
"""


class AirIos():

    def setup_air_ios(self, device_name, app_package, desired_caps):
        """
        connect_device airtest， init poco
        """

        auto_setup(__file__)

        # 获取配置
        iostagen_file = desired_caps.get('iostagen_file', '未配置')
        platform = desired_caps.get('platform', '未配置')

        # 服务启动 获取iproxy status
        iproxy_status = self.setup_server(iostagen_file, platform, device_name)

        # 二次启动，失败后抛出异常
        if iproxy_status != 'success':
            sec_iproxy_status = self.setup_server(iostagen_file, platform, device_name)
            assert sec_iproxy_status == 'success', '当前手机 %s 启动服务失败, 请检查手机连接状态，重启手机重装' \
                                                   '和手机上WebDriverAgent应用已信任，' \
                                                   '请确认当前手机已在此Mac电脑启动WebDriverAgent成功，' \
                                                   '并成功连接airtest' % device_name

        iproxy_url = 'http://127.0.0.1:8100'  # 端口转发 iproxy 8100 8100

        # 或者使用connect_device函数
        connect_device("ios:///" + iproxy_url)

        # poco服务,先连接设备再初始化
        poco = iosPoco()

        start_app(app_package)

        sleep(8)
        return poco

    @staticmethod
    def setup_server(iostagen_file, platform, devicename):
        """airtest ios前置条件server"""
        kill_ios_tagent_server(devicename)
        run_iproxy8100()
        run_ios_tagent_server(iostagen_file, platform, devicename)
        iproxy_status = post_iproxy_status()
        return iproxy_status

    @staticmethod
    def teardown_air_ios(g):
        """关闭app，停止poco实例"""
        stop_app(g.appPackage)
        kill_ios_tagent_server(g.deviceName)

if __name__ == '__main__':
    desired_caps = {'iostagen_file': '/Users/liyubin1/Desktop/iOS-Tagent11',
                    'platform': 'iOS',
                    }

    deviceName = 'LDS-Z-C5197'
    app_package = 'com.apple.Preferences'

    air = AirIos()
    air.setup_air_ios(deviceName, app_package, desired_caps)
