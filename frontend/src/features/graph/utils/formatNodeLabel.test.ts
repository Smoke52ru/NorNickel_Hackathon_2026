import { describe, expect, it } from 'vitest'
import { formatNodeLabel } from './formatNodeLabel'

describe('formatNodeLabel', () => {
  it('returns short labels unchanged', () => {
    expect(formatNodeLabel('Никель')).toBe('Никель')
    expect(formatNodeLabel('Краткое имя')).toBe('Краткое имя')
  })

  it('wraps long labels into two lines at a word boundary', () => {
    expect(formatNodeLabel('Электролитическое выщелачивание')).toBe(
      'Электролитическое\nвыщелачивание',
    )
  })

  it('wraps at hyphen when no space is closer to the middle', () => {
    expect(formatNodeLabel('сульфат-аммонийный раствор концентрат')).toBe(
      'сульфат-аммонийный\nраствор концентрат',
    )
  })
})
