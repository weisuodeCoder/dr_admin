<template class="test">
  <el-dialog draggable v-model="status" :width="width==undefined?'600':width" destroy-on-close @close="onClose" class="dr-dialog">
    <template #header>
      <div class="dr-header dr-clearfix">
        <div class="dr-title">{{title}}</div>
        <div class="dr-btn">
          <slot name="head-btn"></slot>
        </div>
      </div>
    </template>
    <slot name="body"></slot>
    <template #footer>
      <div class="dr-footer">
        <el-button size="small" type="primary" @click="status = false">取消</el-button>
        <slot name="button"></slot>
      </div>
    </template>
  </el-dialog>
</template>
<script setup>
import { ref, reactive, defineExpose, defineProps, toRefs } from 'vue';

let status = ref(false);

const props = defineProps(['title', 'width', 'info']);

const onShow = (state) => {
  status.value = true;
};

const onClose = () => {
  if (props.info != undefined && props.info != '' && props.info.val != '{}') {
    props.info.val = {}; // 清空绑定的表单值
  }
  status.value = false;
};

defineExpose({ onShow, onClose });
</script>
<style lang="scss" scoped>
.dr-header {
  .dr-title {
    float: left;
  }
  .dr-btn {
    float: right;
  }
}
</style>