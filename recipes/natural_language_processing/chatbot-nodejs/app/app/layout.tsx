export const metadata = {
  title: 'Sample Node.js AI Chatbot',
  description: 'Sample Node.js AI Chatbot',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
