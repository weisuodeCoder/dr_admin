<template>
  <el-drawer v-model="state" :title="title" :append-to-body="true" @closed="onCloced" destroy-on-close>
    <el-form :model="info.val" label-width="80" label-position="left" :rules="rules" ref="from">
      <el-form-item label="机构" prop="orgId">
        <el-tree-select :disabled="disabled||type=='update'" filterable v-model="info.val.orgId" :props="defaultProps" :data="orgList.val" check-strictly @node-click="onOrgNodeClick" />
      </el-form-item>
      <el-form-item label="职位" prop="roleIds">
        <el-select :disabled="disabled" v-model="info.val.roleIds" placeholder="请选择职位" multiple>
          <el-option v-for="(item) of roleList.val" :key="item.id" :label="item.name" :value="item.id" />
        </el-select>
        <el-tag :type="roleList.val.length==0?'info':'warning'" style="margin-left:10px" effect="dark" round>{{roleList.val.length}}</el-tag>
      </el-form-item>
    </el-form>
    <el-button size="small" type="success" @click="doSubmit(from)">
      {{ getName() }}
    </el-button>
  </el-drawer>
</template>
<script setup>
import { ref, reactive, defineExpose, defineEmits, computed } from 'vue';
import { apiList as orgApiList } from '@/api/core/sys/org';
import { apiList as roleApiList } from '@/api/core/sys/role';
import { apiCreate, apiUpdate, apiShow } from '@/api/core/sys/connect';

const emit = defineEmits(['onChange']);
const info = reactive({ val: {} });
const from = ref(null);
const state = ref(false);
const title = ref('');
const orgList = reactive({ val: [] }); // 机构
const roleList = reactive({ val: [] }); // 角色
let id = 0;
let type = 'show';
let disabled = true;

// tree默认显示数据
const defaultProps = {
  children: 'children',
  label: 'name',
  value: 'id',
};

// 表单验证规则
const rules = reactive({
  orgId: [{ required: true, message: '内容不能为空', trigger: 'change' }],
  roleIds: [{ required: true, message: '内容不能为空', trigger: 'change' }],
});

// 显示
const onShow = (_id, _title, _pid, _type) => {
  id = _id;
  type = _type;
  let join = '';
  if (_type == 'create') {
    disabled = false;
    join = ' - 创建';
  } else if (_type == 'show') {
    disabled = true;
    join = ' - 查看';
  } else if (_type == 'update') {
    disabled = false;
    join = ' - 更新';
  }
  title.value = _title + join;
  onRefresh(_id);
  info.val.userId = _pid;
  state.value = true;
};

const onCloced = () => {
  info.val = {};
};

// 加载页面
const onRefresh = (_id) => {
  if (_id != 0 && _id != undefined) {
    apiShow(_id).then((res) => {
      info.val.orgId = res.data.orgId;
      info.val.tableId = res.data.id;
      getRoles(res.data.orgId);
      let ids = [];
      res.data.roleIds.forEach((item) => ids.push(item.roleId));
      info.val.roleIds = ids;
      console.log(info.val.roleIds);
    });
  }
  let data = {
    pageSize: 10000,
  };
  orgApiList(data).then((res) => {
    orgList.val = arr2tree(res.data.list, 'id', 'pid', 'children', 0);
  });
};

// 当选择组织后
const onOrgNodeClick = (_data, _node) => {
  let orgName = getParentName(_node);
  orgName.reverse();
  info.val.orgName = orgName.join(' -> ');
  info.val.roleIds = [];
  getRoles(_data.id);
};

// 获取角色
const getRoles = (_id) => {
  let data = {
    pageSize: 10000,
    orgId: _id,
  };
  roleApiList(data).then((res) => {
    roleList.val = res.data.list;
  });
};
// 获取路径名称
const getParentName = (_data) => {
  let nameArr = [];
  nameArr.push(_data.data.name);
  if (_data.data.pid != 0) {
    nameArr.push(...getParentName(_data.parent));
  }
  return nameArr;
};

// arr2tree算法
function arr2tree(_data, _id, _parentId, _childName, _condition) {
  return _data.filter((father) => {
    let newArr = _data.filter((child) => {
      return father[_id] === child[_parentId];
    });
    father[_childName] = newArr;
    return _condition == 0
      ? father[_parentId] == _condition
      : father[_id] == _condition;
  });
}

// 提交
const doSubmit = (rule) => {
  if (!rule) return;
  rule.validate((valid) => {
    if (valid) {
      if (id == 0) {
        apiCreate(info.val).then((res) => {
          state.value = false;
          emit('onChange');
        });
      } else {
        apiUpdate(info.val).then((res) => {
          state.value = false;
          emit('onChange');
        });
      }
    } else {
      return false;
    }
  });
};

// 获取按钮名称
const getName = computed(() => {
  return () => {
    let name = '';
    if (type == 'create') {
      name = '创建';
    } else if (type == 'show') {
      name = '确定';
    } else if (type == 'update') {
      name = '更新';
    }
    return name;
  };
});

defineExpose({ onShow });
</script>
<style lang="scss" scoped>
</style>