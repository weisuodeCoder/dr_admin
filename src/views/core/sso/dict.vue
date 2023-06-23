<template>
  <Card title="字典管理" shadow="never" cardStyle="border:none" :bodyStyle="{padding: '20px 0'}">
    <template #body>
      <div class="dr-clearfix dr-body">
        <div class="dr-left">
          <List></List>
        </div>
        <div class="dr-right">
          <Item></Item>
        </div>
      </div>
    </template>
  </Card>
</template>
<script setup>
import Card from '@/components/tools/card.vue';
import { reactive, provide } from 'vue';
import List from './dict/list.vue';
import Item from './dict/item.vue';

const dict_data = reactive({
  val: { id: 0, name: '', type: '', typeName: '' },
});

provide('dict_data', dict_data);
</script>
<style lang='scss' scoped>
.dr-body {
  display: flex;
  justify-content: left;
  .dr-left {
    width: 500px;
    margin-right: 20px;
  }
  .dr-right {
    flex: 1;
    width: calc(500px);
  }
}
</style>