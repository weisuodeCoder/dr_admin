<template>
  <span>
    <img class="dr-left-logo" src="../../assets/icons/manage.png" />
  </span>
  <span class="dr-left-content">
    统一应用管理端
  </span>
</template>
<script>
export default {
  props: {
    info: Object,
  },
  setup() {},
};
</script>
<style lang="scss" scoped>
.dr-left-logo {
  position: absolute;
  left: 13px;
  width: 25px;
  top: 15px;
}
.dr-left-content {
  position: absolute;
  left: 45px;
  top: 17px;
  font-size: 16px;
  color: #4663a7;
}
</style>