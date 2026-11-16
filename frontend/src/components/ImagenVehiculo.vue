<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import SiluetaLateral from './SiluetaLateral.vue'
import { useImagenes } from '@/stores/imagenes'
import type { Medidas } from '@/lib/tipos'

/**
 * Foto de referencia del modelo (Wikimedia Commons) cuando existe; si no hay foto o no carga,
 * la silueta generada a escala sobre un plano negro, nunca un ícono de imagen rota.
 */
const props = defineProps<{ medidas: Medidas; nombre: string; imagenId?: string | null }>()
const imagenes = useImagenes()
onMounted(() => imagenes.cargar())
const fallo = ref(false)
const foto = computed(() => (props.imagenId && !fallo.value ? imagenes.porId[props.imagenId] : undefined))
</script>

<template>
  <div v-if="foto" class="relative aspect-[16/9] overflow-hidden bg-superficie">
    <img :src="foto.url" :alt="`Foto de referencia: ${nombre}`" :title="`Foto: ${foto.autor}, ${foto.licencia}`" loading="lazy" decoding="async" class="h-full w-full object-cover" @error="fallo = true" />
    <span class="absolute left-3 top-3 bg-black/60 px-2 py-1 text-[10px] font-bold uppercase tracking-maquinado text-white">Foto de referencia</span>
  </div>
  <div v-else class="sobre-foto relative aspect-[16/9] overflow-hidden bg-[#0d0d0d]">
    <div class="absolute inset-x-6 bottom-5 top-10">
      <SiluetaLateral :medidas="medidas" color="#f2f2f2" :etiqueta="`Silueta esquemática del ${nombre}`" />
    </div>
    <span class="absolute left-4 top-3 text-[10px] font-bold uppercase tracking-maquinado text-apagado">Silueta a escala</span>
  </div>
</template>
