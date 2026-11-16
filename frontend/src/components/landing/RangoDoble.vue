<script setup lang="ts">
const props = defineProps<{ min: number; max: number; paso: number }>()
const modelo = defineModel<[number, number]>({ required: true })

function cambiar(i: 0 | 1, e: Event) {
  const el = e.target as HTMLInputElement
  const v = Number(el.value)
  // Las manijas no se cruzan: cada una se detiene un paso antes de la otra.
  const limitado = i === 0 ? Math.min(v, modelo.value[1] - props.paso) : Math.max(v, modelo.value[0] + props.paso)
  el.value = String(limitado)
  modelo.value = i === 0 ? [limitado, modelo.value[1]] : [modelo.value[0], limitado]
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
