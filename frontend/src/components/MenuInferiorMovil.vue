<script setup lang="ts">
import { GitCompare, RefreshCw, Search } from 'lucide-vue-next'
import { useComparador } from '@/stores/comparador'

const comp = useComparador()
</script>

<template>
  <nav class="fixed inset-x-0 bottom-0 z-40 grid grid-cols-3 border-t border-linea bg-papel/95 backdrop-blur lg:hidden" aria-label="Secciones principales">
    <RouterLink to="/actualizados" class="flex min-h-[56px] flex-col items-center justify-center gap-0.5 text-xs" active-class="font-semibold text-acento">
      <RefreshCw class="h-5 w-5" aria-hidden="true" /> Actualizados
    </RouterLink>
    <RouterLink to="/buscar" class="flex min-h-[56px] flex-col items-center justify-center gap-0.5 text-xs" active-class="font-semibold text-acento">
      <Search class="h-5 w-5" aria-hidden="true" /> Buscar
    </RouterLink>
    <RouterLink :to="{ path: '/comparador', query: comp.ids.length ? { ids: comp.ids.join(',') } : {} }" class="flex min-h-[56px] flex-col items-center justify-center gap-0.5 text-xs" active-class="font-semibold text-acento">
      <GitCompare class="h-5 w-5" aria-hidden="true" /> Comparar ({{ comp.ids.length }})
    </RouterLink>
  </nav>
</template>
