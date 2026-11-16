<script setup lang="ts">
import { nextTick, ref, useId } from 'vue'
import { onClickOutside } from '@vueuse/core'
import { ChevronRight } from 'lucide-vue-next'

defineProps<{ etiqueta: string; opciones: { to: string; texto: string }[]; activo?: boolean }>()
const abierto = ref(false)
const raiz = ref<HTMLElement | null>(null)
const id = useId()
const panel = ref<HTMLElement | null>(null)
const boton = ref<HTMLButtonElement | null>(null)

let temporizador: ReturnType<typeof setTimeout> | undefined

function abrir() { clearTimeout(temporizador); abierto.value = true }
function cerrar() { clearTimeout(temporizador); abierto.value = false }
/** Solo el ratón abre al pasar por encima; en pantallas táctiles manda el toque. */
function alEntrar(e: PointerEvent) { if (e.pointerType === 'mouse') abrir() }
function alSalir(e: PointerEvent) { if (e.pointerType === 'mouse') temporizador = setTimeout(cerrar, 150) }
onClickOutside(raiz, cerrar)

function items() { return Array.from(panel.value?.querySelectorAll<HTMLElement>('[role="menuitem"]') ?? []) }
async function enfocar(i: number) {
  abrir()
  await nextTick()
  const lista = items()
  lista[(i + lista.length) % lista.length]?.focus()
}
function teclaBoton(e: KeyboardEvent) {
  if (e.key === 'ArrowDown') { e.preventDefault(); enfocar(0) }
  else if (e.key === 'ArrowUp') { e.preventDefault(); enfocar(-1) }
  else if (e.key === 'Escape') cerrar()
}
function teclaPanel(e: KeyboardEvent) {
  const actual = items().indexOf(document.activeElement as HTMLElement)
  if (e.key === 'ArrowDown') { e.preventDefault(); enfocar(actual + 1) }
  else if (e.key === 'ArrowUp') { e.preventDefault(); enfocar(actual - 1) }
  else if (e.key === 'Home') { e.preventDefault(); enfocar(0) }
  else if (e.key === 'End') { e.preventDefault(); enfocar(-1) }
  else if (e.key === 'Escape') { e.preventDefault(); cerrar(); boton.value?.focus() }
  else if (e.key === 'Tab') cerrar()
}
</script>

<template>
  <div ref="raiz" class="relative flex items-stretch" @pointerenter="alEntrar" @pointerleave="alSalir">
    <button ref="boton" type="button" :class="['enlace-barra', { 'enlace-barra-activo': activo || abierto }]" aria-haspopup="menu" :aria-expanded="abierto" :aria-controls="id" @click="abierto ? cerrar() : abrir()" @keydown="teclaBoton">
      {{ etiqueta }}<span class="enlace-barra-mas" aria-hidden="true">+</span>
    </button>
    <ul v-show="abierto" :id="id" ref="panel" class="sobre-claro absolute left-0 top-[calc(100%-10px)] z-50 min-w-[150px] bg-papel py-2.5 shadow-menu" role="menu" :aria-label="etiqueta" @keydown="teclaPanel">
      <li v-for="o in opciones" :key="o.to" role="none">
        <RouterLink :to="o.to" role="menuitem" tabindex="-1" class="flex items-center justify-between gap-6 whitespace-nowrap px-[18px] py-2 text-[13px] font-normal text-cuerpo" @click="cerrar">
          <span>{{ o.texto }}</span>
          <ChevronRight class="h-3.5 w-3.5 shrink-0" aria-hidden="true" />
        </RouterLink>
      </li>
    </ul>
  </div>
</template>
