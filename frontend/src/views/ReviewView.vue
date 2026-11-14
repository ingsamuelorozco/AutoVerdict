<script setup lang="ts">
import { computed, onMounted, watch } from 'vue'
import { useHead } from '@unhead/vue'
import { Bug, Check, X } from 'lucide-vue-next'
import { api } from '@/lib/api'
import { useCarga } from '@/composables/useCarga'
import { useFormato } from '@/composables/useFormato'
import { useComparador } from '@/stores/comparador'
import { T } from '@/lib/textos'
import EstadoCarga from '@/components/EstadoCarga.vue'
import MedidorFiabilidad from '@/components/MedidorFiabilidad.vue'
import AlertaBanner from '@/components/AlertaBanner.vue'
import BadgeEstimado from '@/components/BadgeEstimado.vue'
import TarjetaVehiculo from '@/components/TarjetaVehiculo.vue'

const props = defineProps<{ slug: string }>()
const f = useFormato()
const comp = useComparador()
const { datos: d, cargando, error, ejecutar } = useCarga(() => api.get<any>(`/fiabilidad/${props.slug}`))
onMounted(ejecutar)
watch(() => props.slug, ejecutar)
useHead(() => ({ title: d.value ? `Review honesta: ${d.value.vehiculo.marca} ${d.value.vehiculo.modelo} ${d.value.vehiculo.anio}` : 'Review',
  meta: [{ property: 'og:description', content: d.value?.veredicto_honesto?.slice(0, 160) || '' }] }))

const NOMBRES: Record<string, string> = { motor_transmision: 'Motor y transmisión', quejas_documentadas: 'Quejas documentadas', repuestos_y_red: 'Repuestos y red', recalls: 'Recalls', costo_reparaciones: 'Costo de reparaciones', electrica_electronica: 'Eléctrica y electrónica' }
const SEV = { Crítica: 'bg-roja text-white', Alta: 'bg-roja/15 text-roja', Media: 'bg-ambar/15 text-ambar', Baja: 'bg-linea' } as Record<string, string>
const issue = computed(() => {
  if (!d.value) return T.repo
  const v = d.value.vehiculo
  const titulo = encodeURIComponent(`Error en dato: ${v.marca} ${v.modelo} ${v.anio} ${v.version}`)
  const cuerpo = encodeURIComponent(`**Vehículo:** ${v.slug}\n**URL:** ${location.href}\n\n**Dato con error:**\n\n**Valor correcto:**\n\n**Fuente pública que lo respalda (enlace):**\n`)
  return `${T.repo}/issues/new?title=${titulo}&body=${cuerpo}&labels=dato`
})
</script>

