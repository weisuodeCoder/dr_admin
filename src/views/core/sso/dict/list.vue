<template>
  <Card title="字典列表" titleStyle="font-size:14px;font-weight: 500;" shadow="hover" minHeight="0">
    <template #head-btn>
      <el-button size="small" type="primary" @click="onShow(0, 'create')">创建</el-button>
    </template>
    <template #body>
      <Table :columns="columns" :params="params" ref="table" lasy pageType='small'>
        <template #type="scope">
          {{getType(scope.row.type)}}
        </template>
        <template #action="scope">
          <!-- 查看 -->
          <el-button link type="info" size="small" @click="show.onShow(scope.row.id, 'show')">查看</el-button>
          <!-- 编辑 -->
          <el-button link type="primary" size="small" @click="show.onShow(scope.row.id, 'update')">编辑</el-button>
          <!-- 删除 -->
          <el-popconfirm title="此操作将会删除包括本身在内的所有子项，是否确定删除?" confirm-button-text="是" cancel-button-text="否" confirm-button-type="danger" cancel-button-type="info" @confirm="onDelete(scope.row.id)">
            <template #reference>
              <el-button link type="danger" size="small">删除</el-button>
            </template>
          </el-popconfirm>
          <!-- 添加项 -->
          <el-tooltip :content="'添加字典项到：'+scope.row.name" placement="right">
            <el-button link type="warning" size="small" @click="onAddShow(scope.row)">
              <embed :src="'/icons/add_item.svg'" type="image/svg+xml" class="dr-icon" />
            </el-button>
          </el-tooltip>
        </template>
      </Table>
    </template>
  </Card>
  <Info ref="show" @onChange="onRefresh"></Info>
</template>
<script setup>
import Card from '@/components/tools/card.vue';
import Table from '@/components/tools/table.vue';
import Info from './list/info.vue';
import { ref, inject, watch, computed } from 'vue';
import { apiDelete } from '@/api/core/sso/dict-list';

const show = ref(null);
const table = ref(null);
const dict_data = inject('dict_data');

// 列表：表头
const columns = [
  {
    prop: 'name',
    label: '名称',
    width: '100',
  },
  {
    prop: 'code',
    label: '编码',
    width: '100',
  },
  {
    prop: 'type',
    label: '类型',
    width: '100',
    slot: 'type',
  },
  {
    prop: 'description',
    label: '描述',
    width: '600',
  },
  {
    label: '操作',
    width: '185',
    fixed: 'right',
    slot: 'action',
  },
];

// 请求参数
const params = {
  url: '/core/anon/dict/list/list',
  pager: {
    pageSize: 10,
    pageNum: 1,
  },
  search: {},
};

// 显示表单项
const onShow = (_id, _type) => {
  console.log(show.value);
  show.value.onShow(_id, _type);
};

// 刷新页面
const onRefresh = () => {
  table.value.onRefresh();
};

// 获取列表type
const getType = computed(() => {
  return (_type) => {
    if (_type == 'select') {
      return '数组数据';
    } else if (_type == 'tree') {
      return '树形数据';
    } else {
      return '';
    }
  };
});

// 删除字典
const onDelete = (_id) => {
  apiDelete(_id).then((res) => {
    onRefresh();
  });
};

// 添加字典项
const onAddShow = (_data) => {
  let data = { id: _data.id, name: _data.name, type: _data.type };
  data.typeName = _data.type == 'select' ? '数组数据' : '树形数据';
  dict_data.val = data;
};

watch(
  () => table.value,
  (val) => {
    if (val != undefined) {
      onRefresh();
    }
  }
);
</script>
<style lang='scss' scoped>
.dr-icon {
  width: 22px;
  height: 22px;
  pointer-events: none;
}
</style>