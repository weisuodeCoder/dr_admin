<template>
  <Card :title="(dict_data.val.name||'字典项列表')+(dict_data.val.type?'——'+dict_data.val.typeName:'')" titleStyle="font-size:14px;font-weight: 500;" shadow="hover" minHeight="0">
    <template #head-btn>
      <el-button size="small" type="primary" @click="onShow(0, 'create')">创建</el-button>
    </template>
    <template #body>
      <!-- 显示树形表格 -->
      <Table v-if="dict_data.val.type=='tree'" :columns="columns" :params="params" ref="table" lasy>
        <!-- <template #action="scope">
        </template> -->
      </Table>
      <!-- 显示正常表格 -->
      <Table v-else :columns="columns" :params="params" ref="table" lasy>
        <template #action="scope">
          <!-- 查看 -->
          <el-button link type="info" size="small" @click="onShow(scope.row.id, 'show')">查看</el-button>
          <!-- 编辑 -->
          <el-button link type="primary" size="small" @click="onShow(scope.row.id, 'update')">编辑</el-button>
          <!-- 删除 -->
          <el-popconfirm title="此操作将会删除包括本身在内的所有子项，是否确定删除?" confirm-button-text="是" cancel-button-text="否" confirm-button-type="danger" cancel-button-type="info" @confirm="onDelete(scope.row.id)">
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
    </template>
  </Card>
  <Info ref="show" @onChange="onRefresh"></Info>
</template>
<script setup>
import { ref, reactive, defineExpose, inject, watch } from 'vue';
import { ElMessage } from 'element-plus';
import Card from '@/components/tools/card.vue';
import Table from '@/components/tools/table.vue';
import Info from './item/info.vue';
import { apiDelete, apiDeleteAll } from '@/api/core/sso/dict-item';

const show = ref(null);
const table = ref(null);
const title = ref('字典项列表');
const dict_data = inject('dict_data');
let dict_id = 0;

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
    prop: 'label',
    label: '标签',
    width: '180',
  },
  {
    prop: 'code',
    label: '编码',
    width: '80',
  },
  {
    prop: 'description',
    label: '描述',
    width: '600',
  },
  {
    label: '操作',
    width: '145',
    fixed: 'right',
    slot: 'action',
  },
];

// 请求参数
const params = {
  url: '/core/anon/dict/item/list',
  pager: {
    pageSize: 10,
    pageNum: 1,
  },
  search: {},
};

// 刷新页面
const onRefresh = () => {
  table.value.onRefresh();
};

// 显示表单项
const onShow = (_id, _type) => {
  if (dict_id != 0 && dict_data.val.type != undefined) {
    show.value.onShow(_id, _type);
  } else {
    ElMessage.error('请选择左侧字典！');
  }
};

// 删除字典项
const onDelete = (_id) => {
  apiDelete(_id).then((res) => {
    onRefresh();
  });
};

// 删除所有
const deleteAll = () => {
  let ids = table.value.getIds();
  apiDeleteAll(ids).then((res) => {
    onRefresh();
  });
};

watch(dict_data, (val) => {
  dict_id = val.val.id;
  params.search.pid = dict_id;
  if (params.search.pid != 0 && params.search.pid != undefined) onRefresh();
});
</script>
<style lang='scss' scoped>
</style>