import { ChatClient } from '@/components/chat/chat-client'
import { getSelectedModel } from '@/lib/model-helper'
import { useChat } from 'ai/react'
import axios from 'axios'
import React from 'react'
import { toast } from 'sonner'
import { Model } from '../../Model'
import { ApiQuery, ApiThreadQuery } from '../../types'
import { getAuthStatus } from '@/lib/get-auth-status'
import { UserType } from '@/lib/user-type'
import { redirect } from 'next/navigation'
 

export default async function Page() {

  const resp: any = await getAuthStatus()
  const data: UserType = resp?.data
  if(data === undefined){
    redirect('/auth/sign-in');
  }

  // const {
  //   messages,
  //   input,
  //   handleInputChange,
  //   isLoading,
  //   error,
  //   stop,
  //   setMessages,
  //   setInput,
  // } = useChat({
  //   onResponse: (response) => {
  //     if (response) {
  //       setLoadingSubmit(false)
  //     }
  //   },
  //   onError: (error) => {
  //     setLoadingSubmit(false)
  //     toast.error('An error occurred. Please try again.')
  //   },
  // })
  // const [chatId, setChatId] = React.useState<string>('')
  // const [selectedModel, setSelectedModel] = React.useState<string>(
  //   getSelectedModel(),
  // )
  // const [loadingSubmit, setLoadingSubmit] = React.useState(false)

  // React.useEffect(() => {
  //   async function fetch_messages() {
  //     if (params.id) {
  //       const body: ApiThreadQuery = {
  //         thread_id: params.id,
  //         user_id: localStorage.getItem('user_name') || '',
  //       }
  //       const response = await axios.post('/api/chat/thread', body)
  //       console.log(response)
  //       if (response) {
  //         // setMessages(response.data)
  //       }
  //     }
  //   }
  //   fetch_messages()
  // }, [setMessages])

  // const addMessage = (Message: any) => {
  //   messages.push(Message)
  //   window.dispatchEvent(new Event('storage'))
  //   setMessages([...messages])
  // }

  // const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
  //   e.preventDefault()

  //   addMessage({ role: 'user', content: input, id: chatId })
  //   const body: ApiQuery = {
  //     user_id: localStorage.getItem('user_name') || '',
  //     model: selectedModel as Model,
  //     question: input,
  //     thread_id: chatId,
  //   }
  //   setInput('')
  //   const response = (await axios.post('/api/chat/generate', body)).data
  //   console.log(response)
  //   addMessage({ role: 'assistant', content: 'Yohohohohooo', id: chatId })

  //   try {
  //     setLoadingSubmit(false)
  //   } catch (error) {
  //     toast.error('An error occurred. Please try again.')
  //     setLoadingSubmit(false)
  //   }
  // }

  // const onSubmit = (e: React.FormEvent<HTMLFormElement>) => {
  //   e.preventDefault()
  //   setLoadingSubmit(true)

  //   setMessages([...messages])
  //   handleSubmit(e)
  // }

  // // When starting a new chat, append the messages to the local storage
  // React.useEffect(() => {
  //   if (!isLoading && !error && messages.length > 0) {
  //     localStorage.setItem(`chat_${params.id}`, JSON.stringify(messages))
  //     // Trigger the storage event to update the sidebar component
  //     window.dispatchEvent(new Event('storage'))
  //   }
  // }, [messages, chatId, isLoading, error])

  return (
    <main className="flex h-[calc(100dvh)] flex-col items-center">
      <ChatClient
        user={data}
        // chatId={params.id}
        // setSelectedModel={setSelectedModel}
        // messages={messages}
        // input={input}
        // handleInputChange={handleInputChange}
        // handleSubmit={onSubmit}
        // isLoading={isLoading}
        // loadingSubmit={loadingSubmit}
        // error={error}
        // stop={stop}
        // navCollapsedSize={10}
        // defaultLayout={[30, 160]}
      />
    </main>
  )
}
