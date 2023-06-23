<template>
  <Card title="路由管理" titleStyle="font-size:14px;font-weight: 500;" minHeight="0" shadow="hover">
    <template #head-btn>
      <el-button size="small" type="primary" @click="onShow(0, 'create')">创建</el-button>
    </template>
    <template #body>
      <el-tree :data="list.val" :expand-on-click-node="false" :props="defaultProps" @node-click="handleNodeClick" :default-expand-all="status" highlight-current>
        <template #default="{ node, data }">
          <div class="dr-clearfix dr-content">
            <div class="dr-left">{{ node.label }}</div>
            <div class="dr-right">
              <el-button type="info" link size="small" @click="onShow(data.id, 'show'), getChilds(data)">查看</el-button>
              <el-button type="primary" link size="small" @click="onShow(data.id, 'update'), getChilds(data)">编辑</el-button>
              <el-popconfirm title="此操作将删除本节点以及所有子节点，是否删除?" confirm-button-text="是" cancel-button-text="否" confirm-button-type="danger" cancel-button-type="info" @confirm="onDelete(data)">
                <template #reference>
                  <el-button type="danger" link size="small">删除</el-button>
                </template>
              </el-popconfirm>
            </div>
          </div>
        </template>
      </el-tree>
    </template>
  </Card>
  <Info ref="show" @onChange="onRefresh" :data="data.val"></Info>
</template>
<script setup>
import Card from '@/components/tools/card.vue';
import { ref, reactive, defineEmits, inject } from 'vue';
import { apiList, apiDeleteAll } from '@/api/core/sso/routers';
import Info from './info.vue';

const list = reactive({ val: [] });
const show = ref(null);
const data = reactive({ val: {} });
const id = inject('_id');
const status = ref(true);

// tree显示数据
const defaultProps = {
  children: 'children',
  label: 'title',
  value: 'id',
};

const handleNodeClick = (_data) => {
  id.value = _data.id;
};

const getChilds = (_data) => {
  data.val = _data;
};

// 请求数据
const onRefresh = () => {
  apiList({ pageSize: 10000, search: { pid: 0 } }).then((res) => {
    list.val = arr2tree(res.data.list, 'id', 'pid', 'children');
  });
};
onRefresh();

// 设置ids
const setIds = (_data) => {
  let ids = [];
  ids.push(_data.id);
  if (_data.children.length > 0) {
    _data.children.forEach((el) => {
      ids.push(...setIds(el));
    });
  }
  return ids;
};

// 删除
const onDelete = (_data) => {
  let ids = setIds(_data);
  apiDeleteAll(ids).then((res) => {
    onRefresh();
  });
};

// 显示操作弹窗
const onShow = (id, type) => {
  show.value.onShow(id, type);
};

// arr2tree算法(处理的数组: arr，主键: str，父id: str，children名字: str)
function arr2tree(_data, id, parentId, childName) {
  return _data.filter((father) => {
    let newArr = _data.filter((child) => {
      return father[id] === child[parentId];
    });
    father[childName] = newArr;
    return father[parentId] == 0;
  });
}
</script>
<style lang='scss' scoped>
.dr-content {
  width: 100%;
  .dr-left {
    float: left;
  }
  .dr-right {
    float: right;
  }
}
.el-button {
  margin: 0;
}
.dr-dropdown-link {
  padding-left: 5px;
  padding-right: 5px;
  font-size: 22px;
  line-height: 7px;
  font-weight: bold;
  outline: 0;
  color: #ff9f1a;
}
.dr-dropdown-link:hover {
  outline: 0;
}
</style>