'use client'

import { ChatLayout } from '@/components/chat/chat-layout'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import UsernameForm from '@/components/username-form'
import { getSelectedModel } from '@/lib/model-helper'
import { useChat } from 'ai/react'
import axios from 'axios'
import React from 'react'
import { v4 as uuidv4 } from 'uuid'
import { Model } from '../Model'
import { ApiQuery } from '../types'

export default function Home() {
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
  
  return (
    <main className="flex h-[calc(100dvh)] flex-col items-center ">
      Landing Page
    </main>
  )
}
