<script setup lang="ts">
import { computed } from 'vue'
import { ArrowRight, ShieldAlert } from 'lucide-vue-next'
import ImagenVehiculo from './ImagenVehiculo.vue'
import { useFormato } from '@/composables/useFormato'
import { rutaModelo } from '@/lib/rutas'
import type { Modelo } from '@/lib/tipos'

/** Tarjeta de un modelo con todas sus versiones dentro: lleva a la página del modelo con el año más reciente. */
const props = defineProps<{ m: Modelo; lista?: boolean }>()
const f = useFormato()
const nombre = computed(() => `${props.m.marca} ${props.m.modelo}`)
const destino = computed(() => rutaModelo(props.m.marca, props.m.modelo, props.m.anios[0]))
const unPrecio = computed(() => props.m.precio_calle_min === props.m.precio_calle_max)
</script>

<template>
  <article :class="['tarjeta group relative flex transition-colors hover:border-tinta', lista ? 'flex-col sm:flex-row' : 'h-full flex-col']">
    <RouterLink :to="destino" :class="['block shrink-0', lista ? 'sm:w-72' : '']" tabindex="-1" aria-hidden="true">
      <ImagenVehiculo :medidas="m.representante" :nombre="nombre" :imagen-id="m.representante.imagen_id" />
    </RouterLink>
    <div class="flex min-w-0 flex-1 flex-col p-6">
      <p class="etiqueta truncate">{{ m.segmento }} · {{ m.carroceria }}</p>
      <h3 class="mt-2 truncate text-2xl leading-tight">
        <!-- El enlace cubre toda la tarjeta para que cualquier clic abra el modelo -->
        <RouterLink :to="destino" class="after:absolute after:inset-0 after:content-['']">{{ nombre }}</RouterLink>
      </h3>
      <p class="mt-1 text-sm text-tenue">
        <span class="num">{{ m.versiones }}</span> {{ m.versiones === 1 ? 'versión' : 'versiones' }} · {{ m.anios.join(' · ') }}
      </p>

      <div class="mt-5 num">
        <p class="etiqueta">{{ unPrecio ? 'En calle' : 'En calle desde' }}</p>
        <p class="mt-1 text-2xl font-bold leading-tight text-tinta">{{ f.dinero(m.precio_calle_min) }}</p>
        <p v-if="!unPrecio" class="mt-1 text-sm text-tenue">hasta {{ f.dinero(m.precio_calle_max) }}</p>
      </div>

      <div class="mt-auto flex flex-wrap items-center justify-between gap-x-3 gap-y-2 border-t border-linea pt-4">
        <span
          :class="['insignia min-h-[28px] num', m.tiene_alerta_roja ? 'bg-roja text-white' : m.puntaje_fiabilidad >= 7 ? 'border border-mejor text-mejor' : 'border border-linea text-tenue']"
        >
          <ShieldAlert v-if="m.tiene_alerta_roja" class="h-3.5 w-3.5" aria-hidden="true" />
          Fiabilidad {{ f.numero(m.puntaje_fiabilidad, 1) }}
          <span v-if="m.tiene_alerta_roja">· Alerta roja</span>
        </span>
        <span class="enlace-texto">Ver versiones <ArrowRight class="h-4 w-4" aria-hidden="true" /></span>
      </div>
    </div>
  </article>
</template>
