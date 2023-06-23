import $api from '@/api/api';

export const apiApps = () => {
    return $api.post('/core/authc/user/resource/apps', {});
}