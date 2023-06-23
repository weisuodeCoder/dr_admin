# 测试
# coding=UTF-8

from com.darhan.entity import Result
from com.darhan.entity import ResultCode
from com.darhan.entity import PageResult
from com.darhan.utils import SQLTool
from java.util import List
from java.util import Map
from org.springframework.dao import EmptyResultDataAccessException
from java.lang import Integer


def handle(input, jdbcTemplate):
    id = input.get("id")

    sqlEntry = SQLTool.getUpdateParams("sys_resource", input, id)
    count = jdbcTemplate.update(sqlEntry.getSql(), sqlEntry.getParams())
    return Result(count)
