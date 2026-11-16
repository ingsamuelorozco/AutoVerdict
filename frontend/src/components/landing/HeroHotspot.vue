<script setup lang="ts">
import { computed, ref } from 'vue'
import { Plus } from 'lucide-vue-next'

const props = defineProps<{ titulo: string; texto: string; x: number; y: number }>()
const abierto = ref(false)
/** Cerca de los bordes de la foto la etiqueta se abre hacia adentro para no quedar cortada. */
const lado = computed(() => (props.x < 25 ? 'izq' : props.x > 75 ? 'der' : 'centro'))
</script>

<template>
  <span class="group absolute z-10 -translate-x-1/2 -translate-y-1/2" :style="{ left: `${x}%`, top: `${y}%` }">
    <button type="button" class="grid h-[38px] w-[38px] place-items-center rounded-full bg-acento text-white transition-colors hover:bg-acento-hondo motion-safe:animate-pulso" :aria-label="`${titulo}: ${texto}`" :aria-expanded="abierto" @click="abierto = !abierto" @blur="abierto = false">
      <Plus class="h-4 w-4" :stroke-width="3" aria-hidden="true" />
    </button>
    <span
      :class="[
        'sobre-claro pointer-events-none absolute bottom-[calc(100%+12px)] w-max max-w-[240px] bg-papel px-3.5 py-2.5 text-left shadow-menu transition-opacity',
        lado === 'izq' ? 'left-0' : lado === 'der' ? 'right-0' : 'left-1/2 -translate-x-1/2',
        abierto ? 'opacity-100' : 'opacity-0 group-hover:opacity-100 group-focus-within:opacity-100',
      ]"
      aria-hidden="true"
    >
      <span class="block text-[10px] font-bold uppercase tracking-maquinado text-acento-texto">{{ titulo }}</span>
      <span class="mt-1 block text-[13px] font-bold leading-snug text-tinta">{{ texto }}</span>
    </span>
  </span>
</template>
