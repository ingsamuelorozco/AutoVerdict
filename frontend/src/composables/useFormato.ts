import { computed } from 'vue'
import { useAjustes } from '@/stores/ajustes'

const nf = (opts: Intl.NumberFormatOptions) => new Intl.NumberFormat('es-CO', opts)
const cop = nf({ style: 'currency', currency: 'COP', maximumFractionDigits: 0 })
const usd = nf({ style: 'currency', currency: 'USD', maximumFractionDigits: 0 })
const entero = nf({ maximumFractionDigits: 0 })
const dec1 = nf({ minimumFractionDigits: 1, maximumFractionDigits: 1 })
const pct = nf({ style: 'percent', maximumFractionDigits: 1 })

export const LITROS_POR_GALON = 3.785

export function formatoCOP(v: number | null | undefined): string {
  return v === null || v === undefined ? '—' : cop.format(v)
}
export function formatoUSD(v: number | null | undefined): string {
  return v === null || v === undefined ? '—' : usd.format(v)
}
export function formatoNumero(v: number | null | undefined, decimales = 0): string {
  if (v === null || v === undefined) return '—'
  return decimales === 1 ? dec1.format(v) : decimales === 0 ? entero.format(v) : nf({ maximumFractionDigits: decimales }).format(v)
}
export function formatoPct(v: number | null | undefined): string {
  return v === null || v === undefined ? '—' : pct.format(v)
}
export function formatoMillones(v: number | null | undefined): string {
  return v === null || v === undefined ? '—' : `$${dec1.format(v / 1_000_000)} M`
}
export function formatoFecha(iso: string | null | undefined): string {
  if (!iso) return '—'
  return new Date(`${iso.slice(0, 10)}T12:00:00`).toLocaleDateString('es-CO', { year: 'numeric', month: 'short', day: 'numeric' })
}
export function kmlAKmGal(kml: number | null | undefined): number | null {
  return kml === null || kml === undefined ? null : kml * LITROS_POR_GALON
}

export function useFormato() {
  const ajustes = useAjustes()
  const dinero = (cop: number | null | undefined): string =>
    ajustes.moneda === 'USD' && cop != null ? formatoUSD(cop / ajustes.trm) : formatoCOP(cop)
  const dineroSecundario = (cop: number | null | undefined): string =>
    cop == null ? '' : ajustes.moneda === 'USD' ? formatoCOP(cop) : formatoUSD(cop / ajustes.trm)
  const consumo = (kml: number | null | undefined): string =>
    kml == null ? '—' : ajustes.unidadConsumo === 'kmgal' ? `${formatoNumero(kmlAKmGal(kml))} km/gal` : `${formatoNumero(kml, 1)} km/l`
  return {
    dinero, dineroSecundario, consumo, numero: formatoNumero, pct: formatoPct, fecha: formatoFecha,
    cop: formatoCOP, usd: formatoUSD, millones: formatoMillones, moneda: computed(() => ajustes.moneda),
  }
}
