<script setup lang="ts">
import { computed, ref, useId } from 'vue'
import { onClickOutside } from '@vueuse/core'
import { ChevronDown } from 'lucide-vue-next'

defineProps<{ etiqueta: string; opciones: readonly string[] }>()
const modelo = defineModel<string[]>({ required: true })
const emit = defineEmits<{ cambio: [] }>()
const abierto = ref(false)
const raiz = ref<HTMLElement | null>(null)
const boton = ref<HTMLButtonElement | null>(null)
const id = useId()
onClickOutside(raiz, () => (abierto.value = false))

const resumen = computed(() => (modelo.value.length === 0 ? 'Todas' : modelo.value.length === 1 ? modelo.value[0] : `${modelo.value.length} seleccionadas`))
function alternar(o: string) {
  modelo.value = modelo.value.includes(o) ? modelo.value.filter((x) => x !== o) : [...modelo.value, o]
  emit('cambio')
}
function limpiar() {
  modelo.value = []
  emit('cambio')
}
function tecla(e: KeyboardEvent) {
  if (e.key === 'Escape' && abierto.value) { e.stopPropagation(); abierto.value = false; boton.value?.focus() }
}
</script>

<template>
  <div ref="raiz" class="relative" @keydown="tecla">
    <span :id="`${id}-e`" class="etiqueta mb-2 block !text-tinta">{{ etiqueta }}</span>
    <button ref="boton" type="button" class="campo flex items-center justify-between gap-2 text-left text-sm" :aria-expanded="abierto" :aria-controls="id" :aria-labelledby="`${id}-e ${id}-v`" @click="abierto = !abierto">
      <span :id="`${id}-v`" :class="['truncate', modelo.length ? 'text-tinta' : 'text-apagado']">{{ resumen }}</span>
      <ChevronDown :class="['h-4 w-4 shrink-0 text-tenue transition-transform', abierto ? 'rotate-180' : '']" aria-hidden="true" />
    </button>
    <div v-show="abierto" :id="id" role="group" :aria-labelledby="`${id}-e`" class="absolute inset-x-0 top-full z-30 mt-1 max-h-72 overflow-y-auto border border-linea bg-papel py-2 shadow-menu">
      <label v-for="o in opciones" :key="o" class="flex cursor-pointer items-center gap-3 px-4 py-2 text-sm text-cuerpo transition-colors hover:bg-superficie">
        <input type="checkbox" class="h-4 w-4 shrink-0" :checked="modelo.includes(o)" @change="alternar(o)" />
        {{ o }}
      </label>
      <button v-if="modelo.length" type="button" class="mx-4 mb-1 mt-2 text-xs font-bold uppercase tracking-maquinado text-acento-texto" @click="limpiar">Quitar selección</button>
    </div>
  </div>
</template>
