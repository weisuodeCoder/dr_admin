<template>
  <Card title="组织管理" shadow="never" cardStyle="border:none" :bodyStyle="{padding: '20px 0'}">
    <template #body>
      <div class="dr-clearfix dr-body">
        <div class="dr-left">
          <Level @self-change="levelSelf" @all-change="levelAll"></Level>
        </div>
        <div class="dr-right">
          <Orgs ref="orgs"></Orgs>
        </div>
      </div>
    </template>
  </Card>
</template>
<script setup>
import Card from '@/components/tools/card.vue';
import Level from './org/tree.vue';
import Orgs from './org/orgs.vue';
import { ref, provide } from 'vue';

const orgs = ref(null);
const id = ref(null);

provide('_id', id);
const levelSelf = (_data) => {
  orgs.value.onShow([_data.ids], _data.name);
};

const levelAll = (_data) => {
  orgs.value.onShow(_data.ids, _data.name);
};
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