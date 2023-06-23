# 获取资源列表
# coding=UTF-8

from com.darhan.entity import Result
from com.darhan.entity import ResultCode
from com.darhan.entity import PageResult
from com.darhan.entity import Pager
from com.darhan.utils import SQLTool
from com.darhan.utils import JwtUtil
from com.darhan.utils import RedisUtil
from java.util import ArrayList
from java.util import Arrays
from java.util import Map
from java.util import HashMap
from java.lang import Integer


def handle(input, jdbcTemplate):
    # 获取用户数据
    uid = JwtUtil.getId(req.getHeader("Authorization"))
    user = RedisUtil.hget(uid, "user")
    level = user.get("level")

    routers = jdbcTemplate.queryForList("select * from sys_router where 1=1 AND LEVEL >= ? order by createdTime;", level)
    resources = jdbcTemplate.queryForList("select id,name as title,pid,description from sys_resource where 1=1 \
    and level >= ? order by createdTime;", level)
    
    data = HashMap()
    data.put("routers", routers)
    data.put("resources", resources)
    
    return Result(ResultCode.SUCCESS, data)
