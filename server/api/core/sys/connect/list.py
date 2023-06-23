# 测试
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

    pager = Pager()
    pager.setPageSize(input.get("pageSize"))
    pager.setPageNum(input.get("pageNum"))

    condition = ""
    params = ArrayList()

    userId = input.get("userId")
    if (userId == None or userId == 0):
        return Result(u"请选关联用户！")
    condition += " and userId=? "
    params.add(userId)

    condition += " order by createdTime "

    sql = "select * from user_and_org where 1=1 "
    sqlEntry = SQLTool.getPageParams(sql + condition, params, pager)
    list = jdbcTemplate.queryForList(sqlEntry.getSql(), sqlEntry.getParams())

    sqlEntry = SQLTool.getTotalParams(
        "select count(1) from user_and_org where 1=1 " + condition, params)
    total = jdbcTemplate.queryForObject(sqlEntry.getSql(), Integer(0).class, sqlEntry.getParams())

    for i in range(list.size()):
        rows = jdbcTemplate.queryForList("SELECT t.roleId,t.id,r.name FROM user_org_and_role t \
        LEFT JOIN sys_role r ON r.id=t.roleId where tableId=? ;", [list.get(i).get("id")])
        list.get(i).put("rows",rows)

    return Result(ResultCode.SUCCESS, PageResult(total, list))
