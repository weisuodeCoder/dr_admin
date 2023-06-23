<template>
  <router-view />
</template>
<script setup>
import store from '@/store';
import router from '@/router';

if (sessionStorage.getItem('store')) {
  let state = sessionStorage.getItem('store');
  store.replaceState(
    Object.assign({}, store.state, JSON.parse(state == undefined ? '' : state))
  );
  router.push('/');
}

// 在页面刷新时将vuex里面的数据保存到sessionStorage内
window.addEventListener('beforeunload', () => {
  let state = JSON.stringify(store.state);
  sessionStorage.setItem('store', state == undefined ? '' : state);
});
</script>

<style lang="scss">
html,
body {
  width: 100%;
  height: 100%;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #010c16;
  height: 100%;
}
* {
  box-sizing: border-box;
}
</style>
