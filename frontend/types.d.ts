declare enum MessageRole {
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

declare enum Model {
  gemini_pro_chat = 'gemini-pro-chat',
  gemini_pro = 'gemini-pro',
  llama2 = 'llama2',
  llama2_uncensored = 'llama2-uncensored',
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
