<script setup lang="ts">
import { ref } from 'vue'
import { useHead } from '@unhead/vue'
import { api } from '@/lib/api'
import { useAjustes } from '@/stores/ajustes'
import { useFormato } from '@/composables/useFormato'
import EstadoCarga from '@/components/EstadoCarga.vue'
import TarjetaVehiculo from '@/components/TarjetaVehiculo.vue'

useHead({ title: '¿Qué carro me alcanza?' })
const aj = useAjustes()
const f = useFormato()
const e = ref({ ingreso: 8_000_000, inicial: 25_000_000, plazo: 60, pct: 30 })
const r = ref<any>(null)
const cargando = ref(false)
const error = ref<string | null>(null)
async function calcular() {
  cargando.value = true; error.value = null
  try {
    r.value = await api.post('/financiero/asequibilidad', { ingreso_mensual_cop: e.value.ingreso, cuota_inicial_cop: e.value.inicial, plazo_meses: e.value.plazo, max_pct_ingreso: e.value.pct / 100, ciudad: aj.ciudad, limite: 30 })
  } catch (x) { error.value = String(x) } finally { cargando.value = false }
}
</script>

<template>
  <div class="contenedor py-10">
    <h1 class="text-4xl font-semibold">¿Qué carro me alcanza?</h1>
    <p class="mt-2 max-w-2xl text-tenue">Sumamos la cuota del crédito, el seguro, el combustible y el mantenimiento. Solo aparecen los carros cuyo costo mensual real cabe en tu presupuesto.</p>
    <form class="tarjeta mt-8 grid gap-4 p-5 text-sm sm:grid-cols-4" @submit.prevent="calcular">
      <label>Ingreso mensual neto (COP)<input v-model.number="e.ingreso" type="number" min="1000000" step="100000" class="campo mt-1 num" required /></label>
      <label>Cuota inicial disponible (COP)<input v-model.number="e.inicial" type="number" min="0" step="500000" class="campo mt-1 num" /></label>
      <label>Plazo (meses)<input v-model.number="e.plazo" type="number" min="12" max="84" step="12" class="campo mt-1 num" /></label>
      <label>Máximo del ingreso para el carro (%)<input v-model.number="e.pct" type="number" min="5" max="60" class="campo mt-1 num" /></label>
      <button class="boton-primario sm:col-span-4">Calcular</button>
    </form>
    <div class="mt-8" aria-live="polite">
      <EstadoCarga :cargando="cargando" :error="error" :vacio="!!r && !r.total" mensaje-vacio="Ningún carro cabe en ese presupuesto. Prueba con más cuota inicial, más plazo o un porcentaje mayor.">
        <template v-if="r">
          <p class="mb-4">Presupuesto mensual para el carro: <strong class="num">{{ f.dinero(r.presupuesto_mensual_cop) }}</strong> · {{ r.total }} opciones. <span class="text-xs text-tenue">{{ r.aviso }}</span></p>
          <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
            <div v-for="v in r.resultados" :key="v.id" class="grid gap-2">
              <TarjetaVehiculo :v="v" />
              <p class="px-2 text-sm num">Costo mensual real <strong>{{ f.dinero(v.costo_mensual_cop) }}</strong> · holgura {{ f.dinero(v.holgura_cop) }}
                <span class="block text-xs text-tenue">Cuota {{ f.cop(v.desglose_mensual.cuota) }} · seguro {{ f.cop(v.desglose_mensual.seguro) }} · energía {{ f.cop(v.desglose_mensual.energia) }} · mant. {{ f.cop(v.desglose_mensual.mantenimiento) }}</span></p>
            </div>
          </div>
        </template>
      </EstadoCarga>
    </div>
  </div>
</template>
