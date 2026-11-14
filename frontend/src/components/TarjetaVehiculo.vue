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
  <article :class="['tarjeta group relative flex transition-colors hover:border-tinta', lista ? 'flex-col sm:flex-row' : 'h-full flex-col']">
    <RouterLink :to="`/vehiculo/${v.slug}`" :class="['block shrink-0', lista ? 'sm:w-72' : '']" :aria-label="`Ver ficha de ${nombre} ${v.version}`" tabindex="-1">
      <ImagenVehiculo :medidas="v" :nombre="nombre" />
    </RouterLink>
    <div class="flex min-w-0 flex-1 flex-col p-6">
      <div class="flex items-start justify-between gap-3">
        <div class="min-w-0">
          <p class="etiqueta truncate">{{ v.segmento }} · {{ v.anio }}</p>
          <h3 class="mt-2 truncate text-2xl leading-tight">
            <RouterLink :to="`/vehiculo/${v.slug}`" class="hover:underline">{{ nombre }}</RouterLink>
          </h3>
          <p class="mt-1 truncate text-sm text-tenue">{{ v.version }}</p>
        </div>
        <button
          class="boton-icono -mr-2 -mt-2 h-11 w-11 bg-transparent"
          :aria-pressed="fav.es(v.id)"
          :aria-label="fav.es(v.id) ? 'Quitar de favoritos' : 'Agregar a favoritos'"
          @click="fav.alternar(v.id)"
        >
          <Heart :class="['h-5 w-5', fav.es(v.id) ? 'fill-tinta' : '']" aria-hidden="true" />
        </button>
      </div>

      <div class="mt-5 num">
        <p class="etiqueta">En calle</p>
        <p class="mt-1 text-2xl font-bold leading-tight text-tinta">{{ f.dinero(v.precio_total_en_calle_cop) }}</p>
        <p class="mt-1 text-sm text-tenue">Base {{ f.dinero(v.precio_base_cop) }}</p>
      </div>

      <dl class="mt-5 grid grid-cols-3 gap-4 border-t border-linea pt-4">
        <div v-for="d in datosClave" :key="d.etiqueta" class="min-w-0">
          <dt class="truncate text-xs font-normal tracking-[0.5px] text-tenue">{{ d.etiqueta }}</dt>
          <dd class="mt-1 truncate text-sm font-bold text-tinta num">{{ d.valor }}</dd>
        </div>
      </dl>

      <div class="mt-auto flex flex-wrap items-center justify-between gap-x-3 gap-y-1 pt-5">
        <RouterLink
          :to="`/reviews/${v.slug}`"
          :class="['insignia min-h-[28px] num', v.tiene_alerta_roja ? 'bg-roja text-white' : v.puntaje_fiabilidad >= 7 ? 'border border-mejor text-mejor' : 'border border-linea text-tenue']"
          :aria-label="`Fiabilidad ${v.puntaje_fiabilidad} de 10${v.tiene_alerta_roja ? ', con alerta roja' : ''}`"
        >
          <ShieldAlert v-if="v.tiene_alerta_roja" class="h-3.5 w-3.5" aria-hidden="true" />
          Fiabilidad {{ f.numero(v.puntaje_fiabilidad, 1) }}
          <span v-if="v.tiene_alerta_roja">· Alerta roja</span>
        </RouterLink>
        <label class="flex min-h-[44px] cursor-pointer items-center gap-2 text-xs font-bold uppercase tracking-maquinado text-tinta" :title="comp.lleno && !comp.tiene(v.id) ? T.maximo10 : ''">
          <input
            type="checkbox"
            class="h-4 w-4"
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
