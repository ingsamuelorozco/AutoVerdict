import { createRouter, createWebHistory } from 'vue-router'

export const router = createRouter({
  history: createWebHistory(),
  scrollBehavior: (to, _from, guardado) => guardado || (to.hash ? { el: to.hash, top: 140 } : { top: 0 }),
  routes: [
    { path: '/', component: () => import('./views/InicioView.vue') },
    { path: '/actualizados', component: () => import('./views/ActualizadosView.vue') },
    { path: '/buscar', component: () => import('./views/BuscarView.vue') },
    { path: '/comparador', component: () => import('./views/ComparadorView.vue') },
    { path: '/modelo', component: () => import('./views/ModeloView.vue') },
    { path: '/vehiculo/:slug', component: () => import('./views/VehiculoView.vue'), props: true },
    { path: '/reviews', component: () => import('./views/ReviewsView.vue') },
    { path: '/reviews/:slug', component: () => import('./views/ReviewView.vue'), props: true },
    { path: '/herramientas/credito', component: () => import('./views/CreditoView.vue') },
    { path: '/herramientas/seguro', component: () => import('./views/SeguroView.vue') },
    { path: '/herramientas/costo-total', component: () => import('./views/CostoTotalView.vue') },
    { path: '/herramientas/que-me-alcanza', component: () => import('./views/QueMeAlcanzaView.vue') },
    { path: '/herramientas/encuentra-mi-carro', component: () => import('./views/EncuentraMiCarroView.vue') },
    { path: '/metodologia', component: () => import('./views/MetodologiaView.vue') },
    { path: '/creditos', component: () => import('./views/CreditosView.vue') },
    { path: '/:pathMatch(.*)*', component: () => import('./views/NoEncontradoView.vue') },
  ],
})
