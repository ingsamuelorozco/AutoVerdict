import { defineStore } from 'pinia'

export const MAX_COMPARAR = 10
const CLAVE = 'av-comparador'

function leer(): number[] {
  try {
    const v = JSON.parse(localStorage.getItem(CLAVE) || '[]')
    return Array.isArray(v) ? v.filter((x) => Number.isInteger(x)).slice(0, MAX_COMPARAR) : []
  } catch {
    return []
  }
}

export const useComparador = defineStore('comparador', {
  state: () => ({ ids: leer() as number[], referencia: null as number | null }),
  getters: {
    lleno: (s) => s.ids.length >= MAX_COMPARAR,
    tiene: (s) => (id: number) => s.ids.includes(id),
  },
  actions: {
    persistir() {
      try {
        localStorage.setItem(CLAVE, JSON.stringify(this.ids))
      } catch {
        /* sin almacenamiento */
      }
    },
    agregar(id: number): boolean {
      if (this.ids.includes(id) || this.ids.length >= MAX_COMPARAR) return false
      this.ids.push(id)
      this.persistir()
      return true
    },
    quitar(id: number) {
      this.ids = this.ids.filter((x) => x !== id)
      if (this.referencia === id) this.referencia = null
      this.persistir()
    },
    alternar(id: number) {
      if (this.ids.includes(id)) this.quitar(id)
      else this.agregar(id)
    },
    reemplazar(ids: number[]) {
      this.ids = [...new Set(ids)].slice(0, MAX_COMPARAR)
      this.persistir()
    },
    vaciar() {
      this.ids = []
      this.referencia = null
      this.persistir()
    },
  },
})
