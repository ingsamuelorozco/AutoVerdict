<script setup lang="ts">
import SiluetaLateral from './SiluetaLateral.vue'
import type { Medidas } from '@/lib/tipos'

/**
 * El catálogo aún no tiene fotos verificadas del modelo exacto: se muestra la silueta generada a escala
 * sobre un plano negro (como una foto de estudio), nunca la foto de otro modelo ni un ícono de imagen rota.
 */
defineProps<{ medidas: Medidas; nombre: string }>()
</script>

<template>
  <div class="sobre-foto relative aspect-[16/9] overflow-hidden bg-[#0d0d0d]">
    <div class="absolute inset-x-6 bottom-5 top-10">
      <SiluetaLateral :medidas="medidas" color="#f2f2f2" :etiqueta="`Silueta esquemática del ${nombre}`" />
    </div>
    <span class="absolute left-4 top-3 text-[10px] font-bold uppercase tracking-maquinado text-apagado">Silueta a escala</span>
  </div>
</template>
