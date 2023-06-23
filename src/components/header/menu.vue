<template>
  <div class="dr-container">
    <div class="dr-left" @click="doPrev"></div>
    <div class="dr-center">
      <ul class="dr-scroll dr-ban-select" ref="dr_scroll">
        <li
          class="dr-item"
          v-for="(item, x) of menus.val"
          :key="x"
          @click="onSelected(x)"
          :class="current == x ? 'dr-current' : ''"
        >
          <span>
            <img
              class="dr-icon"
              src="../../assets/icons/menus/settings-grey.png"
            />
          </span>
          <span class="dr-item-content">{{ item.meta.title }}</span>
        </li>
      </ul>
    </div>
    <div class="dr-right" @click="doNext"></div>
  </div>
</template>
<script setup>
import {
  ref,
  reactive,
  defineEmits,
  defineProps,
  toRefs,
  watchEffect,
} from "vue";
import router from "../../router/index";

const props = defineProps(["menus"]);
// 当前列表项
let arr = router.getRoutes()[0].children;
let menus = reactive({ val: [] });
// 当前项
let current = ref(0);
// 子传父
const emit = defineEmits(["onSelected"]);
// 系统被选中时
let onSelected = (x) => {
  current.value = x;
  if (menus.val[x] == undefined) return;
  let data = menus.val[x];
  let name = data.name;
  emit("onSelected", name); // 向父组件传值
};

// 获取滚动项
const dr_scroll = ref();
let doPrev = () => {
  // 上一条
  dr_scroll.value.scrollTop -= 60;
};
let doNext = () => {
  // 下一条
  dr_scroll.value.scrollTop += 60;
};

watchEffect(() => {
  menus.val = props.menus;
  onSelected(0);
});
</script>

<style lang="scss" scoped>
.dr-current {
  background-color: #2b3342;
}

.dr-container {
  display: flex;
  flex-direction: row;
  width: 100%;
  height: 100%;
  .dr-left {
    width: 25px;
    background: url(../../assets/icons/chevron-left.png) no-repeat;
    background-size: 125% 70%;
    background-position: -2px 8px;
    cursor: pointer;
    box-shadow: 6px 0px 6px rgba(255, 255, 255, 0.05);
  }
  .dr-center {
    flex: 1;
    padding: 0;
    height: 100%;
    overflow: hidden;
  }
  .dr-right {
    width: 25px;
    background: url(../../assets/icons/chevron-right.png) no-repeat;
    background-size: 125% 70%;
    background-position: -2px 8px;
    cursor: pointer;
    box-shadow: -6px 0px 6px rgba(255, 255, 255, 0.05);
  }
}

.dr-scroll::-webkit-scrollbar {
  display: none;
}

.dr-scroll {
  margin-top: 10px;
  padding: 0;
  overflow-x: scroll;
  widows: 100%;
  height: 100%;
  scrollbar-width: none;
}

.dr-item {
  float: left;
  height: 50%;
  display: inline-block;
  padding: 5px;
  margin-right: 20px;
  margin-bottom: 20px;
  span {
    height: 100%;
    display: inline-block;
    vertical-align: middle;
    color: rgb(75, 156, 214);
  }
}

.dr-item:hover {
  background-color: #2b3342;
  cursor: pointer;
}

.dr-icon {
  width: 30px;
  padding-right: 5px;
}

.dr-item-content {
  line-height: 33px;
}
</style>