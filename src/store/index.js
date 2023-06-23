import { createStore } from 'vuex'


const autoImport = {}; // 自动引入
// require.context()是webpack增加的方法
const files = require.context('./modules', true, /\.js$/);
files.keys().forEach(key => {
  let moduleObj = files(key);
  // 获取不同业务模块名称
  let reg = /.*\/(.*)\.js$/;
  let name = reg.exec(key)[1];
  autoImport[name] = moduleObj.default;
});;

export default createStore({
  state: { // 数据
  },
  getters: { // 获取方式
  },
  mutations: { // 变更
  },
  actions: { // 异步业务
  },
  modules: autoImport
})
