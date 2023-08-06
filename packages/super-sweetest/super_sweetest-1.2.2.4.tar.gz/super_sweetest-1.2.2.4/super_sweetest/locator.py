import os
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from super_sweetest.elements import e
from super_sweetest.globals import g
from super_sweetest.log import logger
from super_sweetest.config import element_wait_timeout


def locating_element(element, action=''):
    el_location = None
    try:
        el, value = e.get(element)
    except:
        logger.exception(
            'Locating the element:%s is Failure, this element is not define' % element)
        raise Exception(
            'Locating the element:%s is Failure, this element is not define' % element)

    if not isinstance(el, dict):
        raise Exception(
            'Locating the element:%s is Failure, this element is not define' % element)

    wait = WebDriverWait(g.driver, element_wait_timeout)

    if el['by'].lower() in ('title', 'url', 'current_url'):
        return None
    else:
        try:
            el_location = wait.until(EC.presence_of_element_located(
                (getattr(By, el['by'].upper()), value)))
        except:
            sleep(5)
            try:
                el_location = wait.until(EC.presence_of_element_located(
                    (getattr(By, el['by'].upper()), value)))
            except :
                raise Exception('Locating the element:%s is Failure: Timeout' % element)
    try:
        if g.driver.name in ('chrome', 'safari'):
            g.driver.execute_script(
                "arguments[0].scrollIntoViewIfNeeded(true)", el_location)
        else:
            g.driver.execute_script(
                "arguments[0].scrollIntoView(false)", el_location)
    except:
        pass

    try:
        if action == 'CLICK':
            #增加class_name elements 通过 index定位 点击
            if  isinstance(int(el['remark']),int):
                el_location = {'elements': el['by'], 'value': value, 'index_': int(el['remark'])}  # 反回所需参数到mobile.py
            else:
                el_location = wait.until(EC.element_to_be_clickable(
                    (getattr(By, el['by'].upper()), value)))
        else:
            # elements 输入 remark 是 int 执行index取值
            if isinstance(int(el['remark']), int):
            # if 'class_name' == el['by'] and isinstance(int(el['remark']), int):
                el_location = {'elements': el['by'],'value': value,'index_': int(el['remark'])}  #反回所需参数到mobile.py
            else:
                el_location = wait.until(EC.visibility_of_element_located(
                    (getattr(By, el['by'].upper()), value)))
    except:
        pass

    return el_location


def locating_elements(elements):
    elements_location = {}
    for el in elements:
        elements_location[el] = locating_element(el)
    return elements_location


def locating_data(keys):
    data_location = {}
    for key in keys:
        data_location[key] = locating_element(key)
    return data_location


def locating_air_element(step):
    element = step['element']
    plan_name = g.plan_name
    try:
        el, value = e.get(element)
    except:
        logger.exception(
            'Locating the element:%s is Failure, this element is not define' % element)
        raise Exception(
            'Locating the element:%s is Failure, this element is not define' % element)

    if step['keyword'] in [ 'TAP', 'CHECK', 'NOTCHECK',  'WAIT_']:
        value_list = value.replace(' ', '').replace('，', ',').replace('\n','').split(',')

        # png
        png = [pho for pho in value_list if pho.endswith('.png')]
        photo = png[0] if png else value
        assert photo != '', '当前元素： %s  ,对应图片： %s 未获取到，请检查页面下包含该元素' % (element, photo)
        assert photo.endswith('.png'), '当前元素： %s  ,对应图片： %s 格式不正确，正确 png 格式：photoname.png' % (element, photo)
        photo_path = os.path.join('./data', plan_name, photo)
        assert os.path.exists(photo_path), '当前元素： %s  ,对应图片路径： %s 不存在，请检查该路径下包含该名称的图片' % (element, photo_path)

        # threshold
        thr = [thr for thr in value_list if 'threshold' in thr.lower()]
        threshold_value = thr[0].split('=')[1] if thr else 0.7

        # target_pos
        target_p = [target_p for target_p in value_list if 'target_pos' in target_p.lower()]
        target_pos_value = target_p[0].split('=')[1] if target_p else 5

        # rgb
        rg = [rg for rg in value_list if 'rgb' in rg.lower()]
        rgb_ = rg[0].split('=')[1] if rg else True
        rgb_value = False if not isinstance(rgb_, bool) and 'false' in rgb_.lower() else True

        el_location = photo_path, float(threshold_value), int(target_pos_value), rgb_value

    elif step['keyword'] in ['INPUT']:
        assert type(el) == dict, '当前元素： %s  ,对应value： %s 未获取到，请检查页面下包含该元素' % (element, value)
        el_location = el['by'], value

    elif step['keyword'] == 'SWIPE':
        # 固定坐标滑动
        # assert re.match(r"^(?:[0-9]{1,4}\,){3}[0-9]{1,4}$", value), '当前坐标：%s 格式或数量不对，正确格式如：3000,20,3000,400'% value
        # 相对坐标滑动
        num_list = value.replace('，', ',').split(',')
        # 校验长度
        assert len(num_list)  == 4 , '当前相对坐标：%s 数量不正确 或 未获取到坐标值，正确格式如：0.2131, 0.2, 2, 6' %num_list
        # 校验数值
        error_num_msg = '当前相对坐标：%s 格式不正确，正确格式如：0.2131, 0.2, 2, 6\n' \
                        'w,w,h,h\n' \
                        'width  宽  w1 w2 小数  0.0001 - 19.9999\n' \
                        'height 高  h1 h2 正数  0.0001 - 19.9999' % (value)
        for num in num_list:
            assert type(float(num)) == float and float(num) >= 0.00001 and float(
                num) <= 20, error_num_msg + '\n错误的值：%s' % num

        el_location = num_list
    elif step['keyword'] == 'TAP_POINT':
        # 相对坐标点击
        num_list = value.replace(' ', '').replace('，', ',').split(',')
        poi = [poi for poi in num_list if 'point' in poi.lower()]
        assert len(poi) == 2, '当前相对坐标：%s 数量不正确 或 未获取到坐标值，正确格式如：0.2131, 0.2' %num_list
        point1 = poi[0].split('=')[1]
        point2 = poi[1].split('=')[1]
        tim = [tap_n for tap_n in num_list if 'times' in tap_n.lower()]
        times = tim[0].split('=')[1] if tim else 1

        el_location = [float(point1), float(point2)], int(times)

    elif step['keyword'] == 'SWIPE_PHOTO':
        values = []
        value_ = value.replace('，',',').split(',')
        error_png_msg = '当前图片：%s 格式不正确，正确 图片滑动 格式：photoname.png#photoname1.png'% value
        if len(value_) != 2:
            raise error_png_msg
        for v in value_:
            assert v.endswith('.png'), error_png_msg
            photo_path = os.path.join('./data', plan_name, v)
            assert os.path.exists(photo_path), '当前元素： %s  ,对应图片路径： %s 不存在，请检查该路径下包含该名称的图片' % (element, photo_path)
            values.append(photo_path)
        el_location = values

    elif step['keyword'] in  ['CLICK', 'CHECK_TEXT', 'NOTCHECK_TEXT']:
        assert type(el) == dict, '当前元素： %s  ,对应value： %s 未获取到，请检查页面下包含该元素' % (element, value)
        el_location = el['by'], value

    elif step['keyword'] in ('BACK', 'HOME', 'MENU', 'POWER'):
        el_location = step['keyword']

    else:
        el_location = value

    return el_location