<script setup lang="ts">
import { onMounted } from 'vue'
import { useHead } from '@unhead/vue'
import BarraSuperior from '@/components/BarraSuperior.vue'
import MenuInferiorMovil from '@/components/MenuInferiorMovil.vue'
import PieDePagina from '@/components/PieDePagina.vue'
import BarraComparar from '@/components/BarraComparar.vue'
import { useAjustes } from '@/stores/ajustes'
import { T } from '@/lib/textos'

useHead({ titleTemplate: (t?: string) => (t ? `${t} · ${T.marca}` : `${T.marca} · ${T.lema}`), htmlAttrs: { lang: 'es-CO' } })
onMounted(() => useAjustes().cargar())
</script>

<template>
  <BarraSuperior />
  <main id="contenido" tabindex="-1" class="min-h-[70vh] outline-none">
    <RouterView v-slot="{ Component }">
      <Transition mode="out-in" enter-active-class="transition-opacity duration-150" leave-active-class="transition-opacity duration-150" enter-from-class="opacity-0" leave-to-class="opacity-0">
        <!-- Un único nodo raíz: varias vistas tienen raíz múltiple y la transición no puede animarlas (quedaba en blanco). -->
        <div :key="$route.path">
          <component :is="Component" />
        </div>
      </Transition>
    </RouterView>
  </main>
  <PieDePagina />
  <BarraComparar v-if="!$route.path.startsWith('/comparador')" />
  <MenuInferiorMovil />
</template>
