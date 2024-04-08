import { Model } from '@/Model'

export function getSelectedModel(): string {
  if (typeof window !== 'undefined') {
    const storedModel = localStorage.getItem('selectedModel')
    return storedModel || Model.groq_mistral_8x7b
  } else {
    // Default model
    return Model.groq_mistral_8x7b
  }
}
