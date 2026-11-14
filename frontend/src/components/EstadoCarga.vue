<script setup lang="ts">
import { AlertCircle, RefreshCw, SearchX, WifiOff } from 'lucide-vue-next'
import { useOnline } from '@vueuse/core'
import { T } from '@/lib/textos'

defineProps<{ cargando?: boolean; error?: string | null; vacio?: boolean; mensajeVacio?: string; filas?: number }>()
defineEmits<{ reintentar: [] }>()
const enLinea = useOnline()
</script>

<template>
  <div v-if="!enLinea" class="mb-4 flex items-center gap-2 rounded-xl border border-ambar/40 bg-ambar/10 p-3 text-sm" role="status">
    <WifiOff class="h-4 w-4" aria-hidden="true" /> {{ T.sinConexion }}
  </div>
  <div v-if="cargando" class="grid gap-4" aria-busy="true" aria-label="Cargando">
    <div v-for="n in filas || 3" :key="n" class="esqueleto h-24" />
  </div>
  <div v-else-if="error" class="tarjeta flex flex-col items-center gap-3 p-8 text-center" role="alert">
    <AlertCircle class="h-8 w-8 text-roja" aria-hidden="true" />
    <p class="font-medium">{{ T.errorCarga }}</p>
    <p class="text-sm text-tenue">{{ error }}</p>
    <button class="boton-secundario" @click="$emit('reintentar')"><RefreshCw class="h-4 w-4" aria-hidden="true" /> {{ T.reintentar }}</button>
  </div>
  <div v-else-if="vacio" class="tarjeta flex flex-col items-center gap-3 p-8 text-center" role="status">
    <SearchX class="h-8 w-8 text-tenue" aria-hidden="true" />
    <p class="font-medium">{{ mensajeVacio || T.sinResultados }}</p>
    <slot name="vacio" />
  </div>
  <slot v-else />
</template>
