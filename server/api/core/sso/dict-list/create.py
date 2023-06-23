# 测试
# coding=UTF-8

from com.darhan.entity import Result
from com.darhan.entity import ResultCode
from com.darhan.entity import PageResult
from com.darhan.utils import IdWorker
from com.darhan.utils import SQLTool
from java.util import List
from java.util import Map
from java.lang import Integer
from com.alibaba.fastjson import JSONObject
from java.lang import Math


def handle(input, jdbcTemplate):
    
    sqlEntry = SQLTool.getInsertParams("dict_list",input)
    count = jdbcTemplate.update(sqlEntry.getSql(), sqlEntry.getParams())
    return Result(count)
