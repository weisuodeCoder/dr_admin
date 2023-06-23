# 测试
# coding=UTF-8

from com.darhan.entity import Result
from com.darhan.entity import ResultCode
from com.darhan.entity import PageResult
from com.darhan.utils import SQLTool
from java.util import List
from java.util import ArrayList
from java.util import Map
from java.lang import Integer


def handle(input, jdbcTemplate):
    id = input.get("id")
    jdbcTemplate.update("delete from user_and_org where id=?;", [id])
    count = jdbcTemplate.update("delete from user_org_and_role where tableId = ? ;", [id])
    return Result(count)
