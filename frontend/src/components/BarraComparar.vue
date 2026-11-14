<script setup lang="ts">
import { GitCompare, X } from 'lucide-vue-next'
import { useComparador, MAX_COMPARAR } from '@/stores/comparador'

const comp = useComparador()
</script>

<template>
  <Transition enter-from-class="translate-y-full opacity-0" leave-to-class="translate-y-full opacity-0">
    <div v-if="comp.ids.length" class="fixed inset-x-0 bottom-16 z-30 px-4 lg:bottom-4 no-imprimir">
      <div class="tarjeta mx-auto flex max-w-xl items-center gap-3 p-2 pl-4 shadow-2xl">
        <p class="text-sm"><strong class="num">{{ comp.ids.length }}</strong> de {{ MAX_COMPARAR }} seleccionados</p>
        <button class="ml-auto grid h-11 w-11 place-items-center rounded-full hover:bg-linea/50" aria-label="Vaciar selección" @click="comp.vaciar()"><X class="h-4 w-4" aria-hidden="true" /></button>
        <RouterLink :to="{ path: '/comparador', query: { ids: comp.ids.join(',') } }" class="boton-primario">
          <GitCompare class="h-4 w-4" aria-hidden="true" /> Comparar
        </RouterLink>
      </div>
    </div>
  </Transition>
</template>
