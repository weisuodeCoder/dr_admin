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

    input.remove("password")
    input.remove("account")

    name = input.get("name")
    if(name==None or name==""):
        return Result(u"昵称不能为空!")
    rows = jdbcTemplate.queryForList("select name from sys_user where name=? and id != ? ;", name, id)
    if(rows.size()>0):
        return Result(u"该昵称已存在!")

    sqlEntry = SQLTool.getUpdateParams("sys_user", input, id)
    count = jdbcTemplate.update(sqlEntry.getSql(), sqlEntry.getParams())
    return Result(count)
