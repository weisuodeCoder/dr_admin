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

    if (input.get("getChild") != None and input.get("getChild") != 0):
        condition += " and l.id = ? "
        params.add(input.get("getChild"))
        condition += " or l.router like '%" + str(input.get("getChild")) + "%' "

    search = input.get("search")
    if (search.get("name") != None and search.get("name") != ""):
        condition += " and l.name like '%"+search.get("name")+"%' "
    condition += " order by l.sort, l.createdTime "

    sql = "SELECT l.*,t.name AS pName \
    FROM sys_org l \
    LEFT JOIN sys_org t \
    ON l.pid=t.id where 1=1 "
    sqlEntry = SQLTool.getPageParams(sql + condition, params, pager)
    list = jdbcTemplate.queryForList(sqlEntry.getSql(), sqlEntry.getParams())

    sqlEntry = SQLTool.getTotalParams(
        "select count(1) from sys_org l where 1=1 " + condition, params)
    total = jdbcTemplate.queryForObject(sqlEntry.getSql(), Integer(0).class, sqlEntry.getParams())

    return Result(ResultCode.SUCCESS, PageResult(total, list))
