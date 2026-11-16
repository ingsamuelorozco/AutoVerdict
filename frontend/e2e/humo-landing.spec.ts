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
