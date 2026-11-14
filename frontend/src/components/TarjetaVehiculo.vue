<script setup lang="ts">
import { computed } from 'vue'
import { Heart, ShieldAlert } from 'lucide-vue-next'
import ImagenVehiculo from './ImagenVehiculo.vue'
import { useFormato } from '@/composables/useFormato'
import { useComparador } from '@/stores/comparador'
import { useFavoritos } from '@/stores/favoritos'
import { T } from '@/lib/textos'
import type { Tarjeta } from '@/lib/tipos'

const props = defineProps<{ v: Tarjeta; lista?: boolean }>()
const f = useFormato()
const comp = useComparador()
const fav = useFavoritos()
const nombre = computed(() => `${props.v.marca} ${props.v.modelo}`)

const datosClave = computed(() => {
  const v = props.v
  const d: { etiqueta: string; valor: string }[] = []
  if (v.tipo_combustible === '100% Eléctrico BEV') d.push({ etiqueta: 'Autonomía', valor: `${f.numero(v.autonomia_estimada_km)} km` })
  else d.push({ etiqueta: 'Consumo real', valor: f.consumo(v.consumo_real_estimado_kml) })
  if (v.carroceria === 'Pickup') d.push({ etiqueta: 'Torque', valor: `${f.numero(v.torque_nm)} Nm` })
  else if (v.segmento === 'Deportivo') d.push({ etiqueta: 'Potencia', valor: `${f.numero(v.potencia_hp)} hp` })
  else d.push({ etiqueta: 'Baúl', valor: `${f.numero(v.capacidad_baul_litros)} L` })
  d.push({ etiqueta: 'Despeje', valor: `${f.numero(v.distancia_libre_suelo_mm)} mm` })
  return d
})
</script>

<template>
  <article :class="['tarjeta group relative flex gap-4 p-3 transition hover:border-tinta/40', lista ? 'flex-row items-center' : 'flex-col']">
    <RouterLink :to="`/vehiculo/${v.slug}`" :class="lista ? 'w-40 shrink-0 sm:w-56' : ''" :aria-label="`Ver ficha de ${nombre} ${v.version}`">
      <ImagenVehiculo :medidas="v" :nombre="nombre" />
    </RouterLink>
    <div class="flex min-w-0 flex-1 flex-col gap-2">
      <div class="flex items-start justify-between gap-2">
        <div class="min-w-0">
          <p class="etiqueta">{{ v.segmento }} · {{ v.anio }}</p>
          <h3 class="truncate text-lg font-semibold">
            <RouterLink :to="`/vehiculo/${v.slug}`" class="hover:underline">{{ nombre }}</RouterLink>
          </h3>
          <p class="truncate text-sm text-tenue">{{ v.version }}</p>
        </div>
        <button
          class="grid h-11 w-11 shrink-0 place-items-center rounded-full hover:bg-linea/50"
          :aria-pressed="fav.es(v.id)"
          :aria-label="fav.es(v.id) ? 'Quitar de favoritos' : 'Agregar a favoritos'"
          @click="fav.alternar(v.id)"
        >
          <Heart :class="['h-5 w-5', fav.es(v.id) ? 'fill-roja text-roja' : '']" aria-hidden="true" />
        </button>
      </div>
      <div class="flex flex-wrap items-baseline gap-x-3 num">
        <span class="text-sm text-tenue">Base {{ f.dinero(v.precio_base_cop) }}</span>
        <span class="font-semibold">En calle {{ f.dinero(v.precio_total_en_calle_cop) }}</span>
      </div>
      <dl class="grid grid-cols-3 gap-2 text-xs">
        <div v-for="d in datosClave" :key="d.etiqueta">
          <dt class="text-tenue">{{ d.etiqueta }}</dt>
          <dd class="font-medium num">{{ d.valor }}</dd>
        </div>
      </dl>
      <div class="mt-auto flex items-center justify-between gap-2 pt-1">
        <RouterLink
          :to="`/reviews/${v.slug}`"
          :class="['inline-flex items-center gap-1 rounded-full px-2 py-1 text-xs font-semibold num',
                   v.tiene_alerta_roja ? 'bg-roja/15 text-roja' : v.puntaje_fiabilidad >= 7 ? 'bg-mejor/15 text-mejor' : 'bg-linea/60']"
          :aria-label="`Fiabilidad ${v.puntaje_fiabilidad} de 10${v.tiene_alerta_roja ? ', con alerta roja' : ''}`"
        >
          <ShieldAlert v-if="v.tiene_alerta_roja" class="h-3.5 w-3.5" aria-hidden="true" />
          Fiabilidad {{ f.numero(v.puntaje_fiabilidad, 1) }}
          <span v-if="v.tiene_alerta_roja">· Alerta roja</span>
        </RouterLink>
        <label class="flex min-h-[44px] cursor-pointer items-center gap-2 text-sm" :title="comp.lleno && !comp.tiene(v.id) ? T.maximo10 : ''">
          <input
            type="checkbox"
            class="h-4 w-4 accent-[rgb(var(--tinta))]"
            :checked="comp.tiene(v.id)"
            :disabled="comp.lleno && !comp.tiene(v.id)"
            @change="comp.alternar(v.id)"
          />
          {{ T.comparar }}
        </label>
      </div>
    </div>
  </article>
</template>
