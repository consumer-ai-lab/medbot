import { Model } from '@/Model'

export function getSelectedModel(): string {
  if (typeof window !== 'undefined') {
    const storedModel = localStorage.getItem('selectedModel')
    return storedModel || Model.gemini_pro
  } else {
    // Default model
    return Model.gemini_pro
  }
}
