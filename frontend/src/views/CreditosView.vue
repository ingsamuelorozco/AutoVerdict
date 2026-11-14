<script setup lang="ts">
import { onMounted } from 'vue'
import { useHead } from '@unhead/vue'
import { api } from '@/lib/api'
import { useCarga } from '@/composables/useCarga'
import EstadoCarga from '@/components/EstadoCarga.vue'

useHead({ title: 'Créditos de fotos' })
interface Img { id: string; url: string; autor: string; licencia: string; url_origen: string; proveedor: string; descripcion: string }
const { datos, cargando, error, ejecutar } = useCarga(() => api.get<Img[]>('/config/imagenes'))
onMounted(ejecutar)
</script>

<template>
  <div class="contenedor pagina">
    <h1 class="titulo-pagina">Créditos de fotos</h1>
    <p class="entradilla">Usamos solo imágenes de Unsplash, Pexels o Wikimedia Commons, revisadas para que no muestren emblemas, logos ni placas legibles. Las fichas usan siluetas generadas a escala mientras no tengamos una foto verificada del modelo exacto.</p>
    <EstadoCarga :cargando="cargando" :error="error" @reintentar="ejecutar">
      <ul class="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <li v-for="i in datos" :key="i.id" class="tarjeta overflow-hidden">
          <img :src="i.url" :alt="i.descripcion" loading="lazy" decoding="async" class="aspect-[16/9] w-full object-cover" />
          <p class="p-6 text-sm"><strong>{{ i.descripcion }}</strong><br />Autor: {{ i.autor }} · Licencia: {{ i.licencia }} · {{ i.proveedor }}<br /><a :href="i.url_origen" class="underline" target="_blank" rel="noopener">Ver original</a></p>
        </li>
      </ul>
    </EstadoCarga>
  </div>
</template>
