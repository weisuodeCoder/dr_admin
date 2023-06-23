<template>
  <Card title="资源管理" shadow="never" cardStyle="border:none" :bodyStyle="{padding: '20px 0'}">
    <template #body>
      <div class="dr-clearfix dr-body">
        <div class="dr-left">
          <Tree></Tree>
        </div>
        <div class="dr-right">
          <Resource></Resource>
        </div>
      </div>
    </template>
  </Card>
</template>
<script setup>
import Card from '@/components/tools/card.vue';
import Tree from './resource/tree.vue';
import Resource from './resource/resource.vue';
import { ref, provide } from 'vue';

const id = ref(null);

provide('_id', id);
</script>
<style lang='scss' scoped>
.dr-body {
  display: flex;
  justify-content: left;
  .dr-left {
    width: 400px;
    margin-right: 20px;
  }
  .dr-right {
    flex: 1;
    width: calc(400px);
  }
}
</style>