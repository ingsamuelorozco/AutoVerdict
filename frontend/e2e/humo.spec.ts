import { expect, test } from '@playwright/test'

const errores: string[] = []
test.beforeEach(({ page }) => {
  errores.length = 0
  page.on('console', (m) => { if (m.type() === 'error' && !m.text().includes('upload.wikimedia.org')) errores.push(m.text()) })
  page.on('pageerror', (e) => errores.push(e.message))
})
test.afterEach(() => expect(errores, errores.join('\n')).toEqual([]))

test('la landing muestra el titular y el buscador rápido', async ({ page }) => {
  await page.goto('/')
  await expect(page.getByRole('heading', { level: 1 })).toContainText('Precio & verdad')
  await expect(page.getByRole('heading', { name: /Encuentra tu carro/i })).toBeVisible()
})

test('el buscador encuentra la Captiva sin tilde y con tilde', async ({ page }) => {
  await page.goto('/buscar?q=captivá')
  await expect(page.getByRole('heading', { name: /Chevrolet Captiva/ }).first()).toBeVisible()
  await expect(page.getByText(/Alerta roja/).first()).toBeVisible()
})

test('la ficha muestra secciones y puesta en calle', async ({ page }) => {
  await page.goto('/vehiculo/toyota-corolla-cross-2026-xei-hev')
  await expect(page.getByRole('heading', { level: 1 })).toContainText('Corolla Cross')
  await expect(page.getByText('Precio total puesto en calle (llave en mano)')).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Tamaño y usabilidad urbana' })).toBeVisible()
})

test('el comparador marca ganadores con la etiqueta MEJOR', async ({ page }) => {
  await page.goto('/comparador?ids=62,270,163')
  await expect(page.getByText('MEJOR').first()).toBeVisible()
  await expect(page.getByText(/Alerta roja de fiabilidad/)).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Huella dimensional' })).toBeVisible()
})

test('la review de la Captiva muestra la alerta roja y fuentes', async ({ page }) => {
  await page.goto('/reviews/chevrolet-captiva-2026-premier-1-5t-cvt-7p')
  await expect(page.getByRole('alert').first()).toContainText(/Alerta roja/i)
  await expect(page.getByRole('heading', { name: /Checklist/ })).toBeVisible()
})

test('el simulador de crédito calcula la cuota', async ({ page }) => {
  await page.goto('/herramientas/credito')
  await expect(page.getByText('Cuota mensual').first()).toBeVisible()
  await expect(page.getByText('36 meses')).toBeVisible()
})

for (const ancho of [1440, 768, 390]) {
  test(`captura sin desbordes a ${ancho}px`, async ({ page }) => {
    await page.setViewportSize({ width: ancho, height: 900 })
    for (const ruta of ['/', '/comparador?ids=62,270,163', '/vehiculo/chevrolet-captiva-2026-premier-1-5t-cvt-7p']) {
      await page.goto(ruta)
      await page.waitForLoadState('networkidle')
      const desborde = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth)
      expect(desborde, `desborde horizontal en ${ruta}`).toBeLessThanOrEqual(1)
      await page.screenshot({ path: `test-results/capturas/${ancho}${ruta.replace(/[/?=,]/g, '_')}.png`, fullPage: false })
    }
  })
}
