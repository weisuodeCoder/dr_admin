<template>
  <Card title="基本信息" shadow="never" cardStyle="border:none" :bodyStyle="{padding: '20px 0'}">
    <!-- <template #head-btn>
    </template> -->
    <template #body>
      <el-tabs tab-position="left" lazy>
        <el-tab-pane label="基本信息">
          <Basic></Basic>
        </el-tab-pane>
        <el-tab-pane label="更改头像">
          <Avatar></Avatar>
        </el-tab-pane>
        <el-tab-pane label="教育信息">教育信息</el-tab-pane>
      </el-tabs>
    </template>
  </Card>
</template>
<script setup>
import Card from '@/components/tools/card.vue';
import Basic from '@/components/personal/setting/basic/basic.vue';
import Avatar from '@/components/personal/setting/basic/avatar.vue';
</script>
<style lang='scss' scoped>
</style>