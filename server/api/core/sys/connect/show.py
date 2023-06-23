# 测试
# coding=UTF-8

from com.darhan.entity import Result
from com.darhan.entity import ResultCode
from com.darhan.entity import PageResult
from java.util import List
from java.util import Map
from java.lang import Integer


def handle(input, jdbcTemplate):
    

    id = input.get("id")
    if(id==None or id==0):
        return Result(u"id为空!")
    print(id)
    data = jdbcTemplate.queryForMap("select id,orgId from user_and_org where id = ?", id)

    list = jdbcTemplate.queryForList("select id,roleId from user_org_and_role where tableId=? order by createdTime;", [id])
    data.put("roleIds", list)
    return Result(ResultCode.SUCCESS, data)
    
