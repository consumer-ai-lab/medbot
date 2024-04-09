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

  return (
    <main className="flex h-[calc(90dvh)] flex-col items-center">
      <ChatClient
        user={data}
      />
    </main>
  )
}
