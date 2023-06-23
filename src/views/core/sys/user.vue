<template>
  <Card title="用户管理" shadow="never" cardStyle="border:none" :bodyStyle="{padding: '20px 0'}">
    <template #head-btn>
      <el-button v-show="showC" type="primary" size="small" @click="show.onShow(0,'create')">创建</el-button>
    </template>
    <template #body>
      <Table :columns="columns" :params="params" ref="table" lasy :emptyText="emptyText">
        <template #using="scope">
          {{scope.row.isUsing==1?'是':'否'}}
        </template>
        <template #action="scope">
          <!-- 查看 -->
          <el-button v-show="showR" link type="info" size="small" @click="show.onShow(scope.row.id, 'show')">查看</el-button>
          <!-- 关联 -->
          <el-button v-show="showConnect" link type="warning" size="small" @click="onConnect(scope.row)">关联</el-button>
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
  <Connect ref="connect"></Connect>
</template>
<script setup>
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
import { apiDelete, apiDeleteAll } from '@/api/core/sys/user';
import Card from '@/components/tools/card.vue';
import Table from '@/components/tools/table.vue';
import Info from './user/info.vue';
import Connect from './user/show.vue';

const show = ref(null);
const table = ref(null);
const connect = ref(null);

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
    prop: 'account',
    label: '账号',
    width: '180',
  },
  {
    prop: 'name',
    label: '昵称',
    width: '180',
  },
  {
    prop: 'roleName',
    label: '角色',
    width: '180',
  },
  {
    prop: 'levelName',
    label: '层级',
    width: '180',
  },
  {
    prop: 'orgName',
    label: '机构',
    width: '180',
  },
  {
    prop: 'isUsing',
    label: '是否启用',
    width: '0',
    slot: 'using',
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
  url: '/core/core/sys/user/list',
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
  table.value.onRefresh();
};

const onConnect = (row) => {
  if (row.level == 3) {
    connect.value.onShow(row.name, row.account, row.id);
  } else {
    ElMessage.warning({ message: '管理员用户无需关联职位！' });
  }
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
const showConnect = ref(false);
const emptyText = ref('权限不足');
const rootPath = '/core/core/sys/user/';

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
verify('/core/core/sys/connect/list').then((res) => {
  showConnect.value = res;
});
verify(rootPath + 'list').then((res) => {
  emptyText.value = '暂无数据';
  onRefresh();
});
</script>
<style lang='scss' scoped>
.dr-body {
  display: flex;
  justify-content: left;
  .dr-left {
    width: 400px;
    margin-right: 20px;
  }
  .dr-right {
    flex: 1;
    width: calc(400px);
  }
}
</style>