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
import { useCompletion, type Message } from 'ai/react'
import { toast } from 'sonner'
import { getSelectedModel } from '@/lib/model-helper'
import { UserType } from '@/lib/user-type'
import { Model } from '@/Model'

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

const chatId = 'abcdefg';

export function ChatClient({
	defaultLayout = [30, 160],
	defaultCollapsed = false,
	navCollapsedSize = 10,
	user
	// messages,  TODO: Fetch messages
}: ChatClientProps) {
	const [isCollapsed, setIsCollapsed] = React.useState(defaultCollapsed)
	const [isMobile, setIsMobile] = useState(false);
	const [loadingSubmit, setLoadingSubmit] = React.useState(false)
	const [messages, setMessages] = useState<Message[]>(messagesStub);

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
        },
		onResponse: (response) => {
			if (response) {
				setInput('')
				setLoadingSubmit(false);
			}
		},
		onError: (error) => {
			setLoadingSubmit(false)
			toast.error('An error occurred. Please try again.')
		},
		body: {
			user_id: 'asdasd' || '',
			model: getSelectedModel() as Model,
			thread_id: 'klsdfa',
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
					user={user}
					completion={completion}
					chatId={chatId}
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
