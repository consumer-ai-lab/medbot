import buildAxiosClient from '@/api/build-axios-client'
import Navbar from '@/components/navbar'
import { ThemeProvider } from '@/components/theme-provider'
import { Toaster } from '@/components/ui/toaster'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Medbot',
  description:
    'Medbot is a medical chatbot that helps you diagnose your symptoms and find the right treatment.',
}

async function getAuthStatus() {
  try {
    const axiosClient = buildAxiosClient()
    const resp = await axiosClient.get('/api/auth/current-user')
    return resp
  } catch (err) {
    return null
  }
}

type UserType =
  | {
      email: string
      user_name: string
      user_level: string
    }
  | undefined

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  const resp: any = await getAuthStatus()
  const data: UserType = resp?.data

  return (
    <html lang="en">
      <body className={inter.className}>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <Navbar currentUser={data} />
          {children}
          <Toaster />
        </ThemeProvider>
      </body>
    </html>
  )
}
