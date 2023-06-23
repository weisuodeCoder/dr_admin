<template>
  <Card :title="title" titleStyle="font-size:14px;font-weight: 500;" shadow="hover" minHeight="0">
    <template #body>
      <Table :columns="columns" :params="params" ref="table" lasy :tree="tree">
        <template #action="scope">
          <!-- 资源 -->
          <el-button link type="success" size="small" @click="onPeploy(scope.row)" v-if="scope.row.isRouter==1">配置资源</el-button>
        </template>
      </Table>
    </template>
  </Card>
  <Deploy ref="show"></Deploy>
</template>
<script setup>
import Card from '@/components/tools/card.vue';
import Table from '@/components/tools/table.vue';
import { ref, reactive, defineExpose, inject, watch } from 'vue';
import { getChildIds } from '@/tools';
import Deploy from './deploy/show.vue';

const show = ref(null);
const table = ref(null);
const title = ref('资源列表');
const id = inject('_id');
const tree = reactive({});

// 列表：表头
const columns = [
  {
    type: 'selection',
    width: '40',
  },
  {
    prop: 'sort',
    label: '排序',
    width: '80',
    sortable: true,
  },
  {
    prop: 'title',
    label: '名称',
    width: '180',
  },
  {
    prop: 'path',
    label: '路径',
    width: '180',
  },
  {
    prop: 'name',
    label: '标识',
    width: '180',
  },
  {
    prop: 'component',
    label: '组件',
    width: '0:180',
  },
  {
    prop: 'icon',
    label: '图标',
    width: '180',
  },
  {
    label: '操作',
    width: '85',
    fixed: 'right',
    slot: 'action',
  },
];

// 请求参数
const params = {
  url: '/core/core/sso/routers/list',
  pager: {
    pageSize: 10000,
    pageNum: 1,
  },
  search: {},
};

// 显示配置项
const onPeploy = (_data) => {
  show.value.onShow(_data.title, _data.id);
};

// 刷新页面
const onRefresh = () => {
  table.value.onRefresh();
};

watch(id, (val) => {
  tree.name = 'pid';
  tree.id = val;
  params.getChild = val;
  onRefresh();
});
</script>
<style lang='scss' scoped>
.dr-row-id {
  overflow: hidden;
  // text-overflow: ellipsis;
  white-space: nowrap;
}
</style>