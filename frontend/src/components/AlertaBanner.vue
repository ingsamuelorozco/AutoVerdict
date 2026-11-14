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
        'flex items-start gap-3 rounded-xl border p-3 text-sm',
        a.nivel === 'ROJA' ? 'border-roja/50 bg-roja/10' : 'border-ambar/50 bg-ambar/10',
      ]"
      role="alert"
    >
      <ShieldAlert v-if="a.nivel === 'ROJA'" class="mt-0.5 h-5 w-5 shrink-0 text-roja" aria-hidden="true" />
      <AlertTriangle v-else class="mt-0.5 h-5 w-5 shrink-0 text-ambar" aria-hidden="true" />
      <div>
        <strong class="mr-1 uppercase tracking-wide">{{ a.nivel === 'ROJA' ? 'Alerta roja' : 'Alerta amarilla' }}.</strong>
        <span :class="compacta ? 'line-clamp-2' : ''">{{ a.texto }}</span>
      </div>
    </div>
  </div>
</template>
