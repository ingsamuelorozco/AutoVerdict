<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useHead } from '@unhead/vue'
import { api } from '@/lib/api'
import { useAjustes } from '@/stores/ajustes'
import { useFormato } from '@/composables/useFormato'
import SelectorCascada from '@/components/SelectorCascada.vue'
import BarraFinanciera from '@/components/BarraFinanciera.vue'
import BarraApilada from '@/components/BarraApilada.vue'
import BadgeEstimado from '@/components/BadgeEstimado.vue'

useHead({ title: 'Costo total de propiedad' })
const route = useRoute()
const aj = useAjustes()
const f = useFormato()
const vid = ref<number | null>(null)
const otroId = ref<number | null>(null)
const e = ref({ anios: 5, km: 15000, mezcla: 60, casa: 80, financiar: false })
const r = ref<any>(null)
onMounted(() => { if (route.query.id) vid.value = Number(route.query.id) })
watch([vid, otroId, e, () => aj.ciudad], async () => {
  if (!vid.value) return
  r.value = await api.post('/financiero/tco', { vehiculo_id: vid.value, anios: e.value.anios, km_anio: e.value.km, mezcla_ciudad: e.value.mezcla / 100,
    ciudad: aj.ciudad, carga_casa_pct: e.value.casa / 100, financiar: e.value.financiar, comparar_con_id: otroId.value })
}, { deep: true })
const comp = computed(() => (r.value ? { ...r.value.componentes_cop, tramites: r.value.tramites_iniciales_cop, depreciacion: r.value.depreciacion_cop } : {}))
</script>

<template>
  <BarraFinanciera />
  <div class="contenedor py-10">
    <h1 class="text-4xl font-semibold">Costo total de propiedad</h1>
    <p class="mt-2 text-tenue">Combustible o energía, mantenimiento, seguro, SOAT, impuesto, revisión técnico-mecánica e intereses, menos lo que recuperas al vender. <BadgeEstimado /></p>
    <div class="mt-8 grid gap-8 lg:grid-cols-[22rem_1fr]">
      <div class="tarjeta grid content-start gap-4 p-5 text-sm">
        <p class="etiqueta">Vehículo</p>
        <SelectorCascada @elegido="vid = $event" />
        <label>Horizonte: <strong class="num">{{ e.anios }} años</strong><input v-model.number="e.anios" type="range" min="1" max="10" class="w-full" /></label>
        <label>Kilómetros al año<input v-model.number="e.km" type="number" min="1000" max="100000" step="1000" class="campo mt-1 num" /></label>
        <label>Mezcla ciudad: <strong class="num">{{ e.mezcla }}%</strong><input v-model.number="e.mezcla" type="range" min="0" max="100" step="10" class="w-full" /></label>
        <label>Carga en casa (eléctricos e híbridos enchufables): <strong class="num">{{ e.casa }}%</strong><input v-model.number="e.casa" type="range" min="0" max="100" step="10" class="w-full" /></label>
        <label class="flex items-center gap-2"><input v-model="e.financiar" type="checkbox" class="h-4 w-4" /> Lo compro financiado (30% de cuota inicial)</label>
        <details class="rounded-xl border border-linea p-3"><summary class="cursor-pointer">Punto de equilibrio contra otro vehículo</summary><div class="mt-3"><SelectorCascada @elegido="otroId = $event" /></div></details>
      </div>
      <div v-if="r" class="grid content-start gap-6" aria-live="polite">
        <div class="tarjeta grid gap-4 p-6 sm:grid-cols-3">
          <div><p class="etiqueta">Costo total neto a {{ r.anios }} años</p><p class="font-titulo text-4xl font-semibold num">{{ f.dinero(r.costo_total_neto_cop) }}</p></div>
          <div><p class="etiqueta">Por mes</p><p class="text-2xl font-semibold num">{{ f.dinero(r.costo_por_mes_cop) }}</p></div>
          <div><p class="etiqueta">Por kilómetro</p><p class="text-2xl font-semibold num">{{ f.dinero(r.costo_por_km_cop) }}</p></div>
          <p class="text-sm text-tenue sm:col-span-3 num">Precio {{ f.dinero(r.precio_base_cop) }} · reventa estimada {{ f.dinero(r.valor_reventa_cop) }} · energía {{ f.dinero(r.energia.costo_1000km_cop) }} cada 1.000 km</p>
        </div>
        <div class="tarjeta p-6"><BarraApilada :componentes="comp" :formato="f.dinero" titulo="Componentes del costo total" /></div>
        <div v-if="r.punto_equilibrio" class="tarjeta p-6">
          <h2 class="text-xl font-semibold">Punto de equilibrio</h2>
          <p class="mt-2">Diferencia de precio <strong class="num">{{ f.dinero(r.punto_equilibrio.diferencia_precio_cop) }}</strong> · ahorro anual en energía y mantenimiento <strong class="num">{{ f.dinero(r.punto_equilibrio.ahorro_anual_cop) }}</strong>.</p>
          <p class="mt-1 text-lg font-semibold">{{ r.punto_equilibrio.anios_equilibrio === null ? 'No se recupera la diferencia con estos supuestos.' : r.punto_equilibrio.anios_equilibrio === 0 ? 'El primero ya es más barato desde el inicio.' : `Se paga en ${f.numero(r.punto_equilibrio.anios_equilibrio, 1)} años (≈ ${f.numero(r.punto_equilibrio.km_equilibrio)} km).` }}</p>
        </div>
        <div class="tarjeta overflow-x-auto p-6">
          <h2 class="text-xl font-semibold">Año a año</h2>
          <table class="mt-3 w-full min-w-[640px] text-sm num">
            <thead><tr class="text-right text-tenue"><th class="text-left font-normal">Año</th><th class="font-normal">Energía</th><th class="font-normal">Mant.</th><th class="font-normal">Seguro</th><th class="font-normal">SOAT</th><th class="font-normal">Impuesto</th><th class="font-normal">RTM</th></tr></thead>
            <tbody><tr v-for="a in r.por_anio" :key="a.anio" class="border-t border-linea text-right"><td class="py-1 text-left">{{ a.anio }}</td><td>{{ f.cop(a.combustible) }}</td><td>{{ f.cop(a.mantenimiento) }}</td><td>{{ f.cop(a.seguro) }}</td><td>{{ f.cop(a.soat) }}</td><td>{{ f.cop(a.impuesto) }}</td><td>{{ f.cop(a.tecnomecanica) }}</td></tr></tbody>
          </table>
        </div>
      </div>
      <p v-else class="text-tenue">Elige un vehículo para calcular.</p>
    </div>
  </div>
</template>
