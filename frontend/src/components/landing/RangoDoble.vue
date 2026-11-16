<script setup lang="ts">
const props = defineProps<{ min: number; max: number; paso: number }>()
const modelo = defineModel<[number, number]>({ required: true })

const pct = (v: number) => ((v - props.min) / (props.max - props.min)) * 100

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
    <div class="relative mt-2 h-[14px]">
      <div class="absolute inset-x-[7px] top-1/2 h-[3px] -translate-y-1/2 bg-linea" aria-hidden="true">
        <div class="absolute inset-y-0 bg-acento" :style="{ left: `${pct(modelo[0])}%`, right: `${100 - pct(modelo[1])}%` }" />
      </div>
      <input type="range" class="rango-input" :min="min" :max="max" :step="paso" :value="modelo[0]" @input="cambiar(0, $event)" />
      <input type="range" class="rango-input" :min="min" :max="max" :step="paso" :value="modelo[1]" @input="cambiar(1, $event)" />
    </div>
  </div>
</template>

<style scoped>
/* Dos rangos nativos superpuestos: solo las manijas reciben el puntero. */
.rango-input { position: absolute; inset: 0; width: 100%; height: 100%; margin: 0; background: transparent; pointer-events: none; -webkit-appearance: none; appearance: none; }
.rango-input::-webkit-slider-runnable-track { height: 14px; background: transparent; }
.rango-input::-moz-range-track { background: transparent; }
.rango-input::-webkit-slider-thumb { -webkit-appearance: none; appearance: none; pointer-events: auto; width: 14px; height: 14px; border-radius: 9999px; background: #fff; border: 3px solid rgb(var(--acento)); }
.rango-input::-moz-range-thumb { pointer-events: auto; box-sizing: border-box; width: 14px; height: 14px; border-radius: 9999px; background: #fff; border: 3px solid rgb(var(--acento)); }
.rango-input::-webkit-slider-thumb { cursor: grab; }
.rango-input::-moz-range-thumb { cursor: grab; }
</style>
