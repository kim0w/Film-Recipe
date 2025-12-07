import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Film Recipe - Film Simulation Web App',
  description: 'Apply analog film effects to your digital photos',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  )
}
