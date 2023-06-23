<template>
  <el-form label-width="150">
    <el-form-item>
      <UploadImg :imgConfig="imgConfig" :croConfig="croConfig" ref="upload"></UploadImg>
    </el-form-item>
  </el-form>
  <el-text class="dr-warnings">请点击 ➕ 号选择图片上传：大小180 * 180像素支持JPG、PNG等格式，图片需小于2M</el-text>
  <br>
  <el-button class="dr-action" type="success" @click="doSubmit">更 新</el-button>
</template>
<script setup>
import { ref, reactive } from 'vue';
import { ElMessage } from 'element-plus';
import { apiUpdate, apiShow } from '@/api/core/sso/dict-item';
import UploadImg from '@/components/tools/upload-img.vue';

const imgConfig = { limit: 1 };
const croConfig = { fixedNumber: '1,1', disabled: true };
const upload = ref(null);

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
  upload.value.doSubmit();
  // if (!rule) return;
  // rule.validate((valid) => {
  //   if (valid) {
  //   } else {
  //     return false;
  //   }
  // });
};
</script>
<style lang="scss" scoped>
.dr-action {
  margin-top: 60px;
  margin-left: 220px;
}
.dr-warnings {
  margin-top: 10px;
  margin-left: 30px;
}
</style>