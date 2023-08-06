# coding=utf-8

# @Time: 2020/3/11 11:05
# @Auther: liyubin

import re
import datetime
from airtest.core.api import *
from airtest.core.api import swipe as swipe_air # 为统一config关键字，与swipe函数冲突
from super_sweetest.globals import g
from super_sweetest.log import logger
from super_sweetest.locator import locating_air_element
from super_sweetest.config import element_wait_timeout
from super_sweetest.config import rgb_flag
from super_sweetest.servers.ai_server import recognition_ui
from super_sweetest.servers.ai_server import get_words
from super_sweetest.servers.ai_server import is_in_copywriting
from super_sweetest.servers.ai_server import replace_punctuate
from super_sweetest.servers.ai_server import is_language
from super_sweetest.servers.ai_server import recognition_text
from super_sweetest.servers.ai_server import get_ui_results
from super_sweetest.snapshot import get_air_screenshot
from super_sweetest.servers.common import write_data, read_data


from pathlib import Path
path = Path('lib')
if path.is_dir():
    from lib import *
else:
    from super_sweetest.lib import *


def get_width_height():
    width, height = g.poco.get_screen_size()
    return width, height


def swipe(step):
    """
    1、通过传入的固定坐标滑动

    2、获取设备分辨率计算合适的坐标
    :param poco: 对象
    :param num_list: (0.2, 0.2, 2, 6)
    :return:
    width 宽 w1 w2 小数   0.1-0.9
    height 高  h1 h2 正数 1-9
    """
    num_list = locating_air_element(step)
    duration = step['data'].get('持续时间', 1)


    # 固定坐标滑动
    # start_x = int(num_list[0])
    # start_y = int(num_list[1])
    #
    # end_x = int(num_list[2])
    # end_y = int(num_list[3])
    # if duration:
    #     swipe_air((start_x, start_y), (end_x, end_y), float(duration))
    # else:
    #     swipe_air((start_x, start_y), (end_x, end_y))

    # 相对坐标滑动
    w1 = float(num_list[0])
    w2 = float(num_list[1])
    h1 = float(num_list[2])
    h2 = float(num_list[3])
    width, height = get_width_height()
    start_pt = (float(width * w1), float(height // h1))
    end_pt = (float(width * w2), float(height // h2))

    if duration:
        swipe_air(start_pt, end_pt, float(duration))
    else:
        swipe_air(start_pt, end_pt)
    sleep(1)


def swipe_photo(step):
    value = locating_air_element(step)
    v1 = value[0]
    v2 = value[1]
    swipe_air(Template(filename=v1, rgb=rgb_flag), Template(filename=v2, rgb=rgb_flag))


def tap(step):
    duration = step['data'].get('持续时间', 0.01)
    photo_path, threshold_value, target_pos_value, rgb_value = locating_air_element(step)
    if duration:
        touch(Template(filename=photo_path, threshold=threshold_value, target_pos=target_pos_value, rgb=rgb_value), duration=float(duration))
    else:
        touch(Template(filename=photo_path, threshold=threshold_value, target_pos=target_pos_value, rgb=rgb_value))


def tap_point(step):
    """
    相对坐标点击 TAP_POINT
    point :相对坐标点
    times :点击次数
    :param step:
    :return:
    """
    point, times = locating_air_element(step)
    point1 = point[0]
    point2 = point[1]
    width, height = get_width_height()
    touch([point1*width, point2*height], times=times)


def input(step):
    by, value = locating_air_element(step)
    data = step['data']
    for key in data:
        if by.lower() == 'text':
            if g.platform.lower() == 'air_android':
                g.poco(text=value).set_text(data[key])
            else:
                # ios poco(value).set_text(value)
                g.poco(value).set_text(data[key])
        elif by.lower() == 'textmatches':
            g.poco(textMatches=value).set_text(data[key])
        else:
            if key.startswith('text'):
                text(data['text'], False)
            else:
                text(data[key], False)


def click(step):
    by, value = locating_air_element(step)
    if by.lower() == 'text':
        try:
            if g.platform.lower() == 'air_android':
                g.poco(text=value).click()
            else:
                # ios
                g.poco(value).click()
        except Exception as e:
            sleep(1)
            if g.platform.lower() == 'air_android':
                g.poco(text=value).click()
            else:
                # ios
                g.poco(value).click()
            logger.info('retry poco click, element: %s error msg: %s' % (value, e))
    elif by.lower() == 'textmatches':
        g.poco(textMatches=value).click()
    else:
        assert False, '请指定 element 中 value值：%s 对应的 by 类型为： text'% value


def check(step):
    photo_path, threshold_value, target_pos_value, rgb_value = locating_air_element(step)
    assert exists(Template(filename=photo_path, threshold=threshold_value, target_pos=target_pos_value, rgb=rgb_value))


def notcheck(step):
    photo_path, threshold_value, target_pos_value, rgb_value = locating_air_element(step)
    assert_not_exists(Template(filename=photo_path, threshold=threshold_value, target_pos=target_pos_value, rgb=rgb_value))


def check_text(step):
    by, value = locating_air_element(step)
    if by.lower() == 'text':
        if g.platform.lower() == 'air_android':
            assert g.poco(text=value).exists(), '检查文本 %s 失败'%value
        else:
            # ios
            assert g.poco(value).exists(), '检查文本 %s 失败' % value
    elif by.lower() == 'textmatches':
        assert g.poco(textMatches=value).exists(), '模糊检查文本 %s 失败' % value


def notcheck_text(step):
    by, value = locating_air_element(step)
    if by.lower() == 'text':
        if g.platform.lower() == 'air_android':
            if g.poco(text=value).exists(): raise '反向检查文本 %s 失败'%value
        else:
            # ios
            if g.poco(value).exists(): raise '反向检查文本 %s 失败' % value
    elif by.lower() == 'textmatches':
        if g.poco(textMatches=value).exists(): raise  '模糊反向检查文本 %s 失败' % value


def wait_(step):
    photo_path, threshold_value, target_pos_value, rgb_value = locating_air_element(step)
    wait(Template(filename=photo_path, threshold=threshold_value, target_pos=target_pos_value, rgb=rgb_value), timeout=element_wait_timeout)


def back(step):
    keycode = locating_air_element(step)
    keyevent(keycode)


def home(step):
    keycode = locating_air_element(step)
    keyevent(keycode)


def menu(step):
    keycode = locating_air_element(step)
    keyevent(keycode)


def power(step):
    keycode = locating_air_element(step)
    keyevent(keycode)


def delete():
    # 删除输入框内容
    for i in range(30):
        keyevent('KEYCODE_DEL')


def wake_(step):
    """唤醒手机"""
    wake()


############################AI识别#############################

def write_error_step_text(file_name, time_ms, language, error_word):
    """
    识别错误的文本写到对应步骤的文件 snapshot/planename/AI_zh_error/step_file_time.txt
    :param file:
    :return:
    """
    if len(error_word) > 0:
        text_error_path = os.path.join('snapshot', g.plan_name, 'AI_CopyWrite_' + language + '_Error')
        text_error_path if os.path.exists(text_error_path) else os.mkdir(text_error_path)
        step_file = os.path.join(text_error_path, file_name + '_' + time_ms + '_error_.txt')
        logger.info('验证错误的文本信息已保存在路径： {}'.format(step_file))
        write_data(step_file, str(error_word), mode='w+')


def update_copyword(file_name, new_words, step_copywrite_num):
    """
    读取旧的文本-去重-写入新的文本
    :param file_name: 文件名称.json
    :param new_words: 文本内容 list []
    :param step_copywrite_num: 对应步骤的当前学习次数
    :return:
    """
    read_data_ = read_data(file_name=file_name, flag='eval')
    learn_num_ = re.findall(r'学习次(.*?).txt', file_name)[0]
    learn_file = file_name.replace(learn_num_, '数_{}_'.format(step_copywrite_num+1)) # 本地文件学习次数+1
    write_data(file_name=learn_file, data_=str(list(set(new_words + read_data_))), mode='w+')
    logger.info('本地对应文案,学习更新后路径： {}'.format(learn_file))
    os.remove(file_name)


def valid_lds_ui(language, file, image_path, step_file, time_ms):
    """
     UI识别
    :param file:
    :param image_path:
    :param step_file:
    :param time_ms:
    :return:
    """
    response_lds_ui = recognition_ui(file)
    get_lds_ui_response = get_ui_results(response_lds_ui)  # 最后先判断UI异常，再判断文本异常
    logger.info('UI识别结果： {} , 提示信息： 当 error 或 score 低于80分时此图很可能显示异常'.format(response_lds_ui))

    # 通过识别后correct / error / default 目录分类保存
    max_name = get_lds_ui_response.get('result')  # 最大值对应的name
    max_score = get_lds_ui_response.get('score')  # 最大值
    max_name_file = os.path.join(image_path, max_name + '_' + language)
    max_name_file if os.path.exists(max_name_file) else os.mkdir(max_name_file)
    lds_ui_name_file = os.path.join(max_name_file, step_file + time_ms + '_' + language + '_' + '.png')  # 按识别分数分类保存
    from PIL import Image
    img = Image.open(file)
    img.save(lds_ui_name_file)
    # 提示信息：出现在日志和报告异常中
    screen_file_for_maxname = 'UI识别后图片以最大分数: {0} 分类保存在：{1}'.format(max_name, lds_ui_name_file)
    logger.info(screen_file_for_maxname)
    return max_name, max_score, screen_file_for_maxname


def valid_copywrite(language, file, step_file, step_score, step):
    """
    通过学习次数更新或检查文本内容
    :param file:
    :param step_file:
    :param step_score:
    :return:
    """


    words = recognition_text(file, language)
    words = get_words(words)
    logger.info('识别后文本： {}'.format(words))
    new_words = replace_punctuate(words, baidu_aip=True)  # 忽略百度AIP识别后异常符号

    score_split = step_score.split('学习=')
    learn_num_n = int(score_split[1]) if '文本学习=' in step_score and len(score_split) > 1 else 1  # excel 中 步骤结果：学习次数

    # 精确到步骤的文案 路径 按语言类型分类
    copywrite_file = os.path.join('snapshot', g.plan_name, 'AI_CopyWrite' + language) # 不能按时间保存，否在不能对比
    copywrite_file if os.path.exists(copywrite_file) else os.mkdir(copywrite_file)

    # 遍历本地可能存在的文件名， 文件中最大次数不大于 learn_num_n 值
    now_len_num = '1'  # 本地记录的学习次数
    step_language_path = step_file + '_' + language + '_识别文本记录_学习次数_'
    for learn_num in range(learn_num_n):
        # 先看是否有最大学习次数
        if os.path.exists(os.path.join(copywrite_file, step_language_path + str(learn_num_n) + '_.txt')):
            now_len_num = str(learn_num_n)
            logger.info('文本学习次数已达到： {}'.format(learn_num_n))
            break
        # 小于最大学习次数的文件，从大到小排除
        elif os.path.exists(os.path.join(copywrite_file, step_language_path + str(learn_num_n - learn_num+1) + '_.txt')):
            now_len_num = str(learn_num_n - learn_num+1)
            logger.info('继续进行文本学习： {}'.format(learn_num_n - learn_num+1))
            break
        # 都不符合默认 学习次数1 的路径
        else:
            now_len_num = str(1)
    step_copywrite_file = os.path.join(copywrite_file, step_language_path + now_len_num + '_.txt') # 本地当前存在文件
    # 定义学习次数逻辑
    step_copywrite_num = int(re.findall(r'次数_(.*?)_.txt', step_copywrite_file)[0])  # 文件名中的学习次数

    flag_list = []
    result_list = []
    error_words = []  # 文案识别后错误文本，最后写入错误识别记录
    return_copywrite_data = []
    # 1、当step_copywrite 不存在，按照learn_num_1=1的数值写入
    if not os.path.exists(step_copywrite_file):
        logger.info('本地不存在对应步骤的文案，正在写入...')
        logger.info('文案保存路径：{}'.format(step_copywrite_file))
        write_data(file_name=step_copywrite_file, data_=str(new_words), mode='w+')
    # 2、当文件中数值step_copywrite_num < 定义的学习次数learn_num_n, 本地存在 step_copywrite ，读写后更新内容
    elif step_copywrite_num < learn_num_n and os.path.exists(step_copywrite_file):
        logger.info('对应步骤的文本学习次数还未达到：开始更新...')
        update_copyword(step_copywrite_file, new_words, step_copywrite_num)
    # 3、如果文件中数值step_copywrite_num = 定义的学习次数learn_num_n， 而且本地存在 step_copywrite ， 则满足文本检查的条件， 不再继续写入
    elif step_copywrite_num == learn_num_n:
        logger.info('以首次保存在本地的对应步骤的文案内容 作为 预期结果，检查本次识别是否在 预期结果 中...')
        # 通过文案语言类型对文本识别
        copywrite_data = read_data(step_copywrite_file, flag='eval', mode='r')
        logger.info('文案内容的路径： {}'.format(step_copywrite_file))
        logger.info('文案内容： {}'.format(copywrite_data))

        # 忽略的部分文本
        filter_str = step.get('expected', '').get('#filter', '@#$%')
        filter_str_list = filter_str.split('&') # 包含多个&分隔的过滤词语时
        for word in new_words:
            filter_in_word = [True for filter_s in filter_str_list if filter_s in word] # 防止双重循环，判断忽略词是否在word中
            filter_flag = True if len(filter_in_word) == 0 else False # 如果列表长度=0说明，不忽略
            if filter_flag: # 如果忽略字符不在当前识别word，开始检查
                # 识别后词语的文案检查
                flag = is_in_copywriting(word, copywrite_data)
                result = '识别结果： {0},  文本： {1} '.format(flag, word)
            else:  # 忽略检查filter_str的word文本
                flag = True
                result = '忽略文本： {0}， 识别的文本： {1}'.format(filter_str, word)
            logger.info(result)
            flag_list.append(flag)
            result_list.append(result)
            error_words.append(word) if not flag else ''

        return_copywrite_data = copywrite_data
    return flag_list, result_list, error_words, new_words, return_copywrite_data  # 逻辑判断后记得最后必须返回否则接收不到参数报错


def ai_(step, testcase):
    """
    AI智能识别
    :param step:
    :param testcase:
    :return:
    """
    # 自动化步骤中是否需要跳过
    step_score = step.get('score', 'no step_score') # 包含 #AI识别 / 文本学习=3
    if '#AI识别' in step_score:
        logger.info('########## 已跳过AI识别... ##########\n')
        return True
    logger.info('--------------------------- AI识别开始... ---------------------------\n')

    # 通过图像中文本识别出语言,   用'AUTO_DETECT': '自动检测语言 识别中英文效果好
    language_type = {
        'CHN_ENG': '中英文混合', 'ENG': '英文', 'JAP': '日语', 'KOR': '韩语', 'FRE': '法语', 'SPA': '西班牙语', 'POR': '葡萄牙语',
        'GER': '德语', 'ITA': '意大利语', 'RUS': '俄语', 'DAN': '丹麦语', 'DUT': '荷兰语', 'MAL': '马来语', 'SWE': '瑞典语', 'IND': '印尼语', 'POL': '波兰语',
        'ROM': '罗马尼亚语', 'TUR': '土耳其语', 'GRE': '希腊语', 'HUN': '匈牙利语'
    }
    PLAN_NAME_LANGUAGE = '文本识别需要在 testcase、element、data 的文件名称中配置语言类型，如：test01登录用例#CHN_ENG-TextCase.xlsx \n支持的语言类型：{}'.format(language_type)

    assert '#' in g.plan_name, PLAN_NAME_LANGUAGE
    language = g.plan_name.split('#')[1]  # 默认未设置时，自动识别语言，但是会大大降低识别准确性

    assert language.upper() in language_type.keys(), PLAN_NAME_LANGUAGE
    logger.info('设定的语言: {0} - {1}'.format(language, language_type.get(language.upper())))


    # 路径生成
    plan_name = g.plan_name                              # 项目名称
    sheet_name = g.sheet_name                            # sheet名称
    case_id = testcase.get('id', 'no case_id')           # 用例编号
    case_title = testcase.get('title', 'no case_title')  # 用例标题
    step_num = re.findall(r'^\d*', step.get('no', 'no step_num').replace('>','').replace('^','').replace('<',''))[0]  # 当前用例标题的步骤数,正则匹配数字

    # 精确到步骤的图片路径
    step_file = plan_name + '_' + sheet_name + '_' + case_id + '_' + case_title + '_' + step_num + '_'
    today = datetime.datetime.now().strftime('%Y%m%d_')
    image_path_day = os.path.join('snapshot', g.plan_name, 'AI_UI_' + today + '_' + language) # 每天
    image_path_day if os.path.exists(image_path_day) else os.mkdir(image_path_day)
    time_ms = datetime.datetime.now().strftime('%Y%m%d_%H%M_%S%f')  # 含微秒的日期时间
    file = os.path.join(image_path_day, step_file + time_ms + '_' + language + '.png')
    logger.info('截图保存方式： 项目名称_sheet名称_用例编号_用例标题_步骤数字_日期时间.png')
    logger.info('截图所在位置： {}'.format(file))

    # 图片截取
    get_air_screenshot(file)

    logger.info('--------------------------- UI识别... ---------------------------\n')
    max_name, max_score, screen_file_for_maxname = valid_lds_ui(language, file, image_path_day, step_file, time_ms)

    logger.info('--------------------------- 文本识别... ---------------------------\n')
    flag_list, result_list, error_words, new_words, return_copywrite_data = valid_copywrite(language, file, step_file, step_score, step)  # 文件夹不能以每日保存，不然无法比对

    # 文案识别错误的文本单独记录
    write_error_step_text(step_file, time_ms, language, error_words)

    output_text = {'text': new_words if new_words else '识别到的内容为空'}
    if output_text:
        logger.info('output_text: %s' % repr(output_text))
        my_func = step.get('output', '').get('func', None)   # 获取输出数据中自定义函数
        if my_func:
            logger.info('开始执行自定义函数... 识别后的文本信息在自定义函数中通过key值text提取')
            eval(str('{0}({1})'.format(my_func.replace('(', '').replace(')', ''), output_text)), globals(), locals()) # 输出数据中调用自定义函数,去除（）

    # 图片识别结束抛出异常，报告中展示
    result_list.append(screen_file_for_maxname)

    # 检查UI识别 与 文本识别结果，抛出异常
    ui_flag = max_name == 'correct' and float(max_score) > 80 # 最大值name是correct是True, 分数阈值 80
    text_flag = False not in flag_list
    assert (ui_flag and text_flag), ('\nUI识别结果：{0}  \n文本识别结果：{1}  \n本次识别到的文本：{2}  \n本地文案预期内容：{3}'.format(str({'result': max_name, 'score': max_score}), result_list, new_words, return_copywrite_data))  # 文本识别结果检查



