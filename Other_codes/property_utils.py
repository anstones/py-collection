# coding:utf-8


def format_resident_type(num):
    """
    格式化居民类型
    :param num: 居民类型代号
    :return:
    """
    data = "未知"
    resident_type = {"1": "租客", "2": "业主", "3": "家属"}
    if str(num) in resident_type.keys():
        data = resident_type[str(num)]
    return data


def format_usage_type(num):
    """
    格式化房屋用途
    :param num: 房屋使用代号
    :return:
    """
    data = "未知"
    usage = {"1": "自住", "2": "放租", "3": "商用", "4": "空置", "5": "其他"}
    if str(num) in usage.keys():
        data = usage[str(num)]
    return data


def format_orientation_type(num):
    """
    格式化房屋朝向
    :param num: 房屋朝向代号
    :return:
    """
    data = "未知"
    orientation = {"1": "东", "2": "南", "3": "西", "4": "北", "5": "东南", "6": "西南", "7": "东北", "8": "西北"}
    if str(num) in orientation.keys():
        data = orientation[str(num)]
    return data


def format_decorate_grade_type(num):
    """
    格式化装修类型
    :param num: 装修类型代号
    :return:
    """
    data = "未知"
    decorate_grade = {"1": "毛坯", "2": "简装", "3": "精装", "4": "豪装"}
    if str(num) in decorate_grade.keys():
        data = decorate_grade[str(num)]
    return data


def format_elevator_type(num):
    """
    格式化有无电梯
    :param num: 有无电梯代号
    :return:
    """
    data = "未知"
    elevator_grade = {"1": "无", "2": "有"}
    if str(num) in elevator_grade.keys():
        data = elevator_grade[str(num)]
    return data


def format_property_right_type(num):
    """
    格式化产权性质
    :param num: 产权性质代号
    :return:
    """
    data = "未知"
    property_right = {
        "1": "商品房",
        "2": "经适房",
        "3": "央产房",
        "4": "军产房",
        "5": "公房",
        "6": "小产权房",
        "7": "自建房"
    }
    if str(num) in property_right.keys():
        data = property_right[str(num)]
    return data


def format_house_grade_type(num):
    """
    格式化产权性质
    :param num: 房屋等级代号
    :return:
    """
    data = "未知"
    house_grade = {"1": "高层", "2": "多层", "3": "联排", "4": "独栋", "5": "商业", "6": "其他"}
    if str(num) in house_grade.keys():
        data = house_grade[str(num)]
    return data


def format_certificate_type(num):
    """
    格式化业主证件类型
    :param num: 业主证件类型使用代号
    :return:
    """
    data = "未知"
    certificate = {
        "1": "居民身份证",
        "2": "香港身份证",
        "3": "澳门身份证",
        "4": "往来港澳通行证",
        "5": "台湾居民定居证",
        "6": "外国人永久居留证",
        "7": "外国人居留证",
        "8": "外国人临时居留证",
        "9": "外国人出入境证",
        "10": "外国人旅行证",
        "11": "华侨回国定居证",
        "12": "暂住证"
    }
    if str(num) in certificate.keys():
        data = certificate[str(num)]
    return data
