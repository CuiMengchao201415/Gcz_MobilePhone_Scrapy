from pyecharts.charts import Line, Bar, Pie, Scatter
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from gcz_common.config import config

def analysePhonePricePieCount(data):
    """
    根据手机价格统计手机数量
    :param data:
    :return:
    """
    count = {"低端机": {"安卓": [], "苹果": [], "鸿蒙": []}, "中端机": {"安卓": [], "苹果": [], "鸿蒙": []}, "高端机": {"安卓": [], "苹果": [], "鸿蒙": []}, "全部价位": {"安卓": [], "苹果": [], "鸿蒙": []}}
    for item in data:
        try:
            price = float(item['price'])
            brond = item['brond']
            title = item['goods_title']
        except Exception as e:
            print(e)
            continue
        try:
            if price < 1500:
                if ("苹果" in brond) or ("Apple" in brond) or ("apple" in brond):
                    count['低端机']['苹果'].append(title)
                elif ("华为" in brond) or ("HUAWEI" in brond) or ("huawei" in brond):
                    count['低端机']['鸿蒙'].append(title)
                else:
                    count['低端机']['安卓'].append(title)
            elif price < 3000:
                if ("苹果" in brond) or ("Apple" in brond) or ("apple" in brond):
                    count['中端机']['苹果'].append(title)
                elif ("华为" in brond) or ("HUAWEI" in brond) or ("huawei" in brond):
                    count['中端机']['鸿蒙'].append(title)
                else:
                    count['中端机']['安卓'].append(title)
            else:
                if ("苹果" in brond) or ("Apple" in brond) or ("apple" in brond):
                    count['高端机']['苹果'].append(title)
                elif ("华为" in brond) or ("HUAWEI" in brond) or ("huawei" in brond):
                    count['高端机']['鸿蒙'].append(title)
                else:
                    count['高端机']['安卓'].append(title)
            if ("苹果" in brond) or ("Apple" in brond) or ("apple" in brond):
                count['全部价位']['苹果'].append(title)
            elif ("华为" in brond) or ("HUAWEI" in brond) or ("huawei" in brond):
                count['全部价位']['鸿蒙'].append(title)
            else:
                count['全部价位']['安卓'].append(title)
        except Exception as e:
            print(e)
    return count

def analysePhonePieCount(data, param):
    """
    根据商品某一属性统计商品数量
    :param data:
    :param param:
    :return:
    """
    count = {}
    for item in data:
        try:
            temp = item[param]
        except Exception as e:
            continue
        if temp in count:
            count[temp] += 1
        else:
            count[temp] = 1
    return count


def dictCountAdd1(data, key1, key2, value1):
    if key1 not in data.keys():
        data[key1] = value1.copy()
    if key2 in data[key1]:
        data[key1][key2] += 1
    else:
        data[key1][key2] = 1

def dictAdd(data, key, value):
    if key not in data.keys():
        data[key] = [value]
    else:
        data[key].append(value)


def analysePhonePriceCount(data, param):
    """
    根据商品价格和商标统计数量
    :param data:
    :param param:
    :return:
    """
    priceDict = {}
    priceList = []
    defaultPriceCount = {"低端机": 0, "中端机": 0, "高端机": 0}
    brondCount = {}

    for item in data:
        try:
            price = float(item['price'])
            brond = item[param]
            if (brond=="无" or brond=="未上市"): continue
        except Exception as e:
            continue

        if price < 1500:
            key = '低端机'
            dictCountAdd1(brondCount, brond, key, defaultPriceCount)
        elif price < 3000:
            key = '中端机'
            dictCountAdd1(brondCount, brond, key, defaultPriceCount)
        else:
            key = '高端机'
            dictCountAdd1(brondCount, brond, key, defaultPriceCount)

        dictAdd(priceDict, brond, price)
        brond = brond.replace("GB", "").replace("及以下", "").replace("及以上", "")
        if brond.isdigit():
            brond = int(brond)
            priceList.append([price, brond])
    return priceList, brondCount

