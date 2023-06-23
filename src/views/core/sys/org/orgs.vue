<template>
  <Card :title="title" titleStyle="font-size:14px;font-weight: 500;" shadow="hover" minHeight="0">
    <template #body>
      <Table :columns="columns" :params="params" ref="table" lasy :tree="tree" open="true"></Table>
    </template>
  </Card>
</template>
<script setup>
import Card from '@/components/tools/card.vue';
import Table from '@/components/tools/table.vue';
import { ref, reactive, defineExpose, inject, watch } from 'vue';
import { getChildIds } from '@/tools';

const show = ref(null);
const table = ref(null);
const title = ref('组织列表');
const id = inject('_id');
const tree = reactive({});

// 显示
const onShow = (_ids, _title) => {
  title.value = '组织列表__' + _title;
  params.search.ids = _ids;
  table.value.onRefresh();
};

// 列表：表头
const columns = [
  {
    type: 'index',
    width: '45',
  },
  {
    label: '#',
    // type: 'index',
    width: '45',
  },
  {
    prop: 'sort',
    label: '排序',
    width: '100',
    sortable: true,
  },
  {
    prop: 'name',
    label: '组织名称',
    width: '180',
  },
  {
    prop: 'pName',
    label: '上级组织',
    width: '0',
  },
];

// 请求参数
const params = {
  url: '/core/core/sys/org/list',
  pager: {
    pageSize: 10000,
    pageNum: 1,
  },
  search: {},
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

defineExpose({ onShow });
</script>
<style lang='scss' scoped>
.dr-row-id {
  overflow: hidden;
  // text-overflow: ellipsis;
  white-space: nowrap;
}
</style>