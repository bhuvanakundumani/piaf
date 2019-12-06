import Vue from 'vue'
import Router from 'vue-router'
import Theme from './views/Theme.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: '/app',
  routes: [
    {
      path: '',
      name: 'theme',
      meta: {title: 'Choix du thème'},
      component: Theme
    },
    {
      path: '/annotation',
      name: 'annotation',
      meta: {title: 'Question-réponse'},
      component: () => import('./views/Annotation.vue')
    },
    {
      path: '/introduction',
      name: 'introduction',
      meta: {title: 'Niveaux'},
      component: () => import('./views/introduction/Introduction.vue')
    },
    {
      path: '/introduction/:level/',
      name: 'examples',
      meta: {title: 'Examples'},
      component: () => import('./views/introduction/Examples.vue')
    },
    {
      path: '/introduction/:level/play',
      name: 'play',
      meta: {title: 'play'},
      component: () => import('./views/introduction/Play.vue')
    },
    {
      path: '/bravo',
      name: 'bravo',
      meta: {title: 'Bravo'},
      component: () => import('./views/Bravo.vue')
    },
    {
      path: '/*',
      component: () => import('./views/FourOhFour.vue')
    },
  ]
})
