<template>
  <el-drawer v-model="state" size="50%" destroy-on-close :show-close="false">
    <template #header="{ titleId, titleClass }">
      <h4 :id="titleId" :class="titleClass">{{title}}</h4>
      <el-button size="small" type="primary" class="dr-add" @click="info.onShow(0,pid,'create')">添加</el-button>
    </template>
    <Table :columns="columns" :params="params" ref="table" lasy>
      <template #action="scope">
        <el-button link type="info" size="small" @click="info.onShow(scope.row.id,pid,'show')">查看</el-button>
        <el-button link type="primary" size="small" @click="info.onShow(scope.row.id,pid,'update')">编辑</el-button>
        <el-popconfirm title="是否确定删除?" confirm-button-text="是" cancel-button-text="否" confirm-button-type="danger" cancel-button-type="info" @confirm="onDelete(scope.row.id)">
          <template #reference>
            <el-button link type="danger" size="small">删除</el-button>
          </template>
        </el-popconfirm>
      </template>
      <template #all>
        <el-popconfirm title="是否确定删除?" confirm-button-text="是" cancel-button-text="否" confirm-button-type="danger" cancel-button-type="info" @confirm="deleteAll">
          <template #reference>
            <el-button class="dr-button" type="danger">批量删除</el-button>
          </template>
        </el-popconfirm>
      </template>
    </Table>
  </el-drawer>
  <Info ref="info" @onChange="onChildChange"></Info>
</template>
<script setup>
import Dialog from '@/components/tools/dialog.vue';
import Table from '@/components/tools/table.vue';
import Info from './info.vue';
import { ref, reactive, defineExpose, watch, onMounted } from 'vue';
import { apiShow, apiDelete, apiDeleteAll } from '@/api/core/sso/resource';

const show = ref(null);
const info = ref(null);
const title = ref('');
const table = ref(null);
const state = ref(false);
let pid = 0;

// 列表：表头
const columns = [
  {
    type: 'selection',
    width: '40',
  },
  {
    prop: '#',
    type: 'index',
    width: '45',
  },
  {
    prop: 'name',
    label: '资源名称',
    width: '180',
  },
  {
    prop: 'api',
    label: '资源api',
    width: '260',
  },
  {
    prop: 'type',
    label: '资源类型',
    width: '180',
  },
  {
    label: '操作',
    width: '140',
    fixed: 'right',
    slot: 'action',
  },
];

// 请求参数
const params = {
  url: '/core/core/sso/resource/list',
  pager: {
    pageSize: 10,
    pageNum: 1,
  },
  search: {},
};

// 展示
const onShow = (_name, _id) => {
  _name = _name + '__资源';
  title.value = _name;
  pid = _id;
  params.search.pid = _id;
  state.value = true;
};

// 删除
const onDelete = (id) => {
  apiDelete(id).then((res) => {
    onRefresh();
  });
};

// 子组件触发事件
const onChildChange = () => {
  onRefresh();
};

// 刷新
const onRefresh = () => {
  table.value.onRefresh();
};

// 批量删除操作
const deleteAll = () => {
  let ids = table.value.getIds();
  apiDeleteAll(ids).then((res) => {
    table.value.onRefresh();
  });
};

// 防止
watch(
  () => table.value,
  (val) => {
    if (table.value != undefined && pid != 0) {
      onRefresh();
    }
  }
);

defineExpose({ onShow });
</script>
<style lang='scss' scoped>
.dr-add {
  margin-right: 20px;
}
</style>