import $api from '@/api/api';
import { ElMessage } from 'element-plus';
import { dataFilterNull } from '@/tools'

const url = '/core/core/sys/user/';

export const apiList = (data) => {
  return $api.post(url + 'list', data);
}

export const apiShow = (id) => {
  let data = { id };
  return $api.post(url + 'show', data);
}

export const apiCreate = (data) => {
  dataFilterNull(data);
  return $api.post('/user/create', data).then(res => {
    if (res.success) {
      ElMessage.success({
        message: res.message
      })
    }
  });
}

export const apiUpdate = (data) => {
  dataFilterNull(data);
  return $api.post(url + 'update', data).then(res => {
    if (res.success) {
      ElMessage.success({
        message: res.message
      })
    }
  });
}

export const apiDelete = (id) => {
  let data = { id };
  return $api.post(url + 'delete', data).then(res => {
    if (res.success) {
      ElMessage.success({
        message: res.message
      })
    }
  });
}

export const apiDeleteAll = (ids) => {
  let data = { ids };
  return $api.post(url + 'delete-all', data).then(res => {
    if (res.success) {
      ElMessage.success({
        message: res.message
      })
    }
  });
}