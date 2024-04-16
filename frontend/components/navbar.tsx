'use client'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'
import axios from 'axios'
import { Poppins } from 'next/font/google'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'
import { ModeToggle } from './mode-toggle'

const font = Poppins({
  weight: '600',
  subsets: ['latin'],
})

const routes = [
  {
    href: '/auth/sign-in',
    label: 'Sign In',
    logined: false,
  },
  {
    href: '/auth/sign-up',
    label: 'Sign Up',
    logined: false,
  },
]

interface NavbarProps {
  currentUser?: {
    email: string
    user_name: string
    user_level: string
  }
}

export default function Navbar({ currentUser }: NavbarProps) {


  useEffect(() => {
    localStorage.setItem('user_name', currentUser?.user_name || 'Anonymous')
    window.dispatchEvent(new Event('storage'))
  }, [currentUser])

  
  const router = useRouter()

  async function onClick(label: string) {
    switch (label) {
      case 'Sign In': {
        router.push('/auth/sign-in')
        break
      }
      case 'Sign Up': {
        router.push('/auth/sign-up')
        break
      }
      case 'Sign Out': {
        await axios.post('/api/auth/signout')
        router.push('/')
        router.refresh()
        break
      }
      default: {
        throw new Error('Invalid Route')
      }
    }
  }

  return (
    <div className="w-full h-[calc(10dvh)] z-50 flex justify-between items-center py-2 px-4 border-b border-primary/10 bg-secondary">
      <div
        className="flex text-3xl items-center cursor-pointer"
        onClick={() => router.push('/')}
      >
        <h1
          className={cn(
            'hidden md:block text-xl md:text-3xl font-bold text-primary',
            font.className,
          )}
        >
          medbot.
        </h1>
      </div>
      <div className="flex items-center gap-x-3">
        {currentUser === undefined ? (
          routes.map((route) => {
            return (
              <Button
                key={route.href}
                variant={'ghost'}
                onClick={() => onClick(route.label)}
              >
                <h1
                  className={cn(
                    'font-bold text-lg cursor-pointer',
                    font.className,
                  )}
                >
                  {route.label}
                </h1>
              </Button>
            )
          })
        ) : (
          <Button
            variant={'ghost'}
            onClick={() => onClick('Sign Out')}
          >
            <h1
              className={cn('font-bold text-lg cursor-pointer', font.className)}
            >
              Sign Out
            </h1>
          </Button>
        )}
        <ModeToggle />
      </div>
    </div>
  )
}
