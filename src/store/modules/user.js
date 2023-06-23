// 用户
export default {
    namespaced: true, // 调用时user/XXX
    state: {
        info: {}
    },
    getters: {
        getInfo() { }
    },
    mutations: {
        setInfo(state, data) {
            state.info = data;
        },
        clear(state) {
            state.info = {}
        }
    },
    actions: {
    },
    modules: {
    }
}
