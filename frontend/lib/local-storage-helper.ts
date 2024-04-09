import { Model } from "./model-enum"
import { EmbeddingModel } from "./embedding-model-enum"
import { Strategy } from "./strategy-enum"


export function getSelectedModel(): string {
  if (typeof window !== 'undefined') {
    const stored = localStorage.getItem('selectedModel')
    return stored || Model.groq_mistral_8x7b
  } else {
    // Default
    return Model.groq_mistral_8x7b
  }
}


export function getSelectedEmbeddingModel(): string {
  if (typeof window !== 'undefined') {
    const stored = localStorage.getItem('selectedEmbeddingModel')
    return stored || EmbeddingModel.gemini_pro
  } else {
    // Default
    return EmbeddingModel.gemini_pro
  }
}


export function getSelectedStrategy(): string {
  if (typeof window !== 'undefined') {
    const stored = localStorage.getItem('selectedStrategy')
    return stored || Strategy.pubmed_search
  } else {
    // Default
    return Strategy.pubmed_search
  }
}
