<script setup lang="ts">
import { ref, watch } from 'vue'
import { X } from 'lucide-vue-next'
import { onKeyStroke } from '@vueuse/core'
import { api } from '@/lib/api'
import AlertaBanner from './AlertaBanner.vue'
import MedidorFiabilidad from './MedidorFiabilidad.vue'
import type { Alerta, Falla } from '@/lib/tipos'

const props = defineProps<{ slug: string | null }>()
const emit = defineEmits<{ cerrar: [] }>()
interface Resena { vehiculo: { marca: string; modelo: string; anio: number; version: string; slug: string }; puntaje_fiabilidad: number;
  etiqueta: string; veredicto_honesto: string; alertas: Alerta[]; fallas_comunes_y_contras: Falla[]; pros_reales: string[] }
const datos = ref<Resena | null>(null)
watch(() => props.slug, async (s) => { datos.value = s ? await api.get<Resena>(`/fiabilidad/${s}`) : null }, { immediate: true })
onKeyStroke('Escape', () => props.slug && emit('cerrar'))
</script>

<template>
  <div v-if="slug" class="fixed inset-0 z-50" role="dialog" aria-modal="true" aria-label="Review honesta">
    <div class="absolute inset-0 bg-black/70" @click="emit('cerrar')" />
    <aside class="absolute right-0 top-0 h-full w-[34rem] max-w-full overflow-y-auto border-l border-linea bg-papel p-6 lg:p-10">
      <button class="boton-icono float-right" aria-label="Cerrar" @click="emit('cerrar')"><X class="h-5 w-5" aria-hidden="true" /></button>
      <div v-if="!datos" class="esqueleto mt-12 h-64" />
      <template v-else>
        <p class="etiqueta">Review honesta</p>
        <h2 class="mt-3 text-display-sm">{{ datos.vehiculo.marca }} {{ datos.vehiculo.modelo }} {{ datos.vehiculo.anio }}</h2>
        <p class="mt-2 text-tenue">{{ datos.vehiculo.version }}</p>
        <div class="my-8 flex justify-center border-y border-linea py-6"><MedidorFiabilidad :puntaje="datos.puntaje_fiabilidad" :etiqueta="datos.etiqueta" /></div>
        <AlertaBanner :alertas="datos.alertas" />
        <p class="mt-6 leading-relaxed">{{ datos.veredicto_honesto }}</p>
        <h3 class="etiqueta mt-10">Fallas y contras principales</h3>
        <ul class="mt-4 grid gap-px border border-linea bg-linea text-sm">
          <li v-for="fa in datos.fallas_comunes_y_contras.slice(0, 4)" :key="fa.componente" class="bg-suave p-4">
            <strong>{{ fa.componente }}</strong> · <span class="text-tenue">{{ fa.severidad }}</span>
            <p class="mt-1">{{ fa.descripcion }}</p>
          </li>
        </ul>
        <RouterLink :to="`/reviews/${datos.vehiculo.slug}`" class="boton-primario mt-8 w-full" @click="emit('cerrar')">Ver review completa</RouterLink>
      </template>
    </aside>
  </div>
</template>
