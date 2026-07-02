import { useState, useEffect, useRef } from 'react'
import {fetchChatResponseHTTP} from '../https/http'

const initialMessages = [
  {
    role: 'assistant',
    content: 'Hi there! I can help you review revenue assurance controls, exceptions, and remediation actions. Ask me anything.',
  },
]

export default function ChatInterface() {
  const [messages, setMessages] = useState(initialMessages)
  const [draft, setDraft] = useState('')
  const bottomRef = useRef(null)

  useEffect(() => {
   async function fetchResponse() {
      if (messages.length > 0 && messages[messages.length - 1].role === 'user') {
        const userMessage = messages[messages.length - 1].content
        try {
          const response = await fetchChatResponseHTTP(userMessage)
          setMessages((current) => [
            ...current,
            {
              role: 'assistant',
              content: response.result || 'Sorry, I could not generate a response.',
            },
          ])
        } catch (error) {
          console.error('Error fetching chat response:', error)
          setMessages((current) => [
            ...current,
            {
              role: 'assistant',
              content: 'Sorry, there was an error processing your request.',
            },
          ])
        }
      }
    }

    fetchResponse()
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })

  }, [messages[messages.length - 1].content])

  const sendMessage = (event) => {
    event.preventDefault()
    const trimmed = draft.trim()
    if (!trimmed) return // Ignore empty messages

    const userMessage = { role: 'user', content: trimmed }
    setMessages((current) => [...current, userMessage])
    setDraft('')
  }

  return (
    <section className="rounded-lg border border-[#e4e1da] bg-white/90 p-5 text-left shadow-[0_1px_2px_rgba(17,17,17,0.04)] transition-colors duration-300 dark:border-[#29302d] dark:bg-[#171b19]" id="chat">
      <div className="mb-4 flex items-center justify-between gap-3">
        <div>
          <p className="mb-2 block text-xs font-bold uppercase tracking-[0.08em] text-[#77736c] dark:text-[#8f9691]">Assistant</p>
          <h2 className="text-xl leading-tight font-semibold text-[#111111] dark:text-[#f3f4f2]">Control AI chat</h2>
        </div>
        <span className="rounded-full bg-[rgba(16,163,127,0.12)] px-3 py-1 text-xs font-semibold text-[#08745c] dark:bg-[rgba(16,185,129,0.18)] dark:text-[#5ee0be]">Online</span>
      </div>

      <div className="flex h-[360px] flex-col overflow-hidden rounded-3xl border border-[#e4e1da] bg-[#fbfbf8] shadow-sm dark:border-[#29302d] dark:bg-[#141715]">
        <div className="flex-1 overflow-y-auto px-4 py-4 text-sm text-[#111111] dark:text-[#f3f4f2]">
          <div className="space-y-3">
            {messages.map((message, index) => (
              <div
                key={`${message.role}-${index}`}
                className={`rounded-3xl px-4 py-3 shadow-sm ${
                  message.role === 'user'
                    ? 'ml-auto max-w-[85%] bg-[#111111] text-white dark:bg-[#f3f4f2] dark:text-[#111111]'
                    : 'mr-auto max-w-[90%] bg-white text-[#111111] dark:bg-[#202622] dark:text-[#f3f4f2]'
                }`}
              >
                <p className="whitespace-pre-wrap">{message.content}</p>
              </div>
            ))}
            <div ref={bottomRef} />
          </div>
        </div>

        <form onSubmit={sendMessage} className="border-t border-[#e4e1da] bg-white/90 p-4 dark:border-[#29302d] dark:bg-[#141715]">
          <div className="flex gap-2">
            <input
              className="min-h-[42px] flex-1 rounded-2xl border border-[#e4e1da] bg-white px-4 text-sm text-[#111111] outline-none transition focus:border-[#10a37f] focus:ring-2 focus:ring-[#10a37f]/20 dark:border-[#29302d] dark:bg-[#202622] dark:text-[#f3f4f2]"
              placeholder="Write a message..."
              value={draft}
              onChange={(event) => setDraft(event.target.value)}
              aria-label="Chat input"
            />
            <button
              type="submit"
              className="min-h-[42px] rounded-2xl bg-[#111111] px-4 text-sm font-semibold text-[#f7f7f4] transition hover:bg-[#333333] dark:bg-[#f3f4f2] dark:text-[#111111] dark:hover:bg-[#e6e6e2]"
            >
              Send
            </button>
          </div>
        </form>
      </div>
    </section>
  )
}
