'use client'

import { ChatLayout } from '@/components/chat/chat-layout'
import { getSelectedModel } from '@/lib/model-helper'
import { ChatOllama } from '@langchain/community/chat_models/ollama'
import { useChat } from 'ai/react'
import React from 'react'
import { toast } from 'sonner'

export default function Page({ params }: { params: { id: string } }) {
  const {
    messages,
    input,
    handleInputChange,
    isLoading,
    error,
    stop,
    setMessages,
    setInput,
  } = useChat({
    onResponse: (response) => {
      if (response) {
        setLoadingSubmit(false)
      }
    },
    onError: (error) => {
      setLoadingSubmit(false)
      toast.error('An error occurred. Please try again.')
    },
  })
  const [chatId, setChatId] = React.useState<string>('')
  const [selectedModel, setSelectedModel] = React.useState<string>(
    getSelectedModel(),
  )
  const [ollama, setOllama] = React.useState<ChatOllama>()
  const env = process.env.NODE_ENV
  const [loadingSubmit, setLoadingSubmit] = React.useState(false)

  React.useEffect(() => {
    if (params.id) {
      const item = localStorage.getItem(`chat_${params.id}`)
      if (item) {
        setMessages(JSON.parse(item))
      }
    }
  }, [setMessages])

  const addMessage = (Message: any) => {
    messages.push(Message)
    window.dispatchEvent(new Event('storage'))
    setMessages([...messages])
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()

    addMessage({ role: 'user', content: input, id: chatId })
    setInput('')
    addMessage({ role: 'assistant', content: 'Yohohohohooo', id: chatId })

    try {
      setLoadingSubmit(false)
    } catch (error) {
      toast.error('An error occurred. Please try again.')
      setLoadingSubmit(false)
    }
  }

  const onSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setLoadingSubmit(true)

    setMessages([...messages])
    handleSubmit(e)
  }

  // When starting a new chat, append the messages to the local storage
  React.useEffect(() => {
    if (!isLoading && !error && messages.length > 0) {
      localStorage.setItem(`chat_${params.id}`, JSON.stringify(messages))
      // Trigger the storage event to update the sidebar component
      window.dispatchEvent(new Event('storage'))
    }
  }, [messages, chatId, isLoading, error])

  return (
    <main className="flex h-[calc(100dvh)] flex-col items-center">
      <ChatLayout
        chatId={params.id}
        setSelectedModel={setSelectedModel}
        messages={messages}
        input={input}
        handleInputChange={handleInputChange}
        handleSubmit={onSubmit}
        isLoading={isLoading}
        loadingSubmit={loadingSubmit}
        error={error}
        stop={stop}
        navCollapsedSize={10}
        defaultLayout={[30, 160]}
      />
    </main>
  )
}
