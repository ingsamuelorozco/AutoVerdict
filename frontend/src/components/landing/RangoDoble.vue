<script setup lang="ts">
defineProps<{ min: number; max: number; paso: number }>()
const modelo = defineModel<[number, number]>({ required: true })

function cambiar(i: 0 | 1, e: Event) {
  const v = Number((e.target as HTMLInputElement).value)
  modelo.value = i === 0 ? [v, modelo.value[1]] : [modelo.value[0], v]
}
</script>

<template>
  <div>
    <div class="relative">
      <input type="range" :min="min" :max="max" :step="paso" :value="modelo[0]" @input="cambiar(0, $event)" />
      <input type="range" :min="min" :max="max" :step="paso" :value="modelo[1]" @input="cambiar(1, $event)" />
    </div>
  </div>
</template>
