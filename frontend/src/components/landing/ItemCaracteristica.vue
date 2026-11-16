<script setup lang="ts">
defineProps<{ titulo: string; texto: string; lado: 'izquierda' | 'derecha' }>()
</script>

<template>
  <li :class="{ 'lg:text-right': lado === 'izquierda' }">
    <h3 :class="['flex items-center gap-3 text-lg leading-tight', { 'lg:flex-row-reverse': lado === 'izquierda' }]">
      <span class="grid h-3 w-3 shrink-0 place-items-center rounded-full border-[1.5px] border-acento" aria-hidden="true"><span class="h-1 w-1 rounded-full bg-acento" /></span>
      <span>{{ titulo }}</span>
    </h3>
    <p :class="['mt-3 max-w-[300px] text-[13px] leading-[1.9] text-tenue', { 'lg:ml-auto': lado === 'izquierda' }]">{{ texto }}</p>
  </li>
</template>
