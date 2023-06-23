import instance_axios from './index';

const baseURL = 'http://localhost:10013';
const $api = {};

// 封装post
$api.post = (apiUrl, params) => {
  let httpUrl = baseURL + apiUrl;
  return instance_axios.post(httpUrl, params);
}

export default $api;