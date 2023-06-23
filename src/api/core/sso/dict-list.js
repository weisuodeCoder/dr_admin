import $api from '@/api/api';
import { ElMessage } from 'element-plus';
import { dataFilterNull } from '@/tools'

const url = '/core/core/sso/dict-list/';

export const apiList = (data) => {
  return $api.post('/core/anon/dict/list/list', data);
}

export const apiShow = (id) => {
  let data = { id };
  return $api.post('/core/anon/dict/list/show', data);
}

export const apiCreate = (data) => {
  dataFilterNull(data);
  return $api.post(url + 'create', data).then(res => {
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