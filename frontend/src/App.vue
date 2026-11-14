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
      <Transition mode="out-in" enter-from-class="opacity-0" leave-to-class="opacity-0">
        <component :is="Component" />
      </Transition>
    </RouterView>
  </main>
  <PieDePagina />
  <BarraComparar v-if="!$route.path.startsWith('/comparador')" />
  <MenuInferiorMovil />
</template>
