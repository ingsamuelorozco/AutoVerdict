<script setup lang="ts">
defineProps<{ titulo: string; texto: string; lado: 'izquierda' | 'derecha' }>()
</script>

<template>
  <li>
    <h3 class="text-lg leading-tight">
      <span>{{ titulo }}</span>
    </h3>
    <p class="mt-3 text-[13px] leading-[1.9] text-tenue">{{ texto }}</p>
  </li>
</template>
