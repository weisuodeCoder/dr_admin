import $api from '@/api/api';
import { ElMessage } from 'element-plus';
import { dataFilterNull } from '@/tools'

export const apiLists = () => {
  return $api.post('/core/core/sso/all/list-all', {});
}