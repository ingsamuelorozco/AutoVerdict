import { defineStore } from 'pinia'
import { api } from '@/lib/api'
import { OPC } from '@/lib/opciones'

/** Marcas del catálogo leídas de la API (una sola petición); mientras llega, la lista fija de respaldo. */
export const useCatalogo = defineStore('catalogo', {
  state: () => ({ marcas: [...OPC.marca] as string[], pedida: false }),
  actions: {
    async cargar() {
      if (this.pedida) return
      this.pedida = true
      try {
        this.marcas = (await api.get<{ marca: string }[]>('/catalogo/marcas')).map((m) => m.marca)
      } catch {
        this.pedida = false
      }
    },
  },
})
