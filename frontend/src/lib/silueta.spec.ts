import { describe, expect, it } from 'vitest'
import { desplazamiento, perfilLateral, planta, plantilla } from './silueta'

const m = {
  carroceria: 'SUV', largo_mm: 4500, alto_mm: 1650, distancia_entre_ejes_mm: 2700, distancia_libre_suelo_mm: 200,
  voladizo_delantero_mm: 850, voladizo_trasero_mm: 950, diametro_rueda_mm: 700, ancho_sin_espejos_mm: 1840, ancho_con_espejos_mm: 2050,
}

describe('silueta a escala', () => {
  it('ubica las ruedas sobre el suelo y en los ejes reales', () => {
    const p = perfilLateral(m)
    expect(p.ruedas[0]).toEqual({ cx: 850, cy: 350, r: 350 })
    expect(p.ruedas[1].cx - p.ruedas[0].cx).toBe(2700)
  })
  it('respeta largo y alto', () => {
    const p = perfilLateral(m)
    expect(p.largo).toBe(4500)
    expect(p.cuerpo).toContain('1650')
  })
  it('usa plantilla de sedán si la carrocería es desconocida', () => {
    expect(plantilla('Furgón')).toBe('Sedán')
  })
  it('dibuja espejos hasta el ancho con espejos', () => {
    expect(planta(m).anchoTotal).toBe(2050)
  })
  it('alinea por rueda trasera', () => {
    const otro = { ...m, voladizo_delantero_mm: 900, distancia_entre_ejes_mm: 2600 }
    expect(desplazamiento(otro, 'rueda', 3550)).toBe(50)
    expect(desplazamiento(otro, 'frente', 3550)).toBe(0)
  })
})
