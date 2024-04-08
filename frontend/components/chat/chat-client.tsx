'use client'

import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from '@/components/ui/resizable'
import { cn } from '@/lib/utils'
import React, { useEffect, useState } from 'react'
import { Sidebar } from '../sidebar'
import Chat, { ChatProps } from './chat'
import { useChat, type Message } from 'ai/react'
import { toast } from 'sonner'
import { getSelectedModel } from '@/lib/model-helper'
import { UserType } from '@/lib/user-type'

interface ChatClientProps {
  defaultLayout?: number[] | undefined
  defaultCollapsed?: boolean
  navCollapsedSize?: number
  chatId?: string
  user:UserType;
}

const messages:Message[]=[
  {
    id:'abc',
    content:'Hello, this is your friendly ai assistant',
    role:'assistant'
  },
  {
    id:'def',
    content:'Hey AI, What can you do for me?',
    role:'user'
  },
  {
    id:'ghi',
    content:'I can help you with anything you need',
    role:'assistant'
  },
  {
    id:'jkl',
    content:'Great, I need help with my taxes',
    role:'user'
  },
]

const chatId = 'abcdefg';

export function ChatClient({
  defaultLayout = [30, 160],
  defaultCollapsed = false,
  navCollapsedSize=10,
  user,
  // messages,  TODO: Fetch messages
}: ChatClientProps) {
  const [isCollapsed, setIsCollapsed] = React.useState(defaultCollapsed)
  const [isMobile, setIsMobile] = useState(false);
  const [loadingSubmit, setLoadingSubmit] = React.useState(false)
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

   const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()

    // addMessage({ role: 'user', content: input, id: chatId })
    // const body: ApiQuery = {
    //   user_id: localStorage.getItem('user_name') || '',
    //   model: selectedModel as Model,
    //   question: input,
    //   thread_id: chatId,
    // }
    // setInput('')
    // const response = (await axios.post('/api/chat/generate', body)).data
    // console.log(response)
    // addMessage({ role: 'assistant', content: 'Yohohohohooo', id: chatId })

    // try {
    //   setLoadingSubmit(false)
    // } catch (error) {
    //   toast.error('An error occurred. Please try again.')
    //   setLoadingSubmit(false)
    // }
  }

    const [selectedModel, setSelectedModel] = React.useState<string>(
    getSelectedModel(),
  )

  useEffect(() => {
    const checkScreenWidth = () => {
      setIsMobile(window.innerWidth <= 640)
    }

    // Initial check
    checkScreenWidth()

    // Event listener for screen width changes
    window.addEventListener('resize', checkScreenWidth)

    // Cleanup the event listener on component unmount
    return () => {
      window.removeEventListener('resize', checkScreenWidth)
    }
  }, [])

  return (
    <ResizablePanelGroup
      direction="horizontal"
      onLayout={(sizes: number[]) => {
        document.cookie = `react-resizable-panels:layout=${JSON.stringify(
          sizes,
        )}`
      }}
      className="h-screen items-stretch"
    >
      <ResizablePanel
        defaultSize={defaultLayout[0]}
        collapsedSize={navCollapsedSize}
        collapsible={true}
        minSize={isMobile ? 0 : 12}
        maxSize={isMobile ? 0 : 16}
        onCollapse={() => {
          setIsCollapsed(true)
          document.cookie = `react-resizable-panels:collapsed=${JSON.stringify(
            true,
          )}`
        }}
        onExpand={() => {
          setIsCollapsed(false)
          document.cookie = `react-resizable-panels:collapsed=${JSON.stringify(
            false,
          )}`
        }}
        className={cn(
          isCollapsed
            ? 'min-w-[50px] md:min-w-[70px] transition-all duration-300 ease-in-out'
            : 'hidden md:block',
        )}
      >
        <Sidebar
          user={user}
          isCollapsed={isCollapsed || isMobile}
          messages={messages}
          isMobile={isMobile}
          chatId={chatId}
        />
      </ResizablePanel>
      <ResizableHandle
        className={cn('hidden md:flex')}
        withHandle
      />
      <ResizablePanel
        className="h-full"
        defaultSize={defaultLayout[1]}
      >
        <Chat
          chatId={chatId}
          setSelectedModel={setSelectedModel}
          messages={messages}
          input={input}
          handleInputChange={handleInputChange}
          handleSubmit={handleSubmit}
          isLoading={isLoading}
          loadingSubmit={loadingSubmit}
          error={error}
          stop={stop}
        />
      </ResizablePanel>
    </ResizablePanelGroup>
  )
}
