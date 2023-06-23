import Login from '../views/Login.vue'
import Root from '../views/Root.vue'
import NotFound from '../views/NotFound.vue'

// 基础路由
const routes = [
    {
        path: '/',
        name: 'root',
        component: Root,
    }, {
        path: '/login',
        name: 'login',
        component: Login
    }, {
        path: '/404',
        name: '404',
        component: NotFound
    }, {// 所有未定义的路由都跳转到404页面，必须放在最后
        path: '/:pathMatch(.*)',
        redirect: '/404'
    }
];

export default routes;