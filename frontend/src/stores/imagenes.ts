import { defineStore } from 'pinia'
import { api } from '@/lib/api'

export interface Imagen { id: string; url: string; autor: string; licencia: string; url_origen: string; uso: string; descripcion: string }

/** Catálogo de imágenes con autor y licencia; se pide una sola vez aunque haya muchas tarjetas en pantalla. */
export const useImagenes = defineStore('imagenes', {
  state: () => ({ porId: {} as Record<string, Imagen>, pedida: false }),
  actions: {
    async cargar() {
      if (this.pedida) return
      this.pedida = true
      try {
        const lista = await api.get<Imagen[]>('/config/imagenes')
        this.porId = Object.fromEntries(lista.map((i) => [i.id, i]))
      } catch {
        this.pedida = false
      }
    },
  },
})
