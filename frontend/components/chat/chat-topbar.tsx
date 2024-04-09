'use client'

import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet'
import React, { useEffect } from 'react'

import { getSelectedModel } from '@/lib/model-helper'
import { CaretSortIcon, HamburgerMenuIcon } from '@radix-ui/react-icons'
import { Message } from 'ai/react'
import { Sidebar } from '../sidebar'
import { Button } from '../ui/button'
import { UserType } from '@/lib/user-type'

interface ChatTopbarProps {
  isLoading: boolean
  chatId?: string
  messages: Message[]
  user:UserType
}

export default function ChatTopbar({
  isLoading,
  chatId,
  messages,
  user
}: ChatTopbarProps) {
  const [models, setModels] = React.useState<string[]>([])
  const [open, setOpen] = React.useState(false)
  const [currentModel, setCurrentModel] = React.useState<string | null>(null)

  useEffect(() => {
    setCurrentModel(getSelectedModel())

    const env = process.env.NODE_ENV

    const fetchModels = async () => {
      // const fetchedModels = await fetch(process.env.NEXT_PUBLIC_OLLAMA_URL + "/api/tags");
      // const json = await fetchedModels.json();
      // const apiModels = json.models.map((model : any) => model.name);
      const apiModels = ['gemini', 'chatgpt']
      setModels([...apiModels])
    }
    fetchModels()
  }, [])

  const handleModelChange = (model: string) => {
    setCurrentModel(model)
    if (typeof window !== 'undefined') {
      localStorage.setItem('selectedModel', model)
    }
    setOpen(false)
  }

  return (
    <div className="w-full flex px-4 py-6  items-center justify-between lg:justify-center ">
      <Sheet>
        <SheetTrigger>
          <HamburgerMenuIcon className="lg:hidden w-5 h-5" />
        </SheetTrigger>
        <SheetContent side="left">
          <Sidebar
            user={user}
            chatId={chatId || ''}
            isCollapsed={false}
            isMobile={false}
            messages={messages}
          />
        </SheetContent>
      </Sheet>
    </div>
  )
}
