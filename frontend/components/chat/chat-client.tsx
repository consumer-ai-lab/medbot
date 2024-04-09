'use client'
import {
	ResizableHandle,
	ResizablePanel,
	ResizablePanelGroup,
} from '@/components/ui/resizable'
import { cn } from '@/lib/utils'
import React, { useEffect, useState } from 'react'
import { Sidebar } from '../sidebar'
import Chat from './chat'
import { useCompletion, type Message } from 'ai/react'
import { useToast } from '../ui/use-toast'
import { getSelectedModel } from '@/lib/model-helper'
import { UserType } from '@/lib/user-type'
import { Model } from '@/Model'
import { v4 } from 'uuid';
import { set } from 'react-hook-form'

interface ChatClientProps {
	defaultLayout?: number[] | undefined
	defaultCollapsed?: boolean
	navCollapsedSize?: number
	chatId?: string
	user: UserType;
}

const messagesStub: Message[] = [
	{
		id: 'abc',
		content: 'Hello, this is your friendly ai assistant',
		role: 'assistant'
	},
	{
		id: 'def',
		content: 'Hey AI, What can you do for me?',
		role: 'user'
	},
	{
		id: 'ghi',
		content: 'I can help you with anything you need',
		role: 'assistant'
	},
]


export function ChatClient({
	defaultLayout = [30, 160],
	defaultCollapsed = false,
	navCollapsedSize = 10,
	user
}: ChatClientProps) {
	const {toast}=useToast();
	const [isCollapsed, setIsCollapsed] = React.useState(defaultCollapsed)
	const [isMobile, setIsMobile] = useState(false);
	const [loadingSubmit, setLoadingSubmit] = React.useState(false)
	const [messages, setMessages] = useState<Message[]>(messagesStub);
	const [threadId,setThreadId]=useState<string>('');
	const [newThreadId,setNewThreadId]=useState<string>('');

	const {
		input,
		setInput,
		completion,
		isLoading,
		handleInputChange,
		handleSubmit,
		stop,
	} = useCompletion({
		api: '/api/chat/generate',
		onFinish(prompt,completion) {
            setMessages((current) => [...current, {
				id:'todo',
				content: completion,
				role: 'assistant'
			}]);
			if(threadId.length===0){
				setThreadId(newThreadId);
			}
        },
		onResponse: (response) => {
			if (response) {
				setInput('')
				setLoadingSubmit(false);
			}
		},
		onError: (error) => {
			setLoadingSubmit(false)
			toast({
				variant:"destructive",
				description:'An error occurred. Please try again.'
			})
		},
		body: {
			model: getSelectedModel() as Model,
			thread_id: threadId.length>0?threadId:newThreadId,
		}
	})

	function onSubmit(e: React.FormEvent<HTMLFormElement>) {
        const userMessage: Message = {
            role: "user",
            content: input,
			id: 'sd'
        };
        setMessages((current) => [...current, userMessage]);
        handleSubmit(e);
    }

	useEffect(()=>{
		setNewThreadId(v4())
	},[input])
	
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
					threadId={threadId}
					setThreadId={setThreadId}
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
					user={user}
					completion={completion}
					threadId={threadId}
					setThreadId={setThreadId}
					messages={messages}
					input={input}
					handleInputChange={handleInputChange}
					handleSubmit={onSubmit}
					isLoading={isLoading}
					loadingSubmit={loadingSubmit}
					stop={stop}
				/>
			</ResizablePanel>
		</ResizablePanelGroup>
	)
}
