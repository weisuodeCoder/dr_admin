<template>
  <Dialog :title="title" ref="show" width="800" :info="info">
    <template #body>
      <el-form :model="info.val" label-width="50" label-position="left" :rules="rules" ref="from">
        <!-- 账号，名称 -->
        <el-row gutter="30">
          <el-col :span="12">
            <el-form-item label="账号" prop="account">
              <el-input clearable :disabled="type!='create'" v-model="info.val.account" placeholder="请输入账号" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="名称" prop="name">
              <el-input clearable :disabled="disabled" v-model="info.val.name" placeholder="请输入名称" />
            </el-form-item>
          </el-col>
        </el-row>
        <!-- 等级 -->
        <el-row gutter="30">
          <el-col :span="12">
            <el-form-item label="等级" prop="level">
              <el-select @change="onSelectChange" v-model="info.val.level" placeholder="请选择等级" :disabled="disabled">
                <el-option label="系统管理员" :value="1" />
                <el-option :disabled="showOrg" label="管理员" :value="2" />
                <el-option label="普通用户" :value="3" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="启用" prop="isUsing">
              <el-select v-model="info.val.isUsing" placeholder="是否启用账号" :disabled="disabled">
                <el-option label="是" :value="1" />
                <el-option label="否" :value="0" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <!-- 机构，职位 -->
        <el-row gutter="30">
          <el-col :span="12" v-if="info.val.level==2">
            <el-form-item label="机构" prop="orgId">
              <el-tree-select filterable :disabled="disabled" v-model="info.val.orgId" :props="defaultProps" :data="orgList.val" check-strictly @node-click="onOrgNodeClick" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </template>
    <template #button>
      <el-button size="small" type="success" @click="doSubmit(from)">
        {{ getName() }}
      </el-button>
    </template>
  </Dialog>
</template>
<script setup>
import { Delete } from '@element-plus/icons-vue';
import {
  ref,
  reactive,
  defineProps,
  defineEmits,
  defineExpose,
  computed,
} from 'vue';
import Dialog from '@/components/tools/dialog.vue';
import { ElMessage } from 'element-plus';
import { md5 as password } from '@/tools/pss';
import { apiCreate, apiShow, apiUpdate } from '@/api/core/sys/user';
import { matchingFalse, matchingSome } from '@/tools/rules';
import { apiList as orgApiList } from '@/api/core/sys/org';
import { apiList as roleApiList } from '@/api/core/sys/role';

const props = defineProps(['']);
const emits = defineEmits(['onChange']);
const show = ref(null);
const from = ref(null);
const title = ref('');
const info = reactive({ val: {} });
const orgList = reactive({ val: [] }); // 机构
const roleList = reactive({ val: [] }); // 角色
const showOrg = ref(true);
let disabled = false;
let type = 'show';
let id = 0;

// tree默认显示数据
const defaultProps = {
  children: 'children',
  label: 'name',
  value: 'id',
};

// 验证规则
const rules = reactive({
  account: [
    { min: 5, max: 15, message: '长度必须在5~15之间', trigger: 'blur' },
    { required: true, message: '内容不能为空', trigger: 'blur' },
    { validator: matchingSome.isAccount, trigger: 'blur' },
  ],
  name: [
    { required: true, message: '内容不能为空', trigger: 'blur' },
    { validator: matchingFalse.notEmpty, trigger: 'blur' },
  ],
});

const onSelectChange = (val) => {
  if (val == 1) {
    info.val.orgId = 0;
  } else if (val == 2) {
  }
};

// 显示
const onShow = (_id, _type) => {
  id = _id;
  type = _type;
  let join = '';
  if (_type == 'create') {
    disabled = false;
    info.val.level = 3;
    info.val.isUsing = 1;
    join = '创建';
  } else if (_type == 'show') {
    disabled = true;
    join = '查看';
  } else if (_type == 'update') {
    disabled = false;
    join = '更新';
  }
  title.value = '账号__' + join;
  if (hasResource('/core/core/sys/org/list')) {
    showOrg.value = false; // 当用户拥有org资源，方可选择二级管理员
    onRefresh();
  }
  show.value.onShow();
};

// 获取初始化数据
const onRefresh = () => {
  if (id != 0) {
    apiShow(id).then((res) => {
      info.val = res.data;
    });
  }
  let data = {
    pageSize: 10000,
  };
  orgApiList(data).then((res) => {
    orgList.val = arr2tree(res.data.list, 'id', 'pid', 'children', 0);
  });
};

const onOrgNodeClick = (_data) => {
  let data = {
    pageSize: 10000,
    orgId: _data.id,
  };
  roleApiList(data).then((res) => {
    roleList.val = res.data.list;
  });
};

// 提交按钮逻辑
const doSubmit = (rule) => {
  if (type == 'show') {
    show.value.onClose();
  }
  if (!rule) return;
  rule.validate((valid) => {
    if (valid) {
      if (type == 'create') {
        // create
        info.val.password = password('password.toString()', '123456');
        apiCreate(info.val).then((res) => {
          show.value.onClose();
          emits('onChange');
        });
      } else if (type == 'update') {
        // update
        apiUpdate(info.val).then((res) => {
          show.value.onClose();
          emits('onChange');
        });
      }
    } else {
      return false;
    }
  });
};

// 设置当前节点为disabled
const filterDisabled = (_datas) => {
  for (let i = 0; i < _datas.length; i++) {
    if (_datas[i].id == id) {
      _datas[i].disabled = true;
      if (_datas[i].children.length > 0) {
        childDisabled(_datas[i].children);
      }
    } else if (_datas[i].children.length > 0) {
      filterDisabled(_datas[i].children);
    }
  }
};

// 设置子节点为disabled
const childDisabled = (_datas) => {
  for (let i = 0; i < _datas.length; i++) {
    _datas[i].disabled = true;
    if (_datas[i].children.length > 0) {
      childDisabled(_datas[i].children);
    }
  }
};

// 当选中上级机构时
const onPNodeClick = (_data, node) => {
  info.val.pName = _data.name;
};

// 清空上级机构
const onClear = () => {
  info.val.pid = 0;
  info.val.pName = '无';
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