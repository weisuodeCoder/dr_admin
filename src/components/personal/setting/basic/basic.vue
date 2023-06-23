<template>
  <el-form :model="info.val" label-width="130" label-position="right" :rules="rules" ref="from" style="width:80%;">
    <el-row :gutter="20">
      <el-col :span="12">
        <el-form-item label="昵称" prop="code">
          <el-input :disabled="true" v-model="info.val.code" placeholder="请输入字典项名称" />
        </el-form-item>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="12">
        <el-form-item label="账号" prop="label">
          <el-input :disabled="true" v-model="info.val.label" placeholder="请输入字典项名称" />
        </el-form-item>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="12">
        <el-form-item label="出生日期" prop="sort">
          <el-input-number :min="0" v-model="info.val.sort" />
        </el-form-item>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="12">
        <el-form-item label="性别" prop="type">
          <el-select v-model="info.val.type" placeholder="请选择字典类型">
            <el-option label="数组数据" value="select" />
            <el-option label="树形数据" value="tree" />
          </el-select>
        </el-form-item>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="12">
        <el-form-item label="简介" prop="description">
          <el-input v-model="info.val.description" placeholder="请输入描述信息" :autosize="{ minRows: 4, maxRows: 8 }" type="textarea" />
        </el-form-item>
      </el-col>
    </el-row>
  </el-form>
  <el-space :size="50" class="dr-action">
    <el-button type="success">更 新</el-button>
    <el-button type="info">重 置</el-button>
  </el-space>
</template>
<script setup>
import { ref, reactive } from 'vue';
import { ElMessage } from 'element-plus';
import { apiUpdate, apiShow } from '@/api/core/sso/dict-item';

const from = ref(null);
const info = reactive({ val: {} });

// 验证规则
const rules = reactive({
  code: [{ required: true, message: '编码不能为空', trigger: 'blur' }],
  label: [{ required: true, message: '名称不能为空', trigger: 'blur' }],
  type: [{ required: true, message: '必须指定类型', trigger: 'change' }],
});

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
  rule.validate((valid) => {
    if (valid) {
    } else {
      return false;
    }
  });
};
</script>
<style lang="scss" scoped>
.dr-action {
  margin-top: 30px;
  margin-left: 130px;
}
</style>