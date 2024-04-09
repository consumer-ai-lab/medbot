import { Model } from "./model-enum"


export function getSelectedModel(): string {
  if (typeof window !== 'undefined') {
    const storedModel = localStorage.getItem('selectedModel')
    return storedModel || Model.groq_mistral_8x7b
  } else {
    // Default model
    return Model.groq_mistral_8x7b
  }
}


export function getSelectedEmbeddingModel(): string {
  if (typeof window !== 'undefined') {
    const storedModel = localStorage.getItem('selectedEmbeddingModel')
    return storedModel || Model.groq_mistral_8x7b
  } else {
    // Default model
    return Model.groq_mistral_8x7b
  }
}


export function getSelectedStrategy(): string {
  if (typeof window !== 'undefined') {
    const storedModel = localStorage.getItem('selectedStrategy')
    return storedModel || Model.groq_mistral_8x7b
  } else {
    // Default model
    return Model.groq_mistral_8x7b
  }
}