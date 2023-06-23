import $api from '@/api/api';
import { ElMessage } from 'element-plus';
import { dataFilterNull } from '@/tools'

const url = '/core/core/sys/license/';

export const apiList = (data) => {
    return $api.post(url + 'list', data);
}

export const apiListAll = () => {
    let data = {};
    return $api.post(url + 'list-all', data);
}

export const apiLicense = (data) => {
    dataFilterNull(data);
    return $api.post(url + 'license', data).then(res => {
        if (res.success) {
            ElMessage.success({
                message: res.message
            })
        }
    });
}