<script setup lang="ts">
import { onMounted, ref, useId, watch } from 'vue'
import { api } from '@/lib/api'
import { formatoCOP } from '@/composables/useFormato'

const emit = defineEmits<{ elegido: [id: number] }>()
const marcas = ref<{ marca: string; versiones: number }[]>([])
const modelos = ref<{ modelo: string }[]>([])
const anios = ref<number[]>([])
const versiones = ref<{ id: number; version: string; precio_base_cop: number; tiene_alerta_roja: boolean }[]>([])
const sel = ref({ marca: '', modelo: '', anio: 0 as number, version: 0 as number })
const filtroMarca = ref('')
const uid = useId()

onMounted(async () => (marcas.value = await api.get('/catalogo/marcas')))
watch(() => sel.value.marca, async (m) => {
  sel.value.modelo = ''; sel.value.anio = 0; sel.value.version = 0; anios.value = []; versiones.value = []
  modelos.value = m ? await api.get('/catalogo/modelos', { marca: m }) : []
})
watch(() => sel.value.modelo, async (m) => {
  sel.value.anio = 0; sel.value.version = 0; versiones.value = []
  anios.value = m ? await api.get('/catalogo/anios', { marca: sel.value.marca, modelo: m }) : []
  if (anios.value.length === 1) sel.value.anio = anios.value[0]
})
watch(() => sel.value.anio, async (a) => {
  sel.value.version = 0
  versiones.value = a ? await api.get('/catalogo/versiones', { marca: sel.value.marca, modelo: sel.value.modelo, anio: a }) : []
})
watch(() => sel.value.version, (v) => { if (v) emit('elegido', v) })
const marcasFiltradas = () => marcas.value.filter((m) => m.marca.toLowerCase().includes(filtroMarca.value.toLowerCase()))
</script>

<template>
  <div class="grid gap-2">
    <label class="text-xs text-tenue">Marca
      <input v-model="filtroMarca" class="campo mt-1" placeholder="Escribe para filtrar…" :list="`marcas-${uid}`" @change="sel.marca = (marcas.find((m) => m.marca.toLowerCase() === filtroMarca.toLowerCase()) || marcasFiltradas()[0])?.marca || ''" />
      <datalist :id="`marcas-${uid}`"><option v-for="m in marcas" :key="m.marca" :value="m.marca" /></datalist>
    </label>
    <label class="text-xs text-tenue">Modelo
      <select v-model="sel.modelo" class="campo mt-1" :disabled="!modelos.length">
        <option value="">Elige el modelo</option>
        <option v-for="m in modelos" :key="m.modelo" :value="m.modelo">{{ m.modelo }}</option>
      </select>
    </label>
    <label class="text-xs text-tenue">Año
      <select v-model.number="sel.anio" class="campo mt-1" :disabled="!anios.length">
        <option :value="0">Elige el año</option>
        <option v-for="a in anios" :key="a" :value="a">{{ a }}</option>
      </select>
    </label>
    <label class="text-xs text-tenue">Versión
      <select v-model.number="sel.version" class="campo mt-1" :disabled="!versiones.length">
        <option :value="0">Elige la versión</option>
        <option v-for="v in versiones" :key="v.id" :value="v.id">{{ v.version }} · {{ formatoCOP(v.precio_base_cop) }}{{ v.tiene_alerta_roja ? ' · ⚠ alerta roja' : '' }}</option>
      </select>
    </label>
  </div>
</template>
