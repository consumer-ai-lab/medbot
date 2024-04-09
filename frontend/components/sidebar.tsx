'use client'
import { Button, buttonVariants } from '@/components/ui/button'
import { cn } from '@/lib/utils'
import { Message } from 'ai/react'
import axios from 'axios'
import { MoreHorizontal, SquarePen, Trash2 } from 'lucide-react'
import Image from 'next/image'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import SidebarSkeleton from './sidebar-skeleton'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from './ui/dialog'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuTrigger,
} from './ui/dropdown-menu'
import UserSettings from './user-settings'
import { UserType } from '@/lib/user-type'
import buildAxiosClient from '@/api/build-axios-client'

interface SidebarProps {
  isCollapsed: boolean
  onClick?: () => void
  isMobile: boolean
  user: UserType
  threadId?: string
  setThreadId: (threadId: string) => void;
}

type ThreadType={
  title:string;
  id:string;
}

export function Sidebar({
  isCollapsed,
  isMobile,
  threadId,
  setThreadId,
  user
}: SidebarProps) {

  const [isLoading, setIsLoading] = useState(true);
  const [allThreads, setAllThreads] = useState<ThreadType[]>([]);

  useEffect(() => {
    axios.get('/api/chat/get-threads',{withCredentials:true}).then((resp:any)=>{
      if(resp.data && resp.data.length>0){
        setAllThreads(resp.data.reverse());
      }
    })
    setIsLoading(false)
  }, [threadId])



  // TODO: Delete handler
  const handleDeleteChat = (chatId: string) => {

  }

  return (
    <div
      data-collapsed={isCollapsed}
      className="relative justify-between group lg:bg-accent/20 lg:dark:bg-card/35 flex flex-col h-full gap-4 p-2 data-[collapsed=true]:p-2 "
    >
      <div className=" flex flex-col justify-between p-2 max-h-fit overflow-y-auto">
        <Button
          onClick={() => {
            setThreadId('')
          }}
          variant="ghost"
          className="flex justify-between w-full h-14 text-sm xl:text-lg font-normal items-center "
        >
          <div className="flex gap-3 items-center ">
            {!isCollapsed && !isMobile && (
              <Image
                src="/ollama.png"
                alt="AI"
                width={28}
                height={28}
                className="dark:invert hidden 2xl:block"
              />
            )}
            New chat
          </div>
          <SquarePen
            size={18}
            className="shrink-0 w-4 h-4"
          />
        </Button>

        <div className="flex flex-col pt-10 gap-2">
          <p className="pl-4 text-xs text-muted-foreground">Your chats</p>
          {allThreads.length > 0 && (
            <div className='flex flex-col gap-4'>
              {allThreads.map(({ title, id }) => (
                <div
                  key={id}
                  onClick={() => setThreadId(id)}
                  className={cn(
                    {
                      [buttonVariants({ variant: 'secondaryLink' })]:
                        id === threadId,
                      [buttonVariants({ variant: 'ghost' })]:
                        id !== threadId,
                    },
                    'flex justify-between w-full h-14 text-base font-normal items-center',
                  )}
                >
                  <div className="flex gap-3 items-center truncate">
                    <div className="flex flex-col">
                      <span className="text-xs font-normal ">
                        {title.length > 0 ? title : ''}
                      </span>
                    </div>
                  </div>
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button
                        variant="ghost"
                        className="flex justify-end items-center"
                        onClick={(e) => e.stopPropagation()}
                      >
                        <MoreHorizontal
                          size={15}
                          className="shrink-0"
                        />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent className=" ">
                      <Dialog>
                        <DialogTrigger asChild>
                          <Button
                            variant="ghost"
                            className="w-full flex gap-2 hover:text-red-500 text-red-500 justify-start items-center"
                            onClick={(e) => e.stopPropagation()}
                          >
                            <Trash2 className="shrink-0 w-4 h-4" />
                            Delete chat
                          </Button>
                        </DialogTrigger>
                        <DialogContent>
                          <DialogHeader className="space-y-4">
                            <DialogTitle>Delete chat?</DialogTitle>
                            <DialogDescription>
                              Are you sure you want to delete this chat? This
                              action cannot be undone.
                            </DialogDescription>
                            <div className="flex justify-end gap-2">
                              <Button variant="outline">Cancel</Button>
                              <Button
                                variant="destructive"
                                onClick={() => handleDeleteChat(id)}
                              >
                                Delete
                              </Button>
                            </div>
                          </DialogHeader>
                        </DialogContent>
                      </Dialog>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
              ))}
            </div>
          )}
          {isLoading && <SidebarSkeleton />}
        </div>
      </div>

      <div className="justify-end px-2 py-2 w-full border-t">
        <UserSettings
          user={user}
        />
      </div>
    </div>
  )
}
