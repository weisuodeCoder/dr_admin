//axios.js 
import router from "@/router";
import axios from "axios";
import { ElMessage, ElLoading, ElMessageBox } from 'element-plus';

// 1.创建axios实例
const instance_axios = axios.create({
  // 设置超时时间
  time: 2000
})
let loadingInstance;
// 2.请求拦截器
instance_axios.interceptors.request.use((config) => {
  //在发送之前做点什么
  // 1.设置全局加载动画
  loadingInstance = ElLoading.service({
    background: 'rgba(0, 0, 0, 0.7)',
    text: '加载中',
    fullscreen: true
  });
  // 3.为请求头添加token
  const isLogin = config.headers.Authorization ? true : false;
  if (!isLogin) {
    config.headers.Authorization = sessionStorage.getItem("token");
  }
  // 2.如果是list请求，检查并添加search属性
  let url = config.url;
  url = url.split("/");
  if (url[url.length - 1] == 'list' && config.data.search == undefined) {
    config.data.search = {};
  }
  return config;
}, (err) => {
  //对请求错误做点什么
  return err;
})

// 3.响应拦截器
instance_axios.interceptors.response.use((res) => {
  if (res.headers.authorization != undefined && res.headers.authorization != "") {
    sessionStorage.setItem("token", res.headers.authorization);
  }
  loadingInstance.close();
  res = res.data;
  if (!res.success) {
    alertError(res);
  } else if (res.code == 10002) {
    router.push("/login");
  }
  return res;
}, (err) => {
  loadingInstance.close();
  err = err.response;
  if (err.status == 401) {
    if (Object.keys(err.data).length != 0) {
      switch (err.data.code) {
        case 20006:
          open(err.data.message, "/login")
          break;
        case 20010:
          open(err.data.message, "/login")
        default:
          alertError(err.data);
          break;
      }
    }
  } else {
    ElMessage.error({
      message: "发生错误，请联系管理员!"
    })
  }
})

const alertError = (res) => {
  ElMessage.error({
    dangerouslyUseHTMLString: true,
    message: `<p style="margin-bottom:5px;">错误码：` + res.code + `</p><p>` + res.message + `</p>`
  });
}

const open = (_content, _action) => {
  const messageDom = document.getElementsByClassName('is-message-box')[0];
  if (messageDom === undefined) { // 始终保证页面上只有一个messageBox
    ElMessageBox.alert(`${_content}`, `发生错误：`, {
      autofocus: false,
      confirmButtonText: '确定',
      closeOnClickModal: false,
      closeOnPressEscape: false,
      showClose: false
    }).then(res => {
      if (res == 'confirm' && _action == "/login") {
        sessionStorage.clear();
        router.push(_action);
      }
    })
  }
}

// 4.导出
export default instance_axios;
