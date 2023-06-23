<template>
  <Card :title="info.name==undefined?'职位列表':'职位列表__'+info.name" titleStyle="font-size:14px;font-weight: 500;" minHeight="0" shadow="hover">
    <template #head-btn>
      <el-button v-show="showC" type="primary" size="small" @click="show.onShow(0,'create')">创建</el-button>
    </template>
    <template #body>
      <Table :columns="columns" :params="params" ref="table" lasy :emptyText="emptyText">
        <template #action="scope">
          <!-- 查看 -->
          <el-button v-show="showR" link type="info" size="small" @click="show.onShow(scope.row.id, 'show')">查看</el-button>
          <!-- 授权 -->
          <el-button link type="warning" size="small" v-show="showLicense" @click="license.onShow(scope.row)">授权</el-button>
          <!-- 编辑 -->
          <el-button v-show="showU" link type="primary" size="small" @click="show.onShow(scope.row.id, 'update')">编辑</el-button>
          <!-- 删除 -->
          <el-popconfirm title="此操作将会删除包括本身在内的所有子项，是否确定删除?" confirm-button-text="是" cancel-button-text="否" confirm-button-type="danger" cancel-button-type="info" @confirm="onDelete(scope.row.id)">
            <template #reference>
              <el-button v-show="showD" link type="danger" size="small">删除</el-button>
            </template>
          </el-popconfirm>
        </template>
        <template #all>
          <el-popconfirm title="是否确定删除?" confirm-button-text="是" cancel-button-text="否" confirm-button-type="danger" cancel-button-type="info" @confirm="deleteAll">
            <template #reference>
              <el-button v-show="showDall" class="dr-button" type="danger">批量删除</el-button>
            </template>
          </el-popconfirm>
        </template>
      </Table>
    </template>
  </Card>
  <Info ref="show" @onChange='onChildChange'></Info>
  <License ref="license"></License>
</template>
<script setup>
import { ref, inject, watch } from 'vue';
import { apiDelete, apiDeleteAll } from '@/api/core/sys/role';
import Card from '@/components/tools/card.vue';
import Table from '@/components/tools/table.vue';
import Info from './info.vue';
import License from './license/show.vue';

const show = ref(null);
const table = ref(null);
const license = ref(null);
const info = inject('_data');

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
    prop: 'name',
    label: '职位',
    width: '180',
  },
  {
    prop: 'orgName',
    label: '组织',
    width: '180',
  },
  {
    label: '操作',
    width: '200',
    fixed: 'right',
    slot: 'action',
  },
];

// 请求参数
const params = {
  url: '/core/core/sys/role/list',
  pager: {
    pageSize: 10,
    pageNum: 1,
  },
  search: {},
};

// 删除
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

// 子组件触发事件
const onChildChange = () => {
  onRefresh();
};

// 刷新页面
const onRefresh = () => {
  if (params.orgId == 0 || params.orgId == undefined || params.orgId == '')
    return;
  table.value.onRefresh();
};

/**
 * @abstract: 页面资源
 */
const [showC, showR, showU, showD, showDall] = [
  ref(false),
  ref(false),
  ref(false),
  ref(false),
  ref(false),
];
const [showLicense] = [ref(false)];
const isEmpty = ref(false);
const rootPath = '/core/core/sys/role/';
const emptyText = ref('暂无数据');

verify(rootPath + 'create').then((res) => {
  showC.value = res;
});
verify(rootPath + 'show').then((res) => {
  showR.value = res;
});
verify(rootPath + 'update').then((res) => {
  showU.value = res;
});
verify(rootPath + 'delete').then((res) => {
  showD.value = res;
});
verify(rootPath + 'delete-all').then((res) => {
  showDall.value = res;
});
verify('/core/core/sys/license/license').then((res) => {
  showLicense.value = res;
});

watch(info, (val) => {
  params.orgId = val.id;
  if (hasResource(rootPath + 'list')) {
    // 判断是否拥有列表权限
    emptyText.value = '暂无数据';
    onRefresh();
    isEmpty.value = true;
  } else {
    emptyText.value = '无资源权限';
  }
});
</script>
<style lang='scss' scoped>
</style>