# 获取角色绑定资源
# coding=UTF-8

from com.darhan.entity import Result
from com.darhan.entity import ResultCode
from com.darhan.entity import PageResult
from com.darhan.entity import Pager
from com.darhan.utils import SQLTool
from java.util import ArrayList
from java.util import Arrays
from java.util import Map
from java.util import HashMap
from java.lang import Integer


def handle(input, jdbcTemplate):

    id = input.get("id")
    if(id==None or id==0):
        return Result(u"id不能为空!")
    # routerIds = jdbcTemplate.queryForList("select routerId as id from role_and_router where roleId=? ;", [id])
    ids = jdbcTemplate.queryForList("select resourceId as id from role_and_resource where roleId=? ;", [id])

    data = HashMap()
    data.put("ids", ids)
    
    return Result(ResultCode.SUCCESS, data)
