# 测试
# coding=UTF-8

from com.darhan.entity import Result
from com.darhan.entity import ResultCode
from com.darhan.entity import PageResult
from com.darhan.utils import SQLTool
from java.util import List
from java.util import ArrayList
from java.util import Map
from java.util import HashMap
from org.springframework.dao import EmptyResultDataAccessException
from java.lang import Integer


def handle(input, jdbcTemplate):

    tableId = input.get("tableId")
    if(tableId==None or tableId==0):
        return Result(u"id不能为空!")

    rows = input.get("roleIds")
    input.remove("roleIds")

    jdbcTemplate.update("delete from user_org_and_role where tableId=?;", tableId)

    for roleId in rows:
        data = HashMap()
        data.put("roleId", roleId)
        data.put("tableId", tableId)
        sqlEntry = SQLTool.getInsertParams("user_org_and_role", data)
        jdbcTemplate.update(sqlEntry.getSql(), sqlEntry.getParams())

    return Result(ResultCode.SUCCESS)
