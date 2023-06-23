import store from '@/store'

// 定义全局方法，为了方便起见直接挂在到window上,由于在window上，故无需export


// 获取 hash url
const getHashUrl = () => {
    return window.location.hash.replace('#', '');
}

// 判断资源是否存在
window.hasResource = (_api) => {
    let result = false;
    try {
        let set = new Set(store.state.resources.info[getHashUrl()]);
        result = set.has(_api);
    } catch (err) {
        console.error('hasResource error!!!');
        console.error(err);
    } finally {
        return result;
    }
}

// 异步判断组员是否存在
window.verify = (_api) => {
    return new Promise((resolve, reject) => {
        resolve(hasResource(_api));
    });
}