def analysePhoneCount(data, params=['brond', 'play_memory']):
    """
    根据商品任意两个属性统计商品数量
    :param data:
    :param params:
    :return:
    """
    count = {}
    defaultCount = {}
    if params[0] == 'brond': defaultCount = {'Apple': 0, '华为（HUAWEI）': 0, '小米（MI）': 0, '荣耀（HONOR）': 0, 'vivo': 0, 'OPPO': 0, '杂牌': 0}
    if params[0] == 'play_memory': defaultCount = {'未公布': 0, '4GB及以下': 0, '6GB': 0, '8GB': 0, '12GB': 0, '16GB': 0, '无': 0}
    if params[0] == 'goods_memory': defaultCount = {'64GB及以下': 0, '128GB': 0, '256GB': 0, '512GB': 0, '1TB': 0, '无': 0}
    for item in data:
        try:
            param1 = item[params[0]]
            param2 = item[params[1]]
            if params[0] == 'brond':
                if param1 not in ["Apple", "华为（HUAWEI）", "小米（MI）", "荣耀（HONOR）", "vivo", "OPPO"]:
                    param1 = "杂牌"
            if params[1] == 'brond':
                if param2 not in ["Apple", "华为（HUAWEI）", "小米（MI）", "荣耀（HONOR）", "vivo", "OPPO"]:
                    param2 = "杂牌"
        except Exception as e:
            continue

        if param2 not in count:
            count[param2] = defaultCount.copy()
        if param1 in count[param2]:
            count[param2][param1] += 1
        else:
            count[param2][param1] = 1

    return count

def pie_set_colors(data, id=""):
    """
    生成饼状图
    :param data:
    :return:
    """
    if type(data) == dict:
        data = [("苹果", len(data['苹果'])),("鸿蒙", len(data['鸿蒙'])), ("安卓", len(data['安卓']))]
    pie = (
        Pie()
        .add("", data)
        # .set_colors(["blue", "green", "yellow", "red", "pink","orange"])
        # .set_colors(["blue", "green", "yellow"])
        .set_global_opts(title_opts=opts.TitleOpts(title="饼图"+id))
    )
    pie.render(config.file.echartPath + config.file.pieFileName + id + ".html")

def bar_base_dict_config(data):
    """
    生成柱状图
    :param data:
    :return:
    """
    if type(data) == dict:
        xaxis = list(data[list(data.keys())[0]].keys())
        yaxis = []
        for key in data.keys():
            yaxis.append({"key": key, "values": list(data[key].values())})
    else:
        xaxis = data['xaxis']
        yaxis = data['yaxis']
    bar = Bar({"theme": ThemeType.MACARONS})
    bar.add_xaxis(xaxis)
    for item in yaxis:
        bar.add_yaxis(item["key"], item["values"])
    bar.set_global_opts(title_opts=opts.TitleOpts(title="柱状图"))
    bar.render(config.file.echartPath+config.file.barFileName+".html")

def line_base(data):
    """
    生成折线图
    :param data:
    :return:
    """
    if type(data) == dict:
        xaxis = list(data[list(data.keys())[0]].keys())
        yaxis = []
        for key in data.keys():
            yaxis.append({"key": key, "values": list(data[key].values())})
    else:
        xaxis = data['xaxis']
        yaxis = data['yaxis']

    line = Line()
    line.add_xaxis(xaxis)
    for item in yaxis:
        line.add_yaxis(item["key"], item["values"])
    line.set_global_opts(title_opts=opts.TitleOpts(title="折线图"))

    line.render(config.file.echartPath+config.file.lineFileName+".html")

def scatter(data):
    """
    生成散点图
    :param data:
    :return:
    """
    if type(data) == dict:
        xaxis = list(data.keys())
        yaxis = []
        for key in data.keys():
            yaxis.append({"key": key, "values": list(data[key].values())})
    else:
        xaxis = data['xaxis']
        yaxis = data['yaxis']

    scatter = Scatter()
    scatter.add_xaxis(xaxis)
    for item in yaxis:
        scatter.add_yaxis(item["key"], item["values"])
    scatter.set_global_opts(title_opts=opts.TitleOpts(title="散点图"))
    scatter.render(config.file.echartPath+config.file.lineFileName+".html")


def scatter1(data, statue):
    if (statue<=2):
        data.sort(key=lambda x: x[0])
        x_data = [d[0] for d in data]
        y_data = [d[1] for d in data]
        x = "元"
        y = "GB"
    else:
        data.sort(key=lambda x: x[1])
        x_data = [d[1] for d in data]
        y_data = [d[0] for d in data]
        y = "元"
        x = "GB"
    (
        Scatter()
        .add_xaxis(
            xaxis_data=x_data)
        .add_yaxis(
            series_name="",
            y_axis=y_data,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_series_opts()
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                name=x, type_="value", splitline_opts=opts.SplitLineOpts(is_show=True)
            ),
            yaxis_opts=opts.AxisOpts(
                name=y,
                type_="value",
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            title_opts=opts.TitleOpts(title="散点图")
        )
        .render(config.file.echartPath+config.file.lineFileName+".html")
    )