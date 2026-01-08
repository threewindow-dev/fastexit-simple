import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'FastExit - User Management',
  description: 'FastAPI + Next.js User Management System',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  )
}
