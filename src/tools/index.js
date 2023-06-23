// 删除对象空值
export const dataFilterNull = (data) => {
  Object.keys(data).forEach(key => {
    if (isEmpty(data[key])) {
      delete data[key];
    }
  })
}

// 判断传入的值是否为空
const isEmpty = (obj) => {
  if (typeof obj === 'undefined' || obj === null || obj === '') return true;
  return false
}

// 获取所有子id ({},id,childrenName)
export const getChildIds = (_data, _id = "id", _children = "children") => {
  let ids = [];
  ids.push(_data[_id]);
  _data[_children].forEach((item, x) => {
    ids.push(...getChildIds(item));
  })
  return ids;
}

// img转base64
export const imageToBase64 = (img) => {
  // Vue.prototype.$imageToBase64 = img => { //定义全局
  let canvas = document.createElement("canvas");
  canvas.width = img.width;
  canvas.height = img.height;
  let ctx = canvas.getContext("2d");
  ctx.drawImage(img, 0, 0, img.width, img.height);
  let ext = img.src.substring(img.src.lastIndexOf(".") + 1).toLowerCase();
  let dataURL = canvas.toDataURL("image/jpeg" + ext);
  return dataURL;
};

// base64转file
export const base64ToFile = (urlData, fileName) => {
  let arr = urlData.split(',');
  let mime = arr[0].match(/:(.*?);/)[1];
  let bytes = atob(arr[1]); // 解码base64
  let n = bytes.length
  let ia = new Uint8Array(n);
  while (n--) {
    ia[n] = bytes.charCodeAt(n);
  }
  return new File([ia], fileName, { type: mime });
}

export const urlToFile = (url, callBack) => {
  let img = new Image();
  img.crossOrigin = '';
  img.src = url;
  img.onload = () => {
    let base64 = imageToBase64(img);
    let file = base64ToFile(base64);
    // 使用回调函数返回结果
    callBack && typeof callBack == 'function' && callBack(file);
    return file;
  }
}



// 验证是否登录
// export const checkLogin = () => {
//   if (localStorage.getItem("token") != undefined) {
//     return true;
//   }
// }