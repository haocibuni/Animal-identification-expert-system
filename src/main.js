import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'


// 引入axios包
import axios from 'axios'

Vue.prototype.$axios = axios;
//引入qs
import qs from 'qs'

Vue.prototype.$qs = qs


// 引入element-UI
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

Vue.use(ElementUI);


Vue.config.productionTip = false

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')
