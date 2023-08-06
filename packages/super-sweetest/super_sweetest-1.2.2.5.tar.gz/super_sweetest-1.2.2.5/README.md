# x-atp-app-mqtt



### 开始


 ### 安装
 

```markdown


 1.Andrid/IOS/MQTT自动化测试项目
 
 
 2.sweettest（基于版本1.2）
 
 
 3.运行环境windows(android/mqtt) / MAC(ios)
 
 
 4.pip安装：pip install sweetest
 
    如果超时：pip  install  -i  https://pypi.doubanio.com/simple/  --trusted-host pypi.doubanio.com sweetest
    
 
 5.豆瓣安装（如果安装airtest,poco超时）：
 
   pip  install  -i  https://pypi.doubanio.com/simple/  --trusted-host pypi.doubanio.com airtest
   pip  install  -i  https://pypi.doubanio.com/simple/  --trusted-host pypi.doubanio.com pocoui
   
   
 6.pip升级：pip install -U sweetest
 
 
 7. 部署执行端的电脑首次需安装的依赖
 
    a.本地电脑安装：git.exe
    b.pip install redis  
    c.pip install gitpython==3.1
 


```
 

 ### 部署方式
 
```markdown


 1.环境搭建：
    Android： 环境搭建 http://confluence.leedarson.com/pages/viewpage.action?pageId=1278930（如通过airtest方式运行，可不安装appium和nodejs）
    IOS：     环境搭建 http://confluence.leedarson.com/pages/viewpage.action?pageId=1279273
    MQTT：    参考（2.运行方式）
 
 
 2.运行方式：
    Android/IOS
        a.配置 run_sync_device.py中PLATFORM_URL 需要监听的服务器地址
        b.IOSTANGE_FILE = '/Users/liyubin1/Desktop/iOS-Tagent11'  # iOS-Tagent服务在mac的目录位置
        c.双击/命令行 run_sync_device.py运行即可, 不可用pycharm运行
        
    MQTT:
        a.windows命令行生成： sweetest -r http://172.24.185.55/ -m -n MQTT执行端--001    即可生成，按提示操作
    
    
 3.关于android/ios  work
 
    a.运行后，每次连接新的手机会自动创建一个对应手机的work
    b.根据提示进入对应手机以： x_atp_app_server_手机名称 的目录，然后双击x-atp-app.py启动对应手机work成功
    c.在监听的平台上即以查看到android/ios执行机的状态
    d.手机断开连接时，对应的android/ios work会继续运行，但是平台执行机状态会显示离线不可选，再次连接手机后恢复正常。
    e.从平台下发任务或者定时任务时，先检查平台执行端状态中对应的android work的connect_type信息存在且正确，如果不正确，运行本地调试
    的run_case.py来同步connect_type信息：具体代码已在用例demo中，如下：
             # 发送connect_type信息到平台
            import requests
            host = 'http://172.24.24.10' # 需配置自动化平台IP
            # host = 'http://127.0.0.1:8000' # 需配置自动化平台IP
            connect_url = host + '/software/sweetest/mobile/collect/'
            with open('./connect_type.txt', 'r', encoding='utf8')as fp1:
                connect_type_ = fp1.read()
            data_ = {'connect_type': connect_type_}
            res = requests.post(connect_url, data_).json()
            print('--- %s ---'%res)
            
```

 
 ### 新增

```markdown


 1.图片截取和比对 snapshot/expected/ 图片内容需手动，或运行一次就会自动保存，下次运行开始比对
 

 2.每次执行端运行snapshot/expected/不删除比对素材库 和 log 历史日志
 
 
 3.提交代码时执行teardown，一次清理测试生成数据
 
 
 4.增加class_name 的 elements 通过 index定位，通过 element表 备注行 添加index数值 点击/输入
 
 
 5.新方案加入airtest支持，同时兼容appium
 
 
 6.执行端分离为：数据处理模块与运行模块
 
 
 7.增加失败步骤截图转base64和存入步骤数据
 
 
 8.新增检测接入手机和创建Android/ios 自动化work 目录
 
 
 9.新增MQTT请求支持
 
 9.已更新到1.1.9.8版本


```


 ### 代码版本控制
 
```markdown 

	
 1.test分支：开发测试最新版，对应lds-atp 的test分支部署

 2.master分支：正式稳定版本，每次部署正式环境，合并test到master，对应lds-atp 的master分支部署
 
 
```
