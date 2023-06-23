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
    count = jdbcTemplate.update("delete from dict_list where id=?", id)
    return Result(count)
