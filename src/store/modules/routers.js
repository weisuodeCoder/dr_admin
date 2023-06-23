// 路由
export default {
    namespaced: true, // 调用时user/XXX
    state: {
        info: [],
        status: false,
    },
    getters: {
        getInfo() { return info }
    },
    mutations: {
        setInfo(state, data) {
            state.info = data;
        },
        setStatus(state, _status) {
            state.status = _status;
        },
        clear(state) {
            state.info = [];
            state.status = false;
        }
    },
    actions: {
    },
    modules: {
    }
}