<template>
  <div class="contenedor py-10">
    <EstadoCarga :cargando="cargando && !d" :error="error" @reintentar="ejecutar">
      <template v-if="d">
        <p class="etiqueta">Review honesta · Opinión editorial basada en fuentes</p>
        <h1 class="mt-2 text-4xl font-semibold">{{ d.vehiculo.marca }} {{ d.vehiculo.modelo }} {{ d.vehiculo.anio }}</h1>
        <p class="text-lg text-tenue">{{ d.vehiculo.version }}</p>
        <AlertaBanner class="mt-6" :alertas="d.alertas" />

        <section class="mt-8 grid gap-6 lg:grid-cols-[auto_1fr]" aria-labelledby="medidor">
          <div class="tarjeta flex flex-col items-center p-6"><h2 id="medidor" class="sr-only">Medidor de fiabilidad</h2><MedidorFiabilidad :puntaje="d.puntaje_fiabilidad" :etiqueta="d.etiqueta" :tamano="220" /></div>
          <div class="tarjeta p-6">
            <h2 class="text-xl font-semibold">Desglose del puntaje</h2>
            <ul class="mt-4 grid gap-3">
              <li v-for="(peso, k) in d.pesos" :key="k" class="grid grid-cols-[10rem_1fr_3rem] items-center gap-3 text-sm">
                <span>{{ NOMBRES[k] }} <span class="text-xs text-tenue">({{ Math.round(Number(peso) * 100) }}%)</span></span>
                <span class="h-3 overflow-hidden rounded-full bg-linea" role="meter" :aria-valuenow="d.desglose[k]" aria-valuemin="1" aria-valuemax="10" :aria-label="NOMBRES[k]">
                  <span class="block h-full rounded-full bg-tinta" :style="{ width: `${d.desglose[k] * 10}%` }" />
                </span>
                <span class="text-right font-semibold num">{{ f.numero(d.desglose[k], 1) }}</span>
              </li>
            </ul>
            <p class="mt-3 text-xs text-tenue">Fórmula publicada en <RouterLink to="/metodologia" class="underline">metodología</RouterLink>. Una alerta roja limita el puntaje máximo a 4,0.</p>
          </div>
        </section>

        <section class="tarjeta mt-6 grid gap-4 p-6 md:grid-cols-4" aria-labelledby="costos">
          <h2 id="costos" class="text-xl font-semibold md:col-span-4">Costos y valor <BadgeEstimado /></h2>
          <div><p class="etiqueta">Mantenimiento</p><p class="text-lg font-semibold">{{ d.costos.nivel_costo_mantenimiento }}</p><p class="text-xs text-tenue">Repuestos: disponibilidad {{ d.costos.disponibilidad_repuestos }}</p></div>
          <div><p class="etiqueta">Primeros 60.000 km</p><p class="text-lg font-semibold num">{{ f.dinero(d.costos.costo_primeros_60000km_cop) }}</p></div>
          <div><p class="etiqueta">Por año</p><p class="text-lg font-semibold num">{{ f.dinero(d.costos.costo_mantenimiento_anual_cop) }}</p></div>
          <div><p class="etiqueta">Retención de valor</p><p class="text-sm num">1 año {{ Math.round(d.costos.retencion_valor['1'] * 100) }}% · 3 {{ Math.round(d.costos.retencion_valor['3'] * 100) }}% · 5 {{ Math.round(d.costos.retencion_valor['5'] * 100) }}% · 7 {{ Math.round(d.costos.retencion_valor['7'] * 100) }}%</p><p class="text-xs text-tenue">{{ d.costos.depreciacion_estimada }}</p></div>
        </section>

        <section class="mt-8 max-w-3xl" aria-labelledby="veredicto">
          <h2 id="veredicto" class="text-2xl font-semibold">Veredicto honesto</h2>
          <p class="mt-3 text-lg leading-relaxed">{{ d.veredicto_honesto }}</p>
        </section>

        <section class="mt-8 grid gap-4 md:grid-cols-2">
          <div class="tarjeta border-mejor/40 p-5"><h2 class="flex items-center gap-2 font-semibold"><Check class="h-5 w-5 text-mejor" aria-hidden="true" /> Para quién sí</h2><p class="mt-2">{{ d.para_quien_si }}</p></div>
          <div class="tarjeta border-roja/40 p-5"><h2 class="flex items-center gap-2 font-semibold"><X class="h-5 w-5 text-roja" aria-hidden="true" /> Para quién no</h2><p class="mt-2">{{ d.para_quien_no }}</p></div>
        </section>

        <section class="mt-8" aria-labelledby="pros"><h2 id="pros" class="text-2xl font-semibold">Pros reales</h2>
          <ul class="mt-3 grid gap-2 sm:grid-cols-3"><li v-for="p in d.pros_reales" :key="p" class="tarjeta flex gap-2 p-4 text-sm"><Check class="h-4 w-4 shrink-0 text-mejor" aria-hidden="true" />{{ p }}</li></ul>
        </section>

        <section class="mt-8" aria-labelledby="fallas">
          <h2 id="fallas" class="text-2xl font-semibold">Fallas conocidas y contras</h2>
          <div class="mt-3 overflow-x-auto">
            <table class="w-full min-w-[640px] text-sm">
              <thead><tr class="text-left text-tenue"><th class="py-2 font-normal">Componente</th><th class="font-normal">Severidad</th><th class="font-normal">Km típico</th><th class="text-right font-normal">Reparación aprox.</th><th class="font-normal">Fuente</th></tr></thead>
              <tbody>
                <tr v-for="fa in d.fallas_comunes_y_contras" :key="fa.componente" class="border-t border-linea align-top">
                  <td class="py-3 pr-3"><strong>{{ fa.componente }}</strong><p class="text-tenue">{{ fa.descripcion }}</p><p class="text-xs text-tenue">{{ fa.tipo === 'documentada' ? 'Documentada con fuentes' : 'Opinión editorial' }}</p></td>
                  <td class="py-3"><span :class="['rounded-full px-2 py-0.5 text-xs font-semibold', SEV[fa.severidad]]">{{ fa.severidad }}</span></td>
                  <td class="py-3 num">{{ fa.km_tipico }}</td>
                  <td class="py-3 text-right num">{{ fa.costo_reparacion_cop_aprox ? f.dinero(fa.costo_reparacion_cop_aprox) : '—' }}</td>
                  <td class="py-3 pl-3 text-xs"><a v-for="s in fa.fuentes.filter(Boolean)" :key="s.id" :href="s.url" target="_blank" rel="noopener" class="block underline">{{ s.titulo.slice(0, 60) }}{{ s.titulo.length > 60 ? '…' : '' }}</a></td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <section class="mt-8" aria-labelledby="recalls">
          <h2 id="recalls" class="text-2xl font-semibold">Recalls y campañas de seguridad</h2>
          <p v-if="!d.recalls.length" class="mt-2 text-sm text-tenue">No registramos campañas para este modelo y año. Verifica siempre por VIN en el portal de la SIC.</p>
          <ul class="mt-3 grid gap-2">
            <li v-for="r in d.recalls" :key="r.id" class="tarjeta p-4 text-sm"><strong>{{ r.titulo }}</strong> · {{ r.ente }} · {{ r.estado }}<p class="mt-1 text-tenue">{{ r.descripcion }}</p>
              <a v-for="s in r.fuentes.filter(Boolean)" :key="s.id" :href="s.url" target="_blank" rel="noopener" class="mr-3 text-xs underline">{{ s.titulo.slice(0, 50) }}…</a></li>
          </ul>
        </section>

        <section class="mt-8" aria-labelledby="checklist">
          <h2 id="checklist" class="text-2xl font-semibold">Checklist de inspección para comprar usado</h2>
          <ol class="mt-3 grid gap-3">
            <li v-for="(c, i) in d.checklist_usado" :key="i" class="tarjeta p-4 text-sm">
              <label class="flex gap-3"><input type="checkbox" class="mt-1 h-4 w-4 shrink-0" /><span><strong>{{ c.componente }}</strong> ({{ c.severidad }}, {{ c.km_tipico }})
                <span class="mt-1 block"><em>Qué revisar:</em> {{ c.que_revisar }}</span>
                <span class="block"><em>Qué preguntar:</em> {{ c.que_preguntar }}</span>
                <span class="block"><em>Prueba de manejo:</em> {{ c.prueba_de_manejo }}</span></span></label>
            </li>
          </ol>
        </section>

        <section v-if="d.alternativas.length" class="mt-8" aria-labelledby="alternativas">
          <h2 id="alternativas" class="text-2xl font-semibold">Alternativas mejores</h2>
          <div class="mt-3 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <div v-for="a in d.alternativas" :key="a.id" class="grid gap-2">
              <TarjetaVehiculo :v="a" />
              <button class="boton-secundario" @click="comp.agregar(d.vehiculo.id); comp.agregar(a.id); $router.push({ path: '/comparador', query: { ids: comp.ids.join(',') } })">Comparar</button>
            </div>
          </div>
        </section>

        <section class="mt-10 text-sm" aria-labelledby="fuentes">
          <h2 id="fuentes" class="text-lg font-semibold">Fuentes y fecha</h2>
          <p class="text-tenue">Última verificación: {{ f.fecha(d.ultima_verificacion) }}</p>
          <ul class="mt-2 grid gap-1"><li v-for="s in d.fuentes.filter(Boolean)" :key="s.id"><a :href="s.url" target="_blank" rel="noopener" class="underline">{{ s.titulo }}</a> <span class="text-tenue">({{ s.tipo }})</span></li></ul>
          <a :href="issue" target="_blank" rel="noopener" class="boton-secundario mt-4"><Bug class="h-4 w-4" aria-hidden="true" /> Reportar un error en este dato</a>
          <p class="mt-4 text-xs text-tenue">{{ d.aviso_legal }}</p>
        </section>
      </template>
    </EstadoCarga>
  </div>
</template>
