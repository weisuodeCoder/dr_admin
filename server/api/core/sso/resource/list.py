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
    
    search = HashMap(input.get("search"))
    if(search.get("pid")!=None and search.get("pid")!=0):
        condition += " and pid = ? "
        params.add(search.get("pid"))
    else:
        return Result(u"请选择父节点！")
    if(search.get("name") != None and search.get("name")!=""):
        condition += " and name like '%"+search.get("name")+"%' "
    condition += " order by createdTime "
    
    
    sql = "select * from sys_resource where 1=1 "
    sqlEntry = SQLTool.getPageParams(sql + condition, params, pager)
    list = jdbcTemplate.queryForList(sqlEntry.getSql(), sqlEntry.getParams())
    
    sqlEntry = SQLTool.getTotalParams("select count(1) from sys_resource where 1=1 " + condition, params)
    total = jdbcTemplate.queryForObject(sqlEntry.getSql(), Integer(0).class,sqlEntry.getParams())
    
    
    return Result(ResultCode.SUCCESS, PageResult(total, list))
