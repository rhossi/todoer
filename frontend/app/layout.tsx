import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Todoer - Task Management with Neon-Dark Design',
  description: 'Todoer - Track your tasks with the new neon-dark system. Stay organized, stay productive.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="font-display text-gray-100 antialiased">
        <div className="relative z-10">{children}</div>
      </body>
    </html>
  )
}

