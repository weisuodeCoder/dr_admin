<template>
  <div class="dr-aside dr-define" ref="animate">
    <div class="dr-header">
      <img class="dr-left-logo" src="/img/manage.png" />
      <span class="dr-left-content" v-show="!isShow">
        统一应用管理端
      </span>
    </div>
    <slot></slot>
  </div>
</template>
<script setup>
import { ref, defineProps, onBeforeUnmount, watch, triggerRef } from 'vue';

const props = defineProps(['isShow']);
const animate = ref(null);
const largeWidth = '200px';
const smallWidth = '64px';
const animateTime = '0.5s';

watch(
  () => props.isShow,
  (val) => {
    if (val) {
      animate.value.classList.remove('dr-to-large');
      animate.value.classList.add('dr-to-small');
    } else {
      animate.value.classList.remove('dr-to-small');
      animate.value.classList.add('dr-to-large');
    }
  }
);
</script>

<style lang='scss' scoped>
.dr-define {
  width: v-bind(largeWidth);
}
@keyframes toSmall {
  from {
    width: v-bind(largeWidth);
  }
  to {
    width: v-bind(smallWidth);
  }
}
@keyframes toLarge {
  from {
    width: v-bind(smallWidth);
  }
  to {
    width: v-bind(largeWidth);
  }
}
.dr-to-small {
  width: v-bind(smallWidth);
  animation: toSmall v-bind(animateTime);
}
.dr-to-large {
  animation: toLarge v-bind(animateTime);
  width: v-bind(largeWidth);
}
.dr-header {
  position: relative;
  width: 100%;
  height: 70px;
  text-align: center;
  background-color: #212733;

  .dr-left-logo {
    position: absolute;
    left: 14px;
    width: 30px;
    top: 18px;
  }
  .dr-left-content {
    position: absolute;
    width: 68%;
    left: 51px;
    top: 22px;
    font-size: 18px;
    color: #f6f8fb;
    display: block;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    -o-text-overflow: ellipsis;
  }
}
</style>
