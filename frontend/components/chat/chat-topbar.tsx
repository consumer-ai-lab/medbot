'use client'
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet'
import React from 'react'
import { Menu } from "lucide-react"
import { Message } from 'ai/react'
import { Sidebar } from '../sidebar'
import { UserType } from '@/lib/user-type'

interface ChatTopbarProps {
  threadId?: string
  setThreadId: (threadId: string) => void
  user:UserType
} 

export default function ChatTopbar({
  threadId,
  setThreadId,
  user
}: ChatTopbarProps) {

  return (
    <div className="w-full flex px-4 py-6  items-center justify-between lg:justify-center ">
      <Sheet>
        <SheetTrigger>
          <Menu className="lg:hidden w-5 h-5" />
        </SheetTrigger>
        <SheetContent side="left">
          <Sidebar
            user={user}
            threadId={threadId}
            setThreadId={setThreadId}
            isCollapsed={false}
            isMobile={false}
          />
        </SheetContent>
      </Sheet>
    </div>
  )
}
