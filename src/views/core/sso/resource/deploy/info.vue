<template>
  <el-drawer v-model="state" :title="title" :append-to-body="true" @closed="onCloced" destroy-on-close>
    <el-form :model="info.val" label-width="80" label-position="left" :rules="rules" ref="from">
      <el-form-item label="资源名称" prop="name">
        <el-input clearable :disabled="disabled" v-model="info.val.name" placeholder="请输入资源名称" />
      </el-form-item>
      <el-form-item label="资源api" prop="api">
        <el-input clearable :disabled="disabled" v-model="info.val.api" placeholder="请输入api" />
      </el-form-item>
      <el-form-item label="资源类型" prop="type">
        <el-select clearable @change="onChange" :disabled="disabled" v-model="info.val.type" placeholder="请选择资源类型">
          <el-option v-for="item in types" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="账号等级" prop="level">
        <el-select @change="onSelectChange" v-model="info.val.level" placeholder="请选择等级" :disabled="disabled">
          <el-option label="系统管理员" :value="1" />
          <el-option label="管理员" :value="2" />
          <el-option label="普通用户" :value="3" />
          <el-option label="通用" :value="4" />
        </el-select>
      </el-form-item>
      <el-form-item label="描述信息">
        <el-input v-model="info.val.description" placeholder="描述信息" :autosize="{ minRows: 3, maxRows: 5 }" type="textarea" />
      </el-form-item>
    </el-form>
    <el-button size="small" type="success" @click="doSubmit(from)">
      {{ getName() }}
    </el-button>
  </el-drawer>
</template>
<script setup>
import { ref, reactive, defineExpose, defineEmits, computed } from 'vue';
import { apiCreate, apiUpdate, apiShow } from '@/api/core/sso/resource';

const info = reactive({ val: { level: 3 } });
const emits = defineEmits(['onChange']);
const from = ref(null);
const state = ref(false);
const title = ref('');
let disabled = true;
let type = 'show';

// 资源类型选项
const types = [
  { label: '添加', value: 'create' },
  { label: '删除', value: 'delete' },
  { label: '编辑', value: 'update' },
  { label: '查看', value: 'show' },
  { label: '列表', value: 'list' },
  { label: '删除所有', value: 'delete-all' },
  { label: '其他', value: 'other' },
];

// 表单验证规则
const rules = reactive({
  name: [{ required: true, message: '内容不能为空', trigger: 'blur' }],
  type: [{ required: true, message: '内容不能为空', trigger: 'change' }],
});

// 显示
const onShow = (_id, _pid, _type) => {
  info.val.pid = _pid;
  type = _type;
  let join = '';
  if (_type == 'create') {
    disabled = false;
    join = '创建';
  } else if (_type == 'show') {
    disabled = true;
    join = '查看';
  } else if (_type == 'update') {
    disabled = false;
    join = '更新';
  }
  title.value = '资源__' + join;
  onRefresh(_id);
};

const onCloced = () => {
  info.val = {};
};

const onChange = (val) => {
  if (val != 'other') {
    if (info.val.api == undefined || info.val.api == '') {
      info.val.api = val;
    } else {
      info.val.api += val;
    }
    for (let type of types) {
      if (val == type.value) {
        if (info.val.name == undefined || info.val.name == '') {
          info.val.name = '-' + type.label;
        } else {
          info.val.name += '-' + type.label;
        }
      }
    }
  }
};

const onRefresh = (_id) => {
  if (_id == 0) {
    state.value = true;
  } else {
    apiShow(_id).then((res) => {
      info.val = res.data;
      state.value = true;
    });
  }
};

// 提交
const doSubmit = (rule) => {
  if (!rule) return;
  rule.validate((valid) => {
    if (valid) {
      if (type == 'create' && info.val.pid != 0) {
        apiCreate(info.val).then((res) => {
          info.val = {};
          state.value = false;
          emits('onChange');
        });
      } else if (type == 'update') {
        apiUpdate(info.val).then((res) => {
          info.val = {};
          state.value = false;
          emits('onChange');
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
      name = '查看';
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