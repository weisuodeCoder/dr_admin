<template>
  <el-upload v-model:file-list="fileList" ref="upload" :auto-upload="false" list-type="picture-card" :limit="config.limit" :on-exceed="handleExceed" :before-upload="beforeUpload" action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15">
    <el-icon>
      <Plus />
    </el-icon>
    <template #file="{ file }">
      <el-avatar :shape="config.shape" :size="178" :src="file.url" />
      <label class="el-upload-list__item-status-label">
        <el-icon color="#fff">
          <Check />
        </el-icon>
      </label>
      <span class="el-upload-list__item-actions">
        <span class="el-upload-list__item-preview" @click="onShow(file)">
          <el-tooltip effect="light" content="查看图片">
            <el-icon>
              <ZoomIn />
            </el-icon>
          </el-tooltip>
        </span>
        <span v-if="config.cropper" class="el-upload-list__item-preview" @click="doCropper(file)">
          <el-tooltip effect="light" content="图片剪裁">
            <el-icon>
              <Scissor />
            </el-icon>
          </el-tooltip>
        </span>
        <span class="el-upload-list__item-delete" @click="handleRemove(file)">
          <el-tooltip effect="light" content="删除图片">
            <el-icon>
              <Delete />
            </el-icon>
          </el-tooltip>
        </span>
      </span>
    </template>
  </el-upload>
  <Cropper ref="cropper" @onCropper="onCropper" :options="props.croConfig"></Cropper>
  <el-dialog v-model="dialogVisible">
    <img style="width:100%;" :src="dialogImageUrl" alt="Preview Image" />
  </el-dialog>
</template>
<script setup>
import { ref, reactive, defineProps, defineExpose } from 'vue';
import { ElMessage, genFileId } from 'element-plus';
import { Plus, Scissor, Delete, Check, ZoomIn } from '@element-plus/icons-vue';
import Cropper from '@/components/tools/cropper.vue';

const dialogImageUrl = ref('');
const dialogVisible = ref(false);
const props = defineProps(['imgConfig', 'croConfig']);
const upload = ref(null);
const cropper = ref(null);

const fileList = ref([
  {
    url: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
    name: 'aaa',
  },
]);

// 设置项
let config = reactive({
  limit: 5, // 最大添加数
  shape: 'square', // 图片形状
  cropper: true, // 是否裁剪
});

// 更改设置项
config = Object.assign({}, config, props.imgConfig);

// 图片上传拦截器
const beforeUpload = () => {};

// 图片上传
const doSubmit = () => {
  upload.value.submit();
};

// 查看图片
const onShow = (file) => {
  dialogImageUrl.value = file.url;
  dialogVisible.value = true;
};

// 图片裁剪
const doCropper = (file) => {
  console.log(file);
  cropper.value.onShow(file);
};

// 当裁剪完后
const onCropper = (result) => {
  fileList.value.some((item, i) => {
    if (item.uid == result.index) {
      fileList.value.splice(i, 1);
      result.file.uid = genFileId();
      upload.value.handleStart(result.file);
      setTimeout(() => {
        // 将图片放回原来的位置
        let current = fileList.value.pop();
        fileList.value.splice(i, 0, current);
      }, 100);
      return;
    }
  });
};

// 删除当前选中项
const handleRemove = (file) => {
  console.log(file);
  upload.value.handleRemove(file);
};

// 当图片超出limit时的操作
const handleExceed = (files) => {
  if (config.limit == 1) {
    upload.value.clearFiles();
    const file = files[0];
    file.uid = genFileId();
    upload.value.handleStart(file);
  } else {
    ElMessage.warning('当前最多可上传' + config.limit + '张图片！');
  }
};

defineExpose({ doSubmit });
</script>
<style lang='scss' scoped>
.avatar-uploader .el-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
}
</style>