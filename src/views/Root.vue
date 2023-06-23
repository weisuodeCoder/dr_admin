<template>
  <el-container class="dr-home">
    <el-container>
      <!-- 页面左侧 212735-->
      <Animate :isShow="isCollapse">
        <el-aside>
          <el-menu :collapse="isCollapse" router active-text-color="#ffffff" background-color="#2b3342" text-color="#4b9cd6" :unique-opened="true">
            <!-- 一级菜单 -->
            <template v-for="first in menus" :key="first.id">
              <el-menu-item v-if="first.isRouter==1" :index="first.path" @click="tabAdd(first)">
                <i class="dr-line">
                  <img class="dr-icon" :src="first.icon" />
                </i>
                <template #title>
                  <span>
                    {{first.title}}
                  </span>
                </template>
              </el-menu-item>
              <el-sub-menu v-if="first.isRouter==0" :index="first.id">
                <template #title>
                  <i class="dr-line">
                    <img class="dr-icon" :src="first.icon" />
                  </i>
                  <span>
                    {{first.title}}
                  </span>
                </template>
                <!-- 二级菜单 -->
                <template v-for="second in first.children" :key="second.id">
                  <el-menu-item v-if="second.isRouter==1" :index="second.path" @click="tabAdd(second)">
                    <i class="dr-line">
                      <img class="dr-icon" :src="second.icon" />
                    </i>
                    <template #title>
                      <span>
                        {{second.title}}
                      </span>
                    </template>
                  </el-menu-item>
                  <el-sub-menu v-if="second.isRouter==0" :index="second.id">
                    <template #title>
                      <i class="dr-line">
                        <img class="dr-icon" :src="second.icon" />
                      </i>
                      <span>
                        {{second.title}}
                      </span>
                    </template>
                    <!-- 三级菜单 -->
                    <el-menu-item v-for="third in second.children" :key="third.id" :index="third.path" @click="tabAdd(third)">
                      <i class="dr-line">
                        <img class="dr-icon" :src="third.icon" />
                      </i>
                      <template #title>
                        <span>
                          {{third.title}}
                        </span>
                      </template>
                    </el-menu-item>
                  </el-sub-menu>
                </template>
              </el-sub-menu>
            </template>
          </el-menu>
        </el-aside>
      </Animate>
      <!-- 页面右侧 -->
      <el-main class="dr-content">
        <Header @changeMenu="onChangeMenu" @routerChange="onRouterChange"></Header>
        <el-tabs class="dr-tabs" type="border-card" v-model="tabModel" @tab-click="tabClick" @tab-remove="tabRemove">
          <el-tab-pane v-for="item in tabs" :key="item.id" :label="item.title" :name="item.id" :closable="item.name!='home'">
            <router-view v-slot="{ Component }">
              <keep-alive>
                <component :is="Component" />
              </keep-alive>
            </router-view>
          </el-tab-pane>
        </el-tabs>
      </el-main>
    </el-container>
  </el-container>
</template>
<script setup>
import { ref } from 'vue';
import router from '@/router';
import store from '@/store';
import Header from './root/header';
import Animate from './root/animate.vue';

const menus = ref([]);
const tabModel = ref('');
const tabs = ref([]);
const isCollapse = ref(false);

// 切换菜单折叠
const onChangeMenu = () => {
  isCollapse.value = !isCollapse.value;
};

// 切换tab页面
const tabClick = (_tab) => {
  // 切换组件
  let tabRouter = tabs.value.find((item) => _tab.paneName == item.id).path;
  router.push(tabRouter);
  // 切换标签页
  tabModel.value = _tab.paneName;
};

// 递归寻找路由
const resultData = (_arr, _path) => {
  for (let item of _arr) {
    if (item.isRouter == 1) {
      if (item.path == _path) {
        return item;
      }
    } else if (item.children.length > 0) {
      let result = resultData(item.children, _path);
      if (result) return result;
    }
  }
};

// heder组件路由事件
const onRouterChange = (_path) => {
  let found = false;
  let current = undefined;
  // 判断路由是否缓存
  tabs.value.some((item) => {
    if (item.path == _path) {
      found = true;
      current = item;
      return true;
    }
  });
  // 如果不存在，添加到tabs
  if (!found) {
    current = resultData(menus.value, _path);
    if (current) tabs.value.push(current);
  }
  // 切换tabs标签
  if (current) {
    tabModel.value = current.id;
    router.push(_path);
  }
};

// 添加tab页面，并缓存页面
const tabAdd = (_current) => {
  let found = false;
  // 判断选中的菜单是否存在
  tabs.value.some((item) => {
    if (item.id == _current.id) {
      found = true;
      return found;
    }
  });
  // 如果不存在，则添加到tabs数组里头
  if (!found) {
    tabs.value.push(_current);
  }
  // 切换tabs标签
  tabModel.value = _current.id;
};

// 删除tab标签，同时会清除焕春页面
const tabRemove = (_target) => {
  if (tabModel.value == _target) {
    tabs.value.forEach((_item, _key) => {
      if (_target == _item.id) {
        // 选择上一个tab页面，并切换路由
        let key = _key == 0 ? 0 : _key - 1;
        tabModel.value = tabs.value[key].id;
        router.push(tabs.value[key].path);
        return;
      }
    });
  }
  // 从tabs数组删除当前节点数据
  if (_target) tabs.value = tabs.value.filter((_tab) => _target != _tab.id);
};

// 初始化参数
if (store.state.routers.info.length > 0) {
  let treeArr = store.state.routers.info[0].children;
  menus.value = treeArr;
  for (let arr of treeArr) {
    if (arr.name == 'home') {
      tabAdd(arr);
      if (window.location.hash.replace('#', '') == '/') {
        router.push('/home');
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.el-tabs--border-card > .el-tabs__content {
  padding: 0;
}
.el-main {
  padding: 0;
}
.dr-tabs {
  margin: 0 20px;
  background-color: #fff;
}
.el-tabs__header {
  margin: 0;
}
.dr-home {
  height: 100%;
  // 右侧
  .dr-aside {
    background-color: #2b3342;
  }
  //   左侧
  .dr-content {
    background-color: #ecf0f1;
  }
}
.dr-line {
  width: 18px;
  margin-right: 5px;
  line-height: 0; // 使元素垂直居中
  text-align: center;
  // vertical-align: middle;
  // display:table-cell
}
.dr-icon {
  width: 18px;
}
.el-sub-menu {
  display: grid;
}
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}
.el-menu {
  border-right: 0;
}
.el-aside {
  width: 100%;
  overflow: hidden;
}

.moveAside-enter-active,
.moveAside-leave-active {
  transition: width 100s ease-in-out;
}

.moveAside-enter {
  width: 200px;
}
.moveAside-leave-to {
  width: 64px;
}
</style>