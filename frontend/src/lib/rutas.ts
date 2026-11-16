import type { RouteLocationRaw } from 'vue-router'

/** Enlace a la página de un modelo, con el año que debe abrirse seleccionado. */
export function rutaModelo(marca: string, modelo: string, anio?: number): RouteLocationRaw {
  return { path: '/modelo', query: anio ? { marca, modelo, anio: String(anio) } : { marca, modelo } }
}
