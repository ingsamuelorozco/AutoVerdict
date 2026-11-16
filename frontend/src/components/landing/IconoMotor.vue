<script setup lang="ts">
/** Ícono de motor con el mismo trazo que lucide (24 × 24, trazo 2, puntas redondeadas): lucide no trae uno. */
withDefaults(defineProps<{ strokeWidth?: number | string }>(), { strokeWidth: 2 })
</script>

<template>
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" :stroke-width="strokeWidth" stroke-linecap="round" stroke-linejoin="round">
    <!-- Tapa y toma de aire -->
    <path d="M10 5h5" />
    <path d="M12.5 5v3" />
    <!-- Bloque con cárter -->
    <path d="M7 8h9l2 2h1.5v2H21v-2.5h1V17h-1v-2.5h-1.5V16H18l-2 2H9l-2-2H5v-2.5H3V17H2V9.5h1V12h2V8z" />
  </svg>
</template>
