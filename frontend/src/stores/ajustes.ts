import { defineStore } from 'pinia'
import { api } from '@/lib/api'

type Tema = 'claro' | 'oscuro'
const CLAVE = 'av-ajustes'

function leer(): Record<string, unknown> {
  try {
    return JSON.parse(localStorage.getItem(CLAVE) || '{}')
  } catch {
    return {}
  }
}

export const useAjustes = defineStore('ajustes', {
  state: () => {
    const g = leer()
    return {
      moneda: (g.moneda as 'COP' | 'USD') || 'COP',
      trm: (g.trmManual as number) || 3316.7,
      trmManual: (g.trmManual as number | null) ?? null,
      trmOficial: null as null | { valor: number; vigencia: string; origen: string },
      ciudad: (g.ciudad as string) || 'bogota',
      perfil: (g.perfil as string) || 'familiar',
      unidadConsumo: (g.unidadConsumo as 'kml' | 'kmgal') || 'kml',
      tema: ((g.tema as Tema) || (document.documentElement.classList.contains('dark') ? 'oscuro' : 'claro')) as Tema,
      ciudades: [] as { id: string; nombre: string; altitud_msnm: number }[],
    }
  },
  actions: {
    guardar() {
      try {
        localStorage.setItem(CLAVE, JSON.stringify({ moneda: this.moneda, trmManual: this.trmManual, ciudad: this.ciudad,
          perfil: this.perfil, unidadConsumo: this.unidadConsumo, tema: this.tema }))
      } catch {
        /* almacenamiento no disponible */
      }
    },
    async cargar() {
      try {
        const [trm, cds] = await Promise.all([
          api.get<{ valor: number; vigencia: string; origen: string }>('/config/trm'),
          api.get<{ ciudades: { id: string; nombre: string; altitud_msnm: number }[] }>('/config/ciudades'),
        ])
        this.trmOficial = trm
        if (!this.trmManual) this.trm = trm.valor
        this.ciudades = cds.ciudades.map(({ id, nombre, altitud_msnm }) => ({ id, nombre, altitud_msnm }))
      } catch {
        /* se usan los valores por defecto */
      }
    },
    fijarTrm(valor: number | null) {
      this.trmManual = valor && valor > 1000 ? valor : null
      this.trm = this.trmManual ?? this.trmOficial?.valor ?? this.trm
      this.guardar()
    },
    alternarTema() {
      this.tema = this.tema === 'oscuro' ? 'claro' : 'oscuro'
      document.documentElement.classList.toggle('dark', this.tema === 'oscuro')
      this.guardar()
    },
  },
})
