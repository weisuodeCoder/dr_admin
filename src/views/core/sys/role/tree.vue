<template>
  <Card title="组织层级" titleStyle="font-size:14px;font-weight: 500;" minHeight="0" shadow="hover">
    <template #body>
      <el-tree :data="list.val" :props="defaultProps" @node-click="handleNodeClick" default-expand-all highlight-current :expand-on-click-node="false" :empty-text="isEmpty?'暂无数据':'无资源权限'" />
    </template>
  </Card>
</template>
<script setup>
import Card from '@/components/tools/card.vue';
import { ref, reactive, defineEmits } from 'vue';
import { getChildIds } from '@/tools';
import { apiList } from '@/api/core/sys/org';

// 列表数据
const list = reactive({ val: [] });
const emit = defineEmits(['onChange']);

// tree显示数据
const defaultProps = {
  children: 'children',
  label: 'name',
  value: 'id',
};

// 点击树形控件事件
const handleNodeClick = (_data) => {
  // let ids = getChildIds(_data, 'id', 'children');
  emit('onChange', { name: _data.name, id: _data.id });
};

// 请求数据
const onRefresh = () => {
  apiList({ pageSize: 10000, search: { pid: 0 } }).then((res) => {
    list.val = arr2tree(res.data.list, 'id', 'pid', 'children');
  });
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

/**
 * @abstract: 页面资源
 */
const isEmpty = ref(false);

if (hasResource('/core/core/sys/org/list')) {
  onRefresh();
  isEmpty.value = true;
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