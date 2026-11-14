<script setup lang="ts">
import { AlertCircle, RefreshCw, SearchX, WifiOff } from 'lucide-vue-next'
import { useOnline } from '@vueuse/core'
import { T } from '@/lib/textos'

defineProps<{ cargando?: boolean; error?: string | null; vacio?: boolean; mensajeVacio?: string; filas?: number }>()
defineEmits<{ reintentar: [] }>()
const enLinea = useOnline()
</script>

<template>
  <div v-if="!enLinea" class="mb-4 flex items-center gap-3 border border-l-4 border-linea border-l-ambar bg-superficie p-4 text-sm" role="status">
    <WifiOff class="h-4 w-4" aria-hidden="true" /> {{ T.sinConexion }}
  </div>
  <div v-if="cargando" class="grid gap-4" aria-busy="true" aria-label="Cargando">
    <div v-for="n in filas || 3" :key="n" class="esqueleto h-28" />
  </div>
  <div v-else-if="error" class="tarjeta flex flex-col items-center gap-4 px-6 py-16 text-center" role="alert">
    <AlertCircle class="h-8 w-8 text-roja" aria-hidden="true" />
    <p class="text-xl font-bold uppercase text-tinta">{{ T.errorCarga }}</p>
    <p class="text-sm text-tenue">{{ error }}</p>
    <button class="boton-secundario" @click="$emit('reintentar')"><RefreshCw class="h-4 w-4" aria-hidden="true" /> {{ T.reintentar }}</button>
  </div>
  <div v-else-if="vacio" class="tarjeta flex flex-col items-center gap-4 px-6 py-16 text-center" role="status">
    <SearchX class="h-8 w-8 text-tenue" aria-hidden="true" />
    <p class="max-w-xl text-xl font-bold uppercase text-tinta">{{ mensajeVacio || T.sinResultados }}</p>
    <slot name="vacio" />
  </div>
  <slot v-else />
</template>
