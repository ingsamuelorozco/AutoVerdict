<script setup lang="ts">
import SiluetaLateral from './SiluetaLateral.vue'
import type { Medidas } from '@/lib/tipos'

/**
 * El catálogo aún no tiene fotos verificadas del modelo exacto: se muestra la silueta generada a escala
 * sobre un degradado oscuro, nunca la foto de otro modelo ni un ícono de imagen rota.
 */
defineProps<{ medidas: Medidas; nombre: string }>()
</script>

<template>
  <div class="relative aspect-[16/9] overflow-hidden rounded-xl bg-gradient-to-br from-[#26231c] via-[#17150f] to-[#0c0b08] text-[#e9e3d6]">
    <div class="absolute inset-x-4 bottom-3 top-6">
      <SiluetaLateral :medidas="medidas" color="#e9e3d6" :etiqueta="`Silueta esquemática del ${nombre}`" />
    </div>
    <span class="absolute left-3 top-2 text-[10px] uppercase tracking-widest text-[#e9e3d6]/60">Silueta a escala</span>
  </div>
</template>
