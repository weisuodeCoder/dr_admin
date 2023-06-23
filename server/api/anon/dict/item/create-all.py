# 测试
# coding=UTF-8

from com.darhan.entity import Result
from com.darhan.entity import ResultCode
from com.darhan.entity import PageResult
from com.darhan.utils import IdWorker
from com.darhan.utils import SQLTool
from java.util import List
from java.util import Map
from java.util import HashMap
from java.lang import Integer
from com.alibaba.fastjson import JSONObject
from java.lang import Math


def handle(input, jdbcTemplate):
    
    # 添加56个民族
    codes = [u"朝鲜族",u"满族",u"侗族",u"瑶族",u"白族",u"土家族",u"哈尼族",u"哈萨克族",u"傣族",u"黎族",u"僳僳族",u"佤族",u"畲族",u"高山族",u"拉祜族",u"水族",u"东乡族",u"纳西族",u"景颇族",u"柯尔克孜族",u"土族",u"达斡尔族",u"仫佬族",u"羌族",u"布朗族",u"撒拉族",u"毛南族",u"仡佬族",u"锡伯族",u"阿昌族",u"普米族",u"塔吉克族",u"怒族",u"乌孜别克族",u"俄罗斯族",u"鄂温克族",u"德昂族",u"保安族",u"裕固族",u"京族",u"塔塔尔族",u"独龙族",u"鄂伦春族",u"赫哲族",u"门巴族",u"珞巴族",u"基诺族"]
    count = 9
    dictId = 286001859657729
    for code in codes:
        row = HashMap()
        count += 1
        row.put('code',count)
        row.put('sort',count)
        row.put('dictId',dictId)
        row.put('label',code)
        print(row)
        sqlEntry = SQLTool.getInsertParams("dict_item",row)
        jdbcTemplate.update(sqlEntry.getSql(), sqlEntry.getParams())
    return Result(ResultCode.SUCCESS)
