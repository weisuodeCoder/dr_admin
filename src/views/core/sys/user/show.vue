<template>
  <el-drawer v-model="state" size="50%" destroy-on-close :show-close="false">
    <template #header="{ titleId, titleClass }">
      <h4 :id="titleId" :class="titleClass">{{title}} - 关联组织职位</h4>
      <el-button v-show="showC&&showOR" size="small" type="primary" class="dr-add" @click="show.onShow(0,title,pid,'create')">添加</el-button>
    </template>
    <Table :columns="columns" :params="params" ref="table" lasy>
      <template #expand="scope">
        <p style="padding-left:5px;">
          <el-tag v-for="(tag, x) in scope.row.rows" :key="tag.id" :closable="showD" @close="onDelete(tag.id)" :type="getType(x)" effect="plain" style="margin-left:10px;margin-bottom:10px">
            {{ tag.name }}
          </el-tag>
        </p>
      </template>
      <template #action="scope">
        <!-- 查看 -->
        <el-button v-show="showR&&showOR" link type="info" size="small" @click="show.onShow(scope.row.id,title,pid,'show')">查看</el-button>
        <!-- 编辑 -->
        <el-button v-show="showU&&showOR" link type="primary" size="small" @click="show.onShow(scope.row.id,title,pid,'update')">编辑
        </el-button>
        <!-- 删除 -->
        <el-popconfirm title="此操作将会删除组织及职务，是否删除?" @confirm="deleteAll(scope.row.id)" confirm-button-text="是" cancel-button-text="否" confirm-button-type="danger" cancel-button-type="info">
          <template #reference>
            <el-button v-show="showDall" link type="danger" size="small">删除</el-button>
          </template>
        </el-popconfirm>
      </template>
    </Table>
  </el-drawer>
  <Connect ref="show" @onChange="onChildChange"></Connect>
</template>
<script setup>
import Connect from './connect.vue';
import {
  ref,
  reactive,
  defineExpose,
  watch,
  onMounted,
  watchEffect,
  computed,
} from 'vue';
import { apiList, apiDelete, apiDeleteAll } from '@/api/core/sys/connect';
import Dialog from '@/components/tools/dialog.vue';
import Table from '@/components/tools/table.vue';

const show = ref(null);
const title = ref('');
const state = ref(false);
const list = reactive({ val: [] });
const table = ref(null);
let pid = 0;

// tag颜色
const types = ['', 'success', 'info', 'danger', 'warning'];

const getType = computed(() => {
  return (_index) => {
    _index = _index % types.length;
    return types[_index];
  };
});

// 列表：表头
const columns = [
  {
    type: 'expand',
    slot: 'expand',
  },
  {
    prop: 'orgName',
    label: '组织',
    width: '500',
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
  url: '/core/core/sys/connect/list',
  pager: {
    pageSize: 10,
    pageNum: 1,
  },
  search: {},
};

// 展示
const onShow = (_name, _account, _id) => {
  _name = '【' + _name + '】-【' + _account + '】';
  title.value = _name;
  pid = _id;
  state.value = true;
  params.userId = _id;
};

// 删除
const onDelete = (_id) => {
  apiDelete(_id).then((res) => {
    onRefresh();
  });
};

// 批量删除操作
const deleteAll = (_id) => {
  apiDeleteAll(_id).then((res) => {
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

watchEffect(() => {
  if (table.value != undefined) {
    onRefresh();
  }
});

defineExpose({ onShow });

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
const showOR = ref(false); // orgs and roles
const rootPath = '/core/core/sys/connect/';

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
verify('/core/core/sys/role/list').then((res) => {
  if (res) {
    verify('/core/core/sys/org/list').then((res) => {
      showOR.value = res;
    });
  }
});
</script>
<style lang='scss' scoped>
.dr-add {
  margin-right: 20px;
}
</style>