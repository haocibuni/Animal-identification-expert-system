import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import bestLocation from "./components/bestLocation";
import animal from "./components/animal";
import rules from "./components/animal/rules";
// 导入公共样式表
import '../src/assets/resert.css'

Vue.use(Router)

export default new Router({
  routes: [
    // {
    //   path: '/',
    //   name: 'bestLocation',
    //   component: bestLocation
    // },
    {
      path: '/',
      name: 'animal',
      component: animal
    },
    {
      path: '/rules',
      name: 'rules',
      component: rules
    },
    {
      path: '/home',
      name: 'home',
      component: Home
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/About.vue')
    }
  ]
})
