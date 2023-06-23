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
  data = HashMap()
  data.put("roots",jdbcTemplate.queryForList("select * from sys_system_router ", []))
  data.put("menus",jdbcTemplate.queryForList("select * from sys_menu_router ", []))
  data.put("items",jdbcTemplate.queryForList("select * from sys_menuitem_router ", []))
  return Result(ResultCode.SUCCESS, data)
