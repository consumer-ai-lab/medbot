import TypewriterTitle from '@/components/typewriter-title'
import { Button } from '@/components/ui/button'
import { getAuthStatus } from '@/lib/get-auth-status'
import { UserType } from '@/lib/user-type'
import { ArrowRight } from 'lucide-react'
import Link from 'next/link'
import { redirect } from 'next/navigation'
import React from 'react'


export default async function Home() {

  const resp: any = await getAuthStatus()
  const data: UserType = resp?.data
  if (data !== undefined) {
    redirect('/chat');
  }

  return (
    <main className="flex h-[calc(100dvh)] bg-gradient-to-r min-h-screen ">
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
          <h1 className="font-semibold text-7xl text-center">
            AI Powered <span className="text-green-600 font-bold ">General Practitioner </span>{" "} Chatbot.
          </h1>
          <div className="mt-4">

          </div>
          <div className="font-semibold text-4xl text-center">
              <TypewriterTitle/>
          </div>
          <div className="mt-8">

          </div>
          <div className="flex justify-center">
            <Link href="/chat">
              <Button
                size={"lg"}
              >
                Get Started
                <ArrowRight
                  className="ml-2 w-5 h-5"
                  strokeWidth={3}
                />
              </Button>
            </Link>
          </div>
      </div>
    </main>
  )
}
