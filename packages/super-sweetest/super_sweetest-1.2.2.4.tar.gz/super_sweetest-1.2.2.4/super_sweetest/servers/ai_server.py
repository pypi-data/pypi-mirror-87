# coding:utf-8

# @Time: 2020/10/28 11:44
# @Auther: liyubin

import requests
from super_sweetest.config import URL_LDS_UI, URL_BAIDU_AIP

"""
人工智能 AI识别 UI/UI文本
UI     基于百度AI平台，训练素材
UI文本 基于百度AIP识别高精度接口
"""


def recognition_ui(input_file):
    """
    UI识别正确和异常
    :param input_file:
    :return:
    """
    file = {'file': open(input_file, 'rb')}
    data = {'code': 117}
    res = requests.post(URL_LDS_UI, data=data, files=file).json()
    return res


def get_ui_results(response):
    """
    获取UI识别中识别结果
    :param response:
    :return:
    """
    return response.get('msg', '')


def recognition_text(input_file, language):
    """
    UI文本识别
    :param input_file:
    :param language: app_config.json 设定的语言,增加识别文本正确性
    :return:
    """
    import json
    file = {'file': open(input_file, 'rb')}  # 发送后接口中通过file.read()获取值
    OPTIONS = {}
    OPTIONS["language_type"] = 'auto_detect' if language is 'CHN_ENG' else language  # 当设置中英文时，用auto_detect，识别效果好
    OPTIONS["detect_direction"] = "true"
    OPTIONS["detect_language"] = "true"
    OPTIONS["probability"] = "true"
    data = {
            'code': 117,
            'options': json.dumps(OPTIONS)
            }
    res = requests.post(url=URL_BAIDU_AIP, data=data, files=file).json()
    return res


def get_words(response):
    """
    获取aip接口返回中的words
    :param response:
    :return:
    """
    if 'words_result' in response.keys():
        new_worlds = []
        for words in response.get('words_result', []):
            new_worlds.append(words.get('words'))
        return new_worlds
    # 超过每日限量
    assert 'limit reached' not in response.get('error_msg'), '⚠ ⚠ ⚠ ⚠ 文本识别调用次数超过当日限量...'


def get_screen_text(file_path):
    """
    获取截图中文本信息
    :return:
    """
    from super_sweetest.snapshot import get_air_screenshot # 防止初始化时 循环导入报错，导入写在这里
    assert str(file_path).endswith('.png'), '截图路径必须以.png结尾'
    get_air_screenshot(file_path=file_path)
    response = recognition_text(file_path)
    return get_words(response)



"""
通过unicode编码范围判断字符
"""


def is_in_copywriting(words, copywriting_data):
    """
    检查单词词语是否在文案中
    直接检查识别后数据，不对数据替换标点符号
    :param words:
    :param copywriting_data:
    :return:
    """
    if words in copywriting_data:
        return True
    return False


def replace_punctuate(words, uchar=False, baidu_aip=False):
    """
    str中标点符号替换为'' 适合unicode编码范围判断单个字符
    :param words:
    :param uchar: 忽略所有符号
    :param baidu_aip: 忽略百度识别后异常的符号
    :return:
    """
    punctuate_list_uchar = [' ', '`', '~', '@', '!', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '=', '+', '/',
                            '|', '[',
                            ']', '{', '}', '.', ',', '，', '。', '?', '、', '<', '>', '《', '》', '！', '·', '（',
                            '）', '【', '】', ':', ';', '；', '"', '’', '”']
    punctuate_list_officers = ['<', '>', '>>>>']  # 忽略baidu_aip识别后有误的标点
    if uchar:
        punctuate_list = punctuate_list_uchar
    elif baidu_aip:
        punctuate_list = punctuate_list_officers
    else:
        punctuate_list = ''
    new_words = ''
    new_words_list = []
    for word in words:
        if word not in punctuate_list:
            new_words = new_words + word if uchar else None
            new_words_list.append(word)
    return new_words if uchar else new_words_list


def is_chinese(uchar):
    """
    是否为中文
    """
    if u'\u4e00' <= uchar <= u'\u9fa5':
        return True
    return False


def is_number(uchar):
    """
    是否为数字
    """
    if u'\u0030' <= uchar <= u'\u0039':
        return True
    return False


def is_english(uchar):
    """
    是否为英文字母
    """
    if u'\u0041' <= uchar <= u'\u005a' or u'\u0061' <= uchar <= u'\u007a':
        return True
    return False


def is_other(uchar):
    """
    判断是否非 汉字/数字/英文 字符
    """
    if not (is_chinese(uchar) or is_number(uchar) or is_english(uchar)):
        return True
    return False


def is_japan(uchar):
    """
    是否为日文
    """
    if u'\u0800' <= uchar <= u'\u4e00 ':
        return True
    return False


def is_korean(uchar):
    """
    是否为韩文
    """
    if u'\uAC00' <= uchar <= u'\uD7A3':
        return True
    return False


def is_France_and_german(uchar):
    """
    德文或法文
    :param uchar:
    :return:
    """
    if u'\u00C0' <= uchar <= u'\u00FF':
        return True
    return False


def is_russian(uchar):
    """
    是否为俄语
    """
    if u'\u0400' <= uchar <= u'\u052f':
        return True
    return False




def is_language(word_list):
    """
    通过文本判断和输出是那种语言
    :return:
    """
    language = []
    for i in range(len(word_list)):
        uchar_ = word_list[i].replace(' ', '')
        if is_english(uchar_):
            language.append('en')
        elif is_chinese(uchar_):
            language.append('zh')
        elif is_russian(uchar_):
            language.append('ru')
        elif is_korean(uchar_):
            language.append('kr')
        elif is_japan(uchar_):
            language.append('ja')
        else:
            language.append(uchar_)
    return max(language, key=language.count)  # 获取list出现次数最多的元素


