<template>
  <Card title="职位管理" shadow="never" cardStyle="border:none" :bodyStyle="{padding: '20px 0'}">
    <template #body>
      <div class="dr-clearfix dr-body">
        <div class="dr-left">
          <Orgs @onChange="onChildChange"></Orgs>
        </div>
        <div class="dr-right">
          <Role ref="role"></Role>
        </div>
      </div>
    </template>
  </Card>
</template>
<script setup>
import Card from '@/components/tools/card.vue';
import Orgs from './role/tree.vue';
import Role from './role/role.vue';
import { ref, provide, reactive } from 'vue';

const role = ref(null);
const info = reactive({});

const onChildChange = (_data) => {
  info.name = _data.name;
  info.id = _data.id;
};

provide('_data', info);
</script>
<style lang='scss' scoped>
.dr-body {
  display: flex;
  justify-content: left;
  .dr-left {
    width: 260px;
    margin-right: 20px;
  }
  .dr-right {
    flex: 1;
    width: calc(400px);
  }
}
</style>