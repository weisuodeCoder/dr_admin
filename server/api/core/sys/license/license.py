# 资源授权
# coding=UTF-8

from com.darhan.entity import Result
from com.darhan.entity import ResultCode
from com.darhan.entity import PageResult
from com.darhan.utils import SQLTool
from com.darhan.utils import IdWorker
from java.util import List
from java.util import Map
from java.lang import Integer
from java.util import HashMap


def handle(input, jdbcTemplate):
    id = input.get("id")  # 角色id
    if (id == None or id == 0):
        return Result(u"请指定角色！")

    jdbcTemplate.update("delete from role_and_router where roleId = ? ;", id)
    jdbcTemplate.update("delete from role_and_resource where roleId = ? ;", id)

    routers = input.get("routers")
    if (routers != None and routers.size() != 0):
        for rid in routers:
            data = HashMap()
            data.put("roleId", id)
            data.put("routerId", rid)
            sqlEntry = SQLTool.getInsertParams("role_and_router", data)
            jdbcTemplate.update(sqlEntry.getSql(), sqlEntry.getParams())
            # jdbcTemplate.update("insert into role_and_router (roleId, routerId) values (?, ?);", [id, rId])

    resources = input.get("resources")
    if (resources != None and resources.size() != 0):
        for rid in resources:
            data = HashMap()
            data.put("roleId", id)
            data.put("resourceId", rid)
            sqlEntry = SQLTool.getInsertParams("role_and_resource", data)
            jdbcTemplate.update(sqlEntry.getSql(), sqlEntry.getParams())
            # jdbcTemplate.update("insert into role_and_resource (roleId, resourceId) values (?, ?);", [id, rId])

    return Result(ResultCode.SUCCESS)
