<script setup lang="ts">
defineProps<{ titulo: string; texto: string; lado: 'izquierda' | 'derecha' }>()
</script>

<template>
  <li>
    <h3>
      <span>{{ titulo }}</span>
    </h3>
    <p>{{ texto }}</p>
  </li>
</template>
