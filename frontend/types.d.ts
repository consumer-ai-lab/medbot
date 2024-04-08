import type { Model } from '@/Model'

enum MessageRole {
  user = 'user',
  assistant = 'assistant',
}

interface Message {
  role: MessageRole
  content: string
}

interface ChatThread {
  title: string
  id: string
}

interface Query {
  question: string
  model: Model
}

interface ApiThreadQuery {
  user_id: string
  thread_id: string
}

interface ApiQuery {
  user_id: string
  thread_id: string
  model: Model
  question: string
}

interface QaQuery {
  model: Model
  question: string
  summary: string
}

interface QaResponse {
  type: 'OK' | 'REJECTED'
  response: string
}

