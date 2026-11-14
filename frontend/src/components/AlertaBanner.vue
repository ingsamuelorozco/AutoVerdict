<script setup lang="ts">
import { AlertTriangle, ShieldAlert } from 'lucide-vue-next'
import type { Alerta } from '@/lib/tipos'

defineProps<{ alertas: Alerta[]; compacta?: boolean }>()
</script>

<template>
  <div v-if="alertas.length" class="grid gap-2">
    <div
      v-for="a in alertas"
      :key="a.texto"
      :class="[
        'flex items-start gap-4 border border-l-4 border-linea bg-superficie p-4 text-sm',
        a.nivel === 'ROJA' ? 'border-l-roja' : 'border-l-ambar',
      ]"
      role="alert"
    >
      <ShieldAlert v-if="a.nivel === 'ROJA'" class="mt-0.5 h-5 w-5 shrink-0 text-roja" aria-hidden="true" />
      <AlertTriangle v-else class="mt-0.5 h-5 w-5 shrink-0 text-ambar" aria-hidden="true" />
      <div>
        <strong class="mr-1 text-xs uppercase tracking-maquinado">{{ a.nivel === 'ROJA' ? 'Alerta roja' : 'Alerta amarilla' }}.</strong>
        <span :class="compacta ? 'line-clamp-2' : ''">{{ a.texto }}</span>
      </div>
    </div>
  </div>
</template>
