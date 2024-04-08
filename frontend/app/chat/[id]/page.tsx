import { ChatLayout } from '@/components/chat/chat-layout'
import { getAuthStatus } from '@/lib/get-current-user'
import { UserType } from '@/lib/types'
import { redirect } from 'next/navigation'
import React from 'react'



export default async function ChatPage({ params }: { params: { id: string } }) {

  const resp: any = await getAuthStatus()
  const data: UserType = resp?.data;
  if(!data){
    redirect('/auth/sign-in')
  }

  return (
    <main className="flex h-[calc(100dvh)] flex-col items-center">
      <ChatLayout
        chatId={params.id}
        setSelectedModel={()=>{}}
        messages={[{id:'adad',content:'asasd',role:'user'}]}
        input={'input'}
        handleInputChange={()=>{}}
        handleSubmit={()=>{}}
        isLoading={true}
        loadingSubmit={true}
        error={undefined}
        stop={()=>{}}
        navCollapsedSize={10}
        defaultLayout={[30, 160]}
      />
    </main>


  )
}
