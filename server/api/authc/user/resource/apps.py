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

    routers = []
    resources = []
    if(level==1): # 超级管理员，系统维护人员专用
        routers = jdbcTemplate.queryForList("select * from sys_router where 1=1 order by sort;")
        resources = jdbcTemplate.queryForList("select id,name as title,pid,api from sys_resource where 1=1 \
        order by createdTime;")
    elif(level==2): # 管理员，运维人员专用
        routers = jdbcTemplate.queryForList("select * from sys_router where 1=1 AND LEVEL >= ? order by sort;", level)
        resources = jdbcTemplate.queryForList("select id,name as title,pid,api from sys_resource where 1=1 \
        and level >= ? order by createdTime;", level)
    elif(level==3):
        sql = "SELECT roleId FROM user_org_and_role WHERE tableId IN ( \
        SELECT id FROM user_and_org WHERE userId IN ( \
        SELECT id FROM sys_user WHERE id=?))"
        rids = jdbcTemplate.queryForList(sql, user.get("id"))
        if(rids.size()==0):
            return Result(ResultCode.UNDISTRIBUTED_ERROR)
        iterator = rids.iterator()
        idsStr = ""
        while (iterator.hasNext()):
            idsStr += str(iterator.next().get("roleId")) + ","
        idsStr = idsStr[0:-1]
        routers = jdbcTemplate.queryForList("select * from sys_router where 1=1 \
        AND LEVEL >= ? AND id IN ( \
        select routerId from role_and_router where roleId in ("+idsStr+")\
        ) AND level == 4 order by sort;", level)
        resources = jdbcTemplate.queryForList("select id,name as title,pid, api \
        from sys_resource where 1=1 \
        and level >= ? AND id IN ( \
        select resourceId from role_and_resource where roleId in ("+idsStr+") \
        ) order by createdTime;", level)
    
    data = HashMap()
    data.put("routers", routers)
    data.put("resources", resources)
    data.put("user", jdbcTemplate.queryForMap("select account,name,level,isUsing from sys_user where id = ?", uid))
    return Result(ResultCode.SUCCESS, data)
