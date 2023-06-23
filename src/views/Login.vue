<template>
  <div class="dr-login">
    <div class="dr-blur dr-clearfix">
      <div class="dr-left">
        <h1 class="dr-name">统一应用管理端</h1>
      </div>
      <div class="dr-right">
        <h1 class="dr-title">登&nbsp;&nbsp;录</h1>
        <el-form :model="info" label-width="50" ref="from" :rules="rules">
          <el-form-item label="账号" prop="account">
            <el-input autofocus clearable placeholder="请输入账号" v-model="info.account" />
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input show-password clearable placeholder="请输入密码" v-model="info.password" type="password" autocomplete="off" />
          </el-form-item>
          <el-form-item>
            <el-button class="dr-submit" type="primary" :auto-insert-space="true" @click="doSubmit(from)">登录</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>
<script setup>
import { reactive, ref, getCurrentInstance } from 'vue';
import router from '../router/index';
import routes from '@/router/defineRouters';
import { useStore } from 'vuex';
import $api from '@/api/api';
import { apiApps } from '@/api/authc/user/resource';
import { matchingFalse, matchingSome } from '@/tools/rules';
import { md5 as checkPass } from '@/tools/pss';

const from = ref(null);
const store = useStore();
const { proxy } = getCurrentInstance();

const info = reactive({
  account: '',
  password: '',
});

// 初始化
const init = () => {
  // 删除内存
  sessionStorage.clear();
  // 删除动态路由
  let defineNames = [];
  let names = [];
  routes.forEach((item) => {
    if (item.name) {
      defineNames.push(item.name);
    }
  });
  let set = new Set(defineNames);
  router.getRoutes().forEach((item) => {
    if (item.name && !set.has(item.name)) {
      names.push(item.name);
    }
  });
  names.forEach((item) => {
    router.removeRoute(item);
  });
  for (let key in store.state) {
    store.commit(key + '/clear');
  }
};
init();

const rules = reactive({
  account: [
    { min: 5, max: 15, message: '长度必须在5~15之间', trigger: 'blur' },
    { required: true, message: '内容不能为空', trigger: 'blur' },
    { validator: matchingSome.isAccount, trigger: 'blur' },
  ],
  password: [
    { required: true, message: '内容不能为空', trigger: 'blur' },
    { validator: matchingFalse.notEmpty, trigger: 'blur' },
  ],
});

window.addEventListener('keydown', (e) => {
  if (e.keyCode == 13) {
    doSubmit(from.value);
  }
});

const doSubmit = (rule) => {
  if (!rule) return;
  let temp = info.password;
  info.password = checkPass('password.toString()', info.password);
  rule.validate((valid) => {
    if (valid) {
      $api.post('/user/login', info).then(
        (res) => {
          // info.account = '';
          info.password = temp;
          if (res.success) {
            apiApps().then((res) => {
              let data = setRouter(res.data);
              store.commit('user/setInfo', res.data.user);
              store.commit('routers/setInfo', data.routers);
              store.commit('resources/setInfo', data.resourcesMap);
              router.push(proxy.$route.query.redirect || '/'); // 重定向到之前页面或 /
            });
          }
        },
        (err) => {
          console.error(err);
        }
      );
    } else {
      return false;
    }
  });
};

const setRouter = (_data) => {
  let resourcesMap = {};
  // 分配资源
  _data.routers.forEach((_rote) => {
    if (_rote.path == null) return;
    resourcesMap[_rote.path] = [];
    for (let i = 0; i < _data.resources.length; ) {
      if (_rote.id == _data.resources[i].pid) {
        resourcesMap[_rote.path].push(_data.resources.splice(i, 1)[0].api);
      } else {
        i++;
      }
    }
  });
  _data.routers.unshift({ id: 0, pid: null });
  let routers = arr2tree(_data.routers, 'id', 'pid', 'children', 0);
  return { resourcesMap, routers };
};

// arr2tree算法(处理的数组: arr，主键: str，父id: str，children名字: str，筛选条件：str)
function arr2tree(_datas, _id, _parentId, _childName, _condition) {
  return _datas.filter((father) => {
    let newArr = _datas.filter((child) => {
      return father[_id] === child[_parentId];
    });
    father[_childName] = newArr;
    return father[_id] == _condition; // 返回条件，根目录id与请求id相同
  });
}
</script>
<style lang="scss" scoped>
.dr-login {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  display: flex;
  .dr-blur {
    margin: auto;
    box-shadow: 10px 10px 10px rgba(0, 0, 0, 0.5),
      -1px -1px 15px rgba(0, 0, 0, 0.08);
    width: 60%;
    height: 70%;
    background: url('@/assets/background.jpg') no-repeat;
    background-size: cover;
    background-position: center center;
    border-radius: 20px;
    .dr-left {
      float: left;
      width: 60%;
      height: 100%;
      padding: 3% 5%;
      .dr-name {
        color: #fff;
        letter-spacing: 5px;
      }
    }
    .dr-right {
      padding: 10% 7% 0;
      width: 40%;
      height: 100%;
      float: right;
      border-top-right-radius: 20px;
      border-bottom-right-radius: 20px;
      background-color: #fff;
      .dr-title {
        text-align: center;
        color: #409eff;
        margin-bottom: 25%;
      }
    }
  }
}
.dr-login::before {
  content: ' ';
  width: 100%;
  height: 100%;
  position: absolute;
  filter: blur(10px);
  transform: scale(1.5);
  z-index: -1;
  background: url('@/assets/background.jpg') no-repeat;
  background-repeat: no-repeat;
  background-size: cover;
  background-color: rgba(58, 115, 240, 0.103);
}
.dr-submit {
  margin-top: 8%;
  width: 100%;
  word-spacing: 40px;
}
.el-button > span {
  letter-spacing: 35px !important;
}
.el-form-item__label {
  color: #409eff !important;
}
</style>