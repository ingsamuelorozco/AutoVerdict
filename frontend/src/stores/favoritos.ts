import { defineStore } from 'pinia'

const CLAVE = 'av-favoritos'
const CLAVE_RECIENTES = 'av-recientes'

function leer(clave: string): number[] {
  try {
    const v = JSON.parse(localStorage.getItem(clave) || '[]')
    return Array.isArray(v) ? v : []
  } catch {
    return []
  }
}

function escribir(clave: string, v: number[]) {
  try {
    localStorage.setItem(clave, JSON.stringify(v))
  } catch {
    /* sin almacenamiento */
  }
}

export const useFavoritos = defineStore('favoritos', {
  state: () => ({ ids: leer(CLAVE), recientes: leer(CLAVE_RECIENTES) }),
  getters: { es: (s) => (id: number) => s.ids.includes(id) },
  actions: {
    alternar(id: number) {
      this.ids = this.ids.includes(id) ? this.ids.filter((x) => x !== id) : [...this.ids, id]
      escribir(CLAVE, this.ids)
    },
    visto(id: number) {
      this.recientes = [id, ...this.recientes.filter((x) => x !== id)].slice(0, 12)
      escribir(CLAVE_RECIENTES, this.recientes)
    },
  },
})
