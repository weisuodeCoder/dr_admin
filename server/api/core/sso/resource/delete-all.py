# 测试
# coding=UTF-8

from com.darhan.entity import Result
from com.darhan.entity import ResultCode
from com.darhan.entity import PageResult
from com.darhan.utils import SQLTool
from java.util import List
from java.util import ArrayList
from java.util import Map
from java.lang import Integer


def handle(input, jdbcTemplate):
    count = jdbcTemplate.update("delete from sys_resource where id in ("+SQLTool.arr2str(input.get("ids"))+");")
    return Result(count)
