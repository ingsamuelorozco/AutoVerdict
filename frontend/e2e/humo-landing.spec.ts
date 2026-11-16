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
