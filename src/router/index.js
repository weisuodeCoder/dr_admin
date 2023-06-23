import { createRouter, createWebHashHistory } from 'vue-router'
import routes from './defineRouters'
import store from '@/store'


const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  scrollBehavior: () => ({ y: 0 }), // 路由跳转后页面滚动到顶部
  routes
});


// 白名单
const whiteList = ['/login'];

// 路由守卫
router.beforeEach((to, from, next) => {
  const isLogin = sessionStorage.token ? true : false;
  if (whiteList.includes(to.path)) { // 如果是白名单直接放行
    next();
  } else if (isLogin) {
    if (from.path == '/login') { // 登陆
      addTreeRoute(store.state.routers.info);
      next();
    } else if (!router.hasRoute('refresh')) { // 页面刷新
      addTreeRoute(store.state.routers.info);
      next();
    } else { // 直接放行
      next();
    }
  } else { // 未登陆，重定向到之前页面
    next(to.path == '/404' ? '/login' : '/login?redirect=' + to.path);
  }
});

// 添加动态路由
const addTreeRoute = (_arr) => {
  if (_arr.length > 0 && _arr[0].id == 0) {
    store.commit('routers/setStatus', true);
    let treeRoute = recursion(_arr[0].children);
    treeRoute.forEach(_child => {
      router.addRoute('root', _child);
    });
    router.addRoute('root', { name: 'refresh', path: '/refresh' }); // 添加虚拟路由，用于甄别浏览器刷新
  }
}

// 递归调用生成路由
const recursion = (_arr) => {
  let newArr = [];
  for (let item of _arr) {
    if (item.isRouter == 1 && item.component != undefined) {
      let data = {
        path: item.path,
        name: item.name,
        component: () => import(`../views/${item.component}.vue`),
      };
      if (item.children.length > 0) {
        data.children = recursion(item.children);
      }
      newArr.push(data);
    } else {
      if (item.children.length > 0) {
        newArr.push(...recursion(item.children));
      }
    }
  }
  return newArr;
}

export default router;
