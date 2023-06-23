<template>
  <Dialog :title="title" ref="show" width="800" :info="info">
    <template #body>
      <el-form :model="info.val" label-width="80" label-position="left" :rules="rules" ref="from">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="字典编码" prop="code">
              <el-input :disabled="disabled" v-model="info.val.code" placeholder="请输入系统唯一编码" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item :disabled="disabled" label="字典名称" prop="name">
              <el-input :disabled="disabled" v-model="info.val.name" placeholder="请输入字典名称" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="数据类型" prop="type">
              <el-select v-model="info.val.type" placeholder="请选择字典类型" :disabled="disabled">
                <el-option label="数组数据" value="select" />
                <el-option label="树形数据" value="tree" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="字典描述" prop="description">
              <el-input :disabled="disabled" v-model="info.val.description" placeholder="请输入描述信息" :autosize="{ minRows: 2, maxRows: 4 }" type="textarea" />
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
import { ref, reactive, defineEmits, defineExpose, computed } from 'vue';
import { ElMessage } from 'element-plus';
import Dialog from '@/components/tools/dialog.vue';
import { apiCreate, apiUpdate, apiShow } from '@/api/core/sso/dict-list';

const emits = defineEmits(['onChange']);
const show = ref(null);
const from = ref(null);
const info = reactive({ val: {} });
const title = ref('');
let id = 0;
let type = 'show';
let state = false;
let disabled = false;

// 验证规则
const rules = reactive({
  code: [{ required: true, message: '编码不能为空', trigger: 'blur' }],
  name: [{ required: true, message: '名称不能为空', trigger: 'blur' }],
  type: [{ required: true, message: '必须指定类型', trigger: 'change' }],
});

// 显示
const onShow = (_id, _type) => {
  id = _id;
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
  title.value = '字典__' + join;
  onRefresh();
  show.value.onShow();
};

// 获取数据
const onRefresh = () => {
  // 获取当前项数据
  if (id != 0 && id != undefined) {
    apiShow(id).then((res) => {
      info.val = res.data;
    });
  }
};

// 提交按钮逻辑
const doSubmit = (rule) => {
  if (!rule) return;
  if (type == 'show') {
    show.value.onClose();
  }
  rule.validate((valid) => {
    if (valid) {
      if (type == 'create') {
        // create
        apiCreate(info.val).then((res) => {
          info.val = {};
          show.value.onClose();
          emits('onChange');
        });
      } else if (type == 'update') {
        // update
        apiUpdate(info.val).then((res) => {
          state = false;
          info.val = {};
          show.value.onClose();
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