import { describe, expect, it } from 'vitest'
import { formatoCOP, formatoNumero, kmlAKmGal } from './useFormato'

describe('formato es-CO', () => {
  it('usa punto de miles en pesos', () => {
    expect(formatoCOP(125900000).replace(/\s/g, ' ')).toMatch(/125\.900\.000/)
  })
  it('usa coma decimal', () => {
    expect(formatoNumero(12.5, 1)).toBe('12,5')
  })
  it('convierte km/l a km/gal con 3,785 L', () => {
    expect(kmlAKmGal(10)).toBeCloseTo(37.85)
  })
  it('muestra guion para nulos', () => {
    expect(formatoCOP(null)).toBe('—')
  })
})
