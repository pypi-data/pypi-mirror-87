# coding: utf-8

# @Time:2020/3/15 12:34
# @Auther:sahala


from setuptools import setup, find_packages  # 这个包没有的可以pip一下

setup(
    name="super_sweetest",  # 这里是pip项目发布的名称
    version="1.2.2.5",  # 版本号，数值大的会优先被pip
    keywords=("pip", "super_sweetest", "featureextraction"),
    description="automation tools",
    long_description="加入小Q智能AI识别 0接入工作量、多词语忽略检查, 语言类型配置到plan_name#ZH-TestCase.xlsx",
    license="MIT Licence",

    url="http://github.com/SahalaProject/super_sweetest",  # 项目相关文件地址，一般是github
    author="liyubin",
    author_email="1399393088@qq.com",
    ########################
    # 精确控制打包文件
    # packages=find_packages("super_sweetest"),
    # package_dir = {"": "super_sweetest"},
    # package_data = {
    #     "": ["*.py", "example/*.zip"], # 根目录下的文件
    #     # "example": ["*.zip"]
    # },
    # exclude_package_data={"": ["README.md"]}, # 过滤打包文件
    ########################
    packages=find_packages(), # 默认加载py
    include_package_data=True,

    platforms="any",
    install_requires=[
                      "Appium-Python-Client",
                      "certifi",
                      "chardet",
                      "idna",
                      "injson",
                      "Pillow",
                      "requests",
                      "selenium",
                      "urllib3",
                      "xlrd",
                      "XlsxWriter",
                      "airtest",
                      "pocoui",
					  "validator_sa",
					  "paho-mqtt",
					  "openpyxl",
					  "arrow",
					  "requests_toolbelt",
					  "GitPython",
					  "baidu-aip",
                      ],  # 这个项目需要的第三方库
    entry_points={
            'console_scripts': [
                'super_sweetest = client.cli:main'
            ]
        }, # 命令行直接启动的命令
)



# 步骤：
# 使用说明：https://setuptools.readthedocs.io/en/latest/setuptools.html#including-data-files

# 1.setup.py放在被打包同级
    # 本地打包项目文件
    # python setup.py sdist

# 2.上传项目到pypi服务器
    # pip install twine
    # twine upload dist/name.tar.gz

# 3.下载上传的库
    # pip install name


# 4.安装打包的本地文件
    # tar -xzvf super.tar.gz
    # python setup.py install