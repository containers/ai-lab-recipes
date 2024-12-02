export const metadata = {
  title: 'Sample Node.js RAG example ',
  description: 'Sample Node.js RAG example',
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
