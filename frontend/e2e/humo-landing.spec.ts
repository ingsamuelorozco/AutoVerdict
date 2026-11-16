import { expect, test } from '@playwright/test'

test('el menú Herramientas se abre y se recorre con el teclado', async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 })
  await page.goto('/')
  const disparador = page.getByRole('button', { name: 'Herramientas' })
  await disparador.focus()
  await page.keyboard.press('ArrowDown')
  await expect(page.getByRole('menuitem', { name: 'Simulador de crédito' })).toBeFocused()
  await page.keyboard.press('End')
  await expect(page.getByRole('menuitem', { name: 'Encuentra mi carro' })).toBeFocused()
  await page.keyboard.press('Escape')
  await expect(disparador).toBeFocused()
  await expect(disparador).toHaveAttribute('aria-expanded', 'false')
})

test('el buscador rápido lleva a /buscar con los filtros elegidos', async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 })
  await page.goto('/')
  await page.getByLabel('Carrocería').selectOption('SUV')
  await page.getByLabel('Marca', { exact: true }).selectOption('Mazda')
  await page.getByRole('button', { name: 'Buscar vehículos' }).click()
  await expect(page).toHaveURL(/carroceria=SUV/)
  await expect(page).toHaveURL(/marca=Mazda/)
})

test('la búsqueda agrupa por modelo y el modelo muestra las versiones del año elegido', async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 })
  await page.goto('/buscar?marca=Mazda')
  // Sedán y hatchback son tarjetas distintas; las versiones van dentro.
  await expect(page.getByRole('heading', { name: 'Mazda 2 Sedán', exact: true })).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Mazda 2 Hatchback', exact: true })).toBeVisible()
  await page.getByRole('link', { name: 'Mazda 2 Sedán', exact: true }).click()
  await expect(page.getByRole('heading', { level: 1 })).toContainText('Mazda 2 Sedán')
  const pestanas = page.getByRole('tab')
  await expect(pestanas.first()).toHaveAttribute('aria-selected', 'true')
  const anio = (await pestanas.last().textContent())!.trim()
  await pestanas.last().click()
  await expect(page).toHaveURL(new RegExp(`anio=${anio}`))
  await expect(page.getByText(new RegExp(`(versión|versiones) en ${anio}`))).toBeVisible()
  // La primera etiqueta de cada tarjeta es «Segmento · año».
  for (const etiqueta of await page.locator('article p.etiqueta.truncate').allTextContents()) expect(etiqueta).toContain(anio)
})
