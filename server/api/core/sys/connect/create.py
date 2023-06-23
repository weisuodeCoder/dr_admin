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
from java.util import HashMap


def handle(input, jdbcTemplate):

    # 判断用户是否存在
    id = input.get("userId")
    if (id == 0 or id == None):
        return Result(u"id不能为空!")

    # 判断数据是否重复
    list = jdbcTemplate.queryForList(
        "select id from user_and_org where orgId=? and userId=?", [input.get("orgId"), id])
    if (list.size() > 0):
        return Result(u"户已关联该组织，请勿重复操作!")

    rows = input.get("roleIds")
    input.remove("roleIds")

    # 关联组织
    sqlEntry = SQLTool.getInsertParams("user_and_org", input)
    count = jdbcTemplate.update(sqlEntry.getSql(), sqlEntry.getParams())

    if (count == 1):
        list = jdbcTemplate.queryForList("select id from user_and_org where \
        orgId=? and userId=? ", [input.get("orgId"), id])
        tableId = list.get(0).get("id")
        for roleId in rows:
            data = HashMap()
            data.put("roleId", roleId)
            data.put("tableId", tableId)
            sqlEntry = SQLTool.getInsertParams("user_org_and_role", data)
            jdbcTemplate.update(sqlEntry.getSql(), sqlEntry.getParams())

    return Result(ResultCode.SUCCESS)
