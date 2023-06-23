<template>
  <div class="dr-header dr-clearfix">
    <el-tooltip :visible="visible" :hide-after="10">
      <template #content>
        <span>{{collspaceText}}</span>
      </template>
      <div class="dr-menu" @click="changeMenu" @mouseenter="visible=true" @mouseleave="visible=false">
        <embed :src="'/icons/'+collapsePath+'.svg'" type="image/svg+xml" class="dr-icon" />
      </div>
    </el-tooltip>
    <!-- 用户名 -->
    <div class="dr-uname">
      <el-space :size="10">
        <el-text style="color:#d48806" size="large">{{getLevel()}}</el-text>
        <el-text>{{store.state.user.info.name}}</el-text>
      </el-space>
    </div>
    <!-- 右浮动，标签反着写 -->
    <!-- 用户 -->
    <el-dropdown class="dr-user" :hide-timeout="300">
      <el-badge is-dot>
        <el-avatar src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" />
      </el-badge>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item @click="jump('/personal/setting/basic')">
            <div style="text-align:center;width:100%">
              <span class="dr-text">{{store.state.user.info.name}}</span>
              <br>
              <span class="dr-text">{{store.state.user.info.account}}</span>
            </div>
          </el-dropdown-item>
          <el-dropdown-item @click="jump('/personal/home')">
            <el-button link size="large" type="primary">个人中心</el-button>
          </el-dropdown-item>
          <el-dropdown-item @click="jump('/personal/message/mine')">
            <el-badge :value="1">
              <el-button size="large" link type="primary">我的消息</el-button>
            </el-badge>
          </el-dropdown-item>
          <el-dropdown-item divided @click="router.push('/login')">
            <el-button link size="large" type="danger">退出登录</el-button>
          </el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
    <!-- 消息 -->
    <el-tooltip :visible="visible" :hide-after="10">
      <template #content>
        <span>查看消息通知</span>
      </template>
      <div class="dr-message" @click="jump('/personal/message/system')" @mouseenter="visible=true" @mouseleave="visible=false">
        <el-badge :value="1">
          <embed src="/icons/message.svg" type="image/svg+xml" class="icon" />
        </el-badge>
      </div>
    </el-tooltip>
    <!-- 全屏操作 -->
    <el-tooltip :visible="visible" :hide-after="10">
      <template #content>
        <span>{{scrrenText}}</span>
      </template>
      <div class="dr-screen" @click="taggleScreen" @mouseenter="visible=true" @mouseleave="visible=false">
        <embed :src="'/icons/'+screenPath+'.svg'" type="image/svg+xml" class="icon" />
      </div>
    </el-tooltip>
  </div>
</template>
<script setup>
import { ref, defineEmits } from 'vue';
import router from '@/router';
import store from '@/store';

const emit = defineEmits(['changeMenu', 'routerChange']);
const screenPath = ref('full_screen');
const scrrenText = ref('全屏显示');
const collapsePath = ref('menu-left');
let collspceStatus = true;
const collspaceText = ref('折叠菜单栏');

// 路由跳转
const jump = (_path) => {
  emit('routerChange', _path);
};

// 获取显示文字
const getLevel = () => {
  const level = store.state.user.info.level;
  let result = '';
  if (level == 1) {
    result = '超级管理员:';
  } else if (level == 2) {
    result = '管理员:';
  }
  return result;
};
// 切换菜单
const changeMenu = () => {
  collspceStatus = !collspceStatus;
  if (collspceStatus) {
    collapsePath.value = 'menu-left';
    collspaceText.value = '折叠菜单栏';
  } else {
    collapsePath.value = 'menu-right';
    collspaceText.value = '展开菜单栏';
  }
  emit('changeMenu');
};
// 全屏模式切换
const taggleScreen = () => {
  let state =
    document.fullscreenElement ||
    document.msFullscreenElement ||
    document.mozFullScreenElement ||
    document.webkitFullscreenElement ||
    false;
  if (state) {
    screenPath.value = 'full_screen';
    exitFullScreen();
    scrrenText.value = '全屏显示';
  } else {
    screenPath.value = 'exit_full_screen';
    fullScreen();
    scrrenText.value = '退出全屏';
  }
};

//实现全屏
const fullScreen = () => {
  // documentElement 属性以一个元素对象返回一个文档的文档元素
  let element = document.documentElement;

  if (element.requestFullscreen) {
    element.requestFullscreen();
  } else if (element.webkitRequestFullScreen) {
    element.webkitRequestFullScreen();
  } else if (element.mozRequestFullScreen) {
    element.mozRequestFullScreen();
  } else if (element.msRequestFullscreen) {
    element.msRequestFullscreen(); // IE11
  }
};

// 退出全屏
const exitFullScreen = () => {
  if (document.exitFullScreen) {
    document.exitFullScreen();
  } else if (document.mozCancelFullScreen) {
    document.mozCancelFullScreen();
  } else if (document.webkitExitFullscreen) {
    document.webkitExitFullscreen();
  } else if (document.msExitFullscreen) {
    document.msExitFullscreen(); // IE11
  }
};
</script>
<style lang='scss' scoped>
$--collapse-text: '折叠菜单栏';
.icon {
  width: 27px;
  height: 27px;
  pointer-events: none;
}
.dr-icon {
  width: 28px;
  height: 28px;
  pointer-events: none;
}

.dr-header {
  width: 100%;
  height: 70px;
  padding: 15px;
  .dr-menu {
    float: left;
    position: relative;
    margin-top: 4px;
    margin-left: 5px;
  }
  .dr-uname {
    float: left;
    position: relative;
    margin-top: 7px;
    margin-left: 10px;
    font-weight: 600;
  }
  .dr-message {
    float: right;
    position: relative;
    margin-right: 20px;
    margin-top: 10px;
  }
  .dr-screen {
    position: relative;
    float: right;
    margin-top: 10px;
    margin-right: 17px;
  }
  .dr-user {
    float: right;
    height: 100%;
    width: 50px;
    margin-right: 10px;
  }
}
.dr-menu,
.dr-message,
.dr-screen,
.dr-user {
  &:hover {
    cursor: pointer;
  }
}
.dr-text {
  font-size: 12px;
  color: #666;
}
</style>