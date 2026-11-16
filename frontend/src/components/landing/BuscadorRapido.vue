<script setup lang="ts">
import { computed, ref } from 'vue'
import { ChevronDown } from 'lucide-vue-next'
import RangoDoble from '@/components/landing/RangoDoble.vue'
import { formatoNumero } from '@/composables/useFormato'
import { OPC } from '@/lib/opciones'
import { useAjustes } from '@/stores/ajustes'
import { T } from '@/lib/textos'

const props = defineProps<{ total?: number | null; marcas?: string[] }>()
const B = T.landing.buscador
const carroceria = ref('')
const marca = ref('')
const ciudad = ref('')
const aj = useAjustes()
/** Rango del precio en calle del catálogo en COP (35 M a 523 M), redondeado a pasos de 5 M. */
const LIMITE = { min: 30_000_000, max: 550_000_000, paso: 5_000_000 }
const rango = ref<[number, number]>([LIMITE.min, LIMITE.max])
const millones = (v: number) => `$${formatoNumero(v / 1_000_000)} M`
const listaMarcas = computed(() => (props.marcas?.length ? props.marcas : OPC.marca))
</script>

<template>
  <section class="relative bg-[linear-gradient(to_bottom,rgb(var(--velo))_0_56px,transparent_56px)] px-4" aria-labelledby="buscador-titulo">
    <form class="mx-auto max-w-[940px] bg-papel px-[35px] dark:bg-superficie pb-[50px] pt-6 shadow-tarjeta" @submit.prevent>
      <div class="flex flex-wrap items-center justify-between gap-4 border-b border-linea pb-5">
        <div class="flex items-baseline gap-4">
          <h2 id="buscador-titulo" class="text-[26px] leading-none">{{ B.titulo }}</h2>
          <RouterLink to="/buscar" class="text-[13px] font-normal text-acento-texto hover:underline">{{ B.avanzada }}</RouterLink>
        </div>
        <p class="text-xl font-bold uppercase leading-none text-tinta"><span class="num text-acento-texto">{{ total ?? '—' }}</span> {{ B.disponibles }}</p>
      </div>
      <div class="mt-6 grid gap-6 md:grid-cols-3">
        <div>
          <label for="bq-carroceria" class="block text-[13px]">{{ B.carroceria }}</label>
          <div class="relative mt-2">
            <select id="bq-carroceria" v-model="carroceria" class="campo-mini w-full appearance-none bg-suave pl-4 pr-9 text-xs" :class="carroceria ? 'text-tinta' : 'text-tenue'">
              <option value="">{{ B.carroceriaVacia }}</option>
              <option v-for="x in OPC.carroceria" :key="x" :value="x">{{ x }}</option>
            </select>
            <ChevronDown class="pointer-events-none absolute right-3 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-tenue" aria-hidden="true" />
          </div>
        </div>
        <div>
          <label for="bq-marca" class="block text-[13px]">{{ B.marca }}</label>
          <div class="relative mt-2">
            <select id="bq-marca" v-model="marca" class="campo-mini w-full appearance-none bg-suave pl-4 pr-9 text-xs" :class="marca ? 'text-tinta' : 'text-tenue'">
              <option value="">{{ B.marcaVacia }}</option>
              <option v-for="x in listaMarcas" :key="x" :value="x">{{ x }}</option>
            </select>
            <ChevronDown class="pointer-events-none absolute right-3 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-tenue" aria-hidden="true" />
          </div>
        </div>
        <div>
          <label for="bq-ciudad" class="block text-[13px]">{{ B.ciudad }}</label>
          <div class="relative mt-2">
            <select id="bq-ciudad" v-model="ciudad" class="campo-mini w-full appearance-none bg-suave pl-4 pr-9 text-xs" :class="ciudad ? 'text-tinta' : 'text-tenue'">
              <option value="">{{ B.ciudadVacia }}</option>
              <option v-for="x in aj.ciudades" :key="x.id" :value="x.id">{{ x.nombre }}</option>
            </select>
            <ChevronDown class="pointer-events-none absolute right-3 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-tenue" aria-hidden="true" />
          </div>
        </div>
      </div>
      <div class="mt-8 grid items-center gap-6">
        <fieldset>
          <legend class="text-[13px] text-tenue">{{ B.precio }}</legend>
          <RangoDoble v-model="rango" class="mt-3" :min="LIMITE.min" :max="LIMITE.max" :paso="LIMITE.paso" :formato="millones" :etiqueta-min="B.precioMin" :etiqueta-max="B.precioMax" />
        </fieldset>
        <button type="submit" class="boton-acento">{{ B.boton }}</button>
      </div>
    </form>
  </section>
</template>
