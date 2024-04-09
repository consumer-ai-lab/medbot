import React from 'react'
import ChatTopbar from './chat-topbar'
import ChatList from './chat-list'
import ChatBottombar from './chat-bottombar'
import { type Message } from 'ai/react';
import { ChatRequestOptions } from 'ai';
import { UserType } from '@/lib/user-type';
import { MessageType } from '@/lib/message-type';

export interface ChatProps {
  setSelectedModel?: React.Dispatch<React.SetStateAction<string>>;
  messages: MessageType[];
  input: string;
  handleInputChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
  handleSubmit: (e: React.FormEvent<HTMLFormElement>, chatRequestOptions?: ChatRequestOptions) => void;
  isLoading: boolean;
  loadingSubmit?: boolean;
  error?: undefined | Error;
  completion:string;
  stop: () => void;
  threadId?: string;
  setThreadId: (threadId: string) => void;
  user:UserType
  }

export default function Chat ({ messages, input, handleInputChange, handleSubmit, isLoading, error, stop, setSelectedModel, threadId,setThreadId, loadingSubmit,completion,user }: ChatProps) {

  return (
    <div className="flex flex-col justify-between w-full h-full  ">
        <ChatTopbar
          user={user}  
          threadId={threadId}
          setThreadId={setThreadId}
        />
        <ChatList  
          completion={completion}
          messages={messages}
          isLoading={isLoading}
          loadingSubmit={loadingSubmit}
        />
        <ChatBottombar 
          input={input}
          handleInputChange={handleInputChange}
          handleSubmit={handleSubmit}
          isLoading={isLoading}
          stop={stop}
        />
    </div>
  )
}
