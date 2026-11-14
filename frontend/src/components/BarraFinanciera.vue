<script setup lang="ts">
import { useAjustes } from '@/stores/ajustes'
import { formatoFecha, formatoNumero } from '@/composables/useFormato'

const aj = useAjustes()
defineProps<{ conDesglose?: boolean }>()
const desglose = defineModel<boolean>('desglose', { default: true })
function trm(e: Event) {
  const v = Number((e.target as HTMLInputElement).value.replace(/\./g, '').replace(',', '.'))
  aj.fijarTrm(Number.isFinite(v) && v > 0 ? v : null)
}
</script>

<template>
  <div class="sticky top-16 z-30 border-b border-linea bg-superficie/95 backdrop-blur no-imprimir">
    <div class="contenedor flex flex-wrap items-center gap-x-4 gap-y-2 py-2 text-sm">
      <div class="flex items-center gap-1" role="group" aria-label="Moneda">
        <button v-for="m in ['COP', 'USD'] as const" :key="m" :aria-pressed="aj.moneda === m" :class="['chip min-h-[32px]', aj.moneda === m ? 'chip-activo' : '']" @click="aj.moneda = m; aj.guardar()">{{ m }}</button>
      </div>
      <label class="flex items-center gap-2">
        <span class="text-tenue">TRM</span>
        <input :value="formatoNumero(aj.trm)" class="w-24 rounded-lg border border-linea bg-papel px-2 py-1 num" inputmode="decimal" aria-label="TRM" @change="trm" />
        <span v-if="aj.trmOficial" class="hidden text-xs text-tenue md:inline">oficial {{ formatoNumero(aj.trmOficial.valor, 2) }} ({{ aj.trmOficial.origen }}, {{ formatoFecha(aj.trmOficial.vigencia.slice(0, 10)) }})</span>
      </label>
      <label class="flex items-center gap-2">
        <span class="text-tenue">Ciudad</span>
        <select v-model="aj.ciudad" class="rounded-lg border border-linea bg-papel px-2 py-1" @change="aj.guardar()">
          <option v-for="c in aj.ciudades" :key="c.id" :value="c.id">{{ c.nombre }} · {{ formatoNumero(c.altitud_msnm) }} msnm</option>
        </select>
      </label>
      <label v-if="conDesglose" class="flex items-center gap-2"><input v-model="desglose" type="checkbox" class="h-4 w-4" /> Desglose legal (SOAT, matrícula, impuesto)</label>
    </div>
  </div>
</template>
