/** Años del vehículo cuando se tomó el precio; 0 si es precio de vitrina (mismo criterio que el backend). */
export function antiguedadCompra(anio: number, fechaPrecio: string | null | undefined): number {
  if (!fechaPrecio) return 0
  const edad = Number(fechaPrecio.slice(0, 4)) - anio
  return edad >= 2 ? edad : 0
}
export const esUsado = (anio: number, fechaPrecio: string | null | undefined) => antiguedadCompra(anio, fechaPrecio) > 0
