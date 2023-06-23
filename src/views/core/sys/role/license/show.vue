<template>
  <el-drawer :title="title" v-model="state" size="60%" destroy-on-close :show-close="false" @closed="onCloced">
    <el-tabs type="border-card" lazy v-model="actived" class="demo-tabs" @tab-change="onChange">
      <el-tab-pane label="菜单及页面" name="router">
        <Resource v-if="actived=='router'" :pid="pid"></Resource>
      </el-tab-pane>
    </el-tabs>
  </el-drawer>
</template>
<script setup>
import { ref, defineExpose } from 'vue';
import Resource from './routerAndResource.vue';

const state = ref(false);
const title = ref('');
const pid = ref(0);
const actived = ref('router');

//当关闭抽屉后清空数据
const onCloced = () => {
  pid.value = 0;
  title.value = '';
};

// 显示
const onShow = (_data) => {
  title.value = '【' + _data.orgName + '】_【' + _data.name + '】_ 授权';
  pid.value = _data.id;
  state.value = true;
};

// tabs标签事件
const onChange = (tab) => {
  console.log(tab);
  console.log(actived.value);
};

defineExpose({ onShow });
</script>
<style lang='scss' scoped>
</style>