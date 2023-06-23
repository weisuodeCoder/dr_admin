<template>
  <el-card :class="minHeight != undefined ? '' : 'dr-card'" :shadow="shadow!=undefined?shadow:'always'" :body-style="bodyStyle" :style="cardStyle">
    <template #header>
      <div class="dr-clearfix">
        <span class="dr-title" :style="titleStyle">{{ title }}</span>
        <div class="dr-operate">
          <!-- 卡片头部左侧内容 -->
          <slot name="head-btn"></slot>
        </div>
      </div>
    </template>
    <!-- 卡片内容 -->
    <slot name="body"></slot>
  </el-card>
</template>
<script setup>
import { defineProps } from 'vue';

const props = defineProps([
  'title',
  'titleStyle',
  'minHeight',
  'shadow',
  'bodyStyle',
  'cardStyle',
]);
</script>
<style lang="scss" scoped>
.dr-title {
  float: left;
  font-weight: bold;
}
.dr-operate {
  float: right;
}
.dr-card {
  min-height: 820px;
}
</style>