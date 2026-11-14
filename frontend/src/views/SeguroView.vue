<script setup lang="ts">
import { ref, watch } from 'vue'
import { useHead } from '@unhead/vue'
import { api } from '@/lib/api'
import { useAjustes } from '@/stores/ajustes'
import { useFormato } from '@/composables/useFormato'
import SelectorCascada from '@/components/SelectorCascada.vue'
import BarraFinanciera from '@/components/BarraFinanciera.vue'

useHead({ title: 'Seguro estimado' })
const aj = useAjustes()
const f = useFormato()
const vid = ref<number | null>(null)
const e = ref({ edad: '36-55', uso: 'particular', antiguedad: 0, deducible: '1' })
const r = ref<any>(null)
watch([vid, e, () => aj.ciudad], async () => {
  if (!vid.value) return
  r.value = await api.post('/financiero/seguro', { vehiculo_id: vid.value, ciudad: aj.ciudad, edad_conductor: e.value.edad, uso: e.value.uso, antiguedad_anios: e.value.antiguedad, deducible: e.value.deducible })
}, { deep: true })
const NOMBRES: Record<string, string> = { ciudad: 'Ciudad', edad_conductor: 'Edad del conductor', uso: 'Uso', antiguedad: 'Antigüedad', riesgo_hurto: 'Riesgo de hurto del modelo', deducible: 'Deducible', electrificado: 'Electrificado' }
</script>

<template>
  <BarraFinanciera />
  <div class="contenedor py-10">
    <h1 class="text-4xl font-semibold">Seguro estimado</h1>
    <p class="mt-2 text-tenue">SOAT con la tarifa oficial vigente y un rango orientativo del seguro todo riesgo. <strong>Estimación orientativa; solicita cotizaciones reales.</strong></p>
    <div class="mt-8 grid gap-8 lg:grid-cols-[22rem_1fr]">
      <div class="tarjeta grid content-start gap-4 p-5 text-sm">
        <SelectorCascada @elegido="vid = $event" />
        <label>Edad del conductor<select v-model="e.edad" class="campo mt-1"><option v-for="x in ['18-25', '26-35', '36-55', '56+']" :key="x">{{ x }}</option></select></label>
        <label>Uso<select v-model="e.uso" class="campo mt-1"><option value="particular">Particular</option><option value="trabajo">Trabajo</option></select></label>
        <label>Antigüedad del vehículo (años)<input v-model.number="e.antiguedad" type="number" min="0" max="30" class="campo mt-1 num" /></label>
        <label>Deducible (SMMLV)<select v-model="e.deducible" class="campo mt-1"><option v-for="x in ['0', '1', '3', '10']" :key="x" :value="x">{{ x }}</option></select></label>
      </div>
      <div v-if="r" class="grid content-start gap-6" aria-live="polite">
        <div class="tarjeta p-6">
          <p class="etiqueta">Todo riesgo anual</p>
          <p class="font-titulo text-4xl font-semibold num">{{ f.dinero(r.prima_anual_min_cop) }} – {{ f.dinero(r.prima_anual_max_cop) }}</p>
          <p class="text-sm text-tenue num">Valor central {{ f.dinero(r.prima_anual_central_cop) }} · Valor asegurado {{ f.dinero(r.valor_asegurado_cop) }} · tasa base {{ f.pct(r.tasa_base) }}</p>
          <ul class="mt-4 grid gap-1 text-sm sm:grid-cols-2"><li v-for="(v, k) in r.factores" :key="k" class="flex justify-between"><span class="text-tenue">{{ NOMBRES[k] || k }}</span><span class="num">× {{ f.numero(v, 2) }}</span></li></ul>
          <p class="mt-3 text-xs text-tenue">{{ r.aviso }} Parámetros consultados el {{ f.fecha(r.fecha_consulta) }}.</p>
        </div>
        <div v-if="r.soat" class="tarjeta p-6">
          <p class="etiqueta">SOAT ({{ r.soat.clase }}, {{ r.soat.rango_cc }})</p>
          <p class="text-3xl font-semibold num">{{ f.dinero(r.soat.total_cop) }}</p>
          <p class="text-sm text-tenue num">Prima {{ f.cop(r.soat.prima_cop) }} + contribución ADRES {{ f.cop(r.soat.contribucion_adres_cop) }} + tasa RUNT {{ f.cop(r.soat.tasa_runt_cop) }}<span v-if="r.soat.descuento_bev_cop"> · descuento eléctricos {{ f.cop(r.soat.descuento_bev_cop) }}</span></p>
          <p class="mt-2 text-xs text-tenue">{{ r.soat.nota }} Vigencia {{ r.soat.vigencia }}. <a :href="r.soat.fuente_url" class="underline" target="_blank" rel="noopener">Fuente</a></p>
        </div>
      </div>
      <p v-else class="text-tenue">Elige un vehículo para ver el estimado.</p>
    </div>
  </div>
</template>
