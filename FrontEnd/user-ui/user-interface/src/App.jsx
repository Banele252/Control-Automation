import { useState, useEffect } from 'react'

const controlStats = [
  { label: 'Revenue at risk', value: '$2.84M', trend: '-18%', tone: 'high' },
  { label: 'Controls healthy', value: '91.6%', trend: '+4.2%', tone: 'good' },
  { label: 'Open exceptions', value: '143', trend: '27 new', tone: 'warn' },
  { label: 'SLA coverage', value: '98.1%', trend: '11 controls', tone: 'good' },
]

const controls = [
  {
    id: 'RA-042',
    name: 'Usage-to-billing completeness',
    domain: 'Mobile prepaid',
    owner: 'Billing Ops',
    exposure: '$920K',
    status: 'Investigating',
    score: 74,
  },
  {
    id: 'RA-117',
    name: 'Rating variance guardrail',
    domain: 'Enterprise data',
    owner: 'Revenue Assurance',
    exposure: '$410K',
    status: 'Monitoring',
    score: 88,
  },
  {
    id: 'RA-203',
    name: 'Partner settlement reconciliation',
    domain: 'Roaming',
    owner: 'Wholesale',
    exposure: '$1.2M',
    status: 'Action needed',
    score: 61,
  },
  {
    id: 'RA-318',
    name: 'Contract discount leakage',
    domain: 'B2B contracts',
    owner: 'Commercial Finance',
    exposure: '$310K',
    status: 'Healthy',
    score: 96,
  },
]

const alerts = [
  { title: 'CDR ingestion gap', detail: 'Cluster NE-04 missed 18 minutes of events', time: '11 min ago' },
  { title: 'Margin drift detected', detail: 'Bundle B-19 cost recovery moved below threshold', time: '34 min ago' },
  { title: 'Duplicate settlement line', detail: 'Partner file KEN-884 has 217 repeated records', time: '1 hr ago' },
]

const timeline = [
  ['08:00', 'Usage feeds reconciled', '2.8B records checked'],
  ['09:30', 'Rating controls scored', '4 controls below target'],
  ['11:00', 'Exception pack generated', '143 cases routed'],
  ['13:00', 'Owner attestation due', '6 teams pending'],
]

const navItems = [
  { label: 'Overview', icon: '⌂' },
  { label: 'Controls', icon: '▦' },
  { label: 'Exceptions', icon: '!' },
  { label: 'Evidence', icon: '◫' },
  { label: 'Settings', icon: '⚙' },
]

const statTone = {
  good: 'text-[#10a37f]',
  warn: 'text-amber-700 dark:text-amber-400',
  high: 'text-amber-700 dark:text-amber-400',
}

const panelClass = 'rounded-lg border border-[#e4e1da] bg-white/90 p-5 text-left shadow-[0_1px_2px_rgba(17,17,17,0.04)] transition-colors duration-300 dark:border-[#29302d] dark:bg-[#171b19]'
const eyebrowClass = 'mb-2 block text-xs font-bold uppercase tracking-[0.08em] text-[#77736c] dark:text-[#8f9691]'
const primaryButtonClass = 'min-h-[38px] rounded-lg bg-[#111111] px-4 font-semibold text-[#f7f7f4] transition hover:-translate-y-px hover:shadow-[0_14px_32px_rgba(17,17,17,0.1)] dark:bg-[#f3f4f2] dark:text-[#111111]'
const ghostButtonClass = 'min-h-[38px] rounded-lg border border-[#e4e1da] bg-white/90 px-3.5 text-[#111111] transition hover:-translate-y-px hover:shadow-[0_14px_32px_rgba(17,17,17,0.1)] dark:border-[#29302d] dark:bg-[#1a1e1c] dark:text-[#f3f4f2]'

function App() {
  const [isDarkMode, setIsDarkMode] = useState(false)
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false)
  const [exceptions, setException] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulate fetching exceptions from an API
    async function fetchExceptions() {
      setLoading(true)
      const response = await fetch('http://localhost:8000/supabase/data/exception')
      const data = await response.json()
      setException(data)
      setLoading(false)
      console.log('Fetched exceptions:', data)
    }

    fetchExceptions()
  }, [])

  return (
    <main className={`${isDarkMode ? 'dark' : ''} grid min-h-svh ${isSidebarCollapsed ? 'grid-cols-[76px_minmax(0,1fr)]' : 'grid-cols-[248px_minmax(0,1fr)]'} bg-[#f7f7f4] bg-[radial-gradient(circle_at_top_left,rgba(16,185,129,0.08),transparent_34rem)] text-[#525252] transition-[grid-template-columns,background-color,color] duration-300 dark:bg-[#0f1110] dark:bg-[radial-gradient(circle_at_top_left,rgba(16,185,129,0.16),transparent_34rem)] dark:text-[#c9cbc8] max-[1120px]:grid-cols-1`}>
      <aside className={`sticky top-0 flex h-svh flex-col border-r border-[#e4e1da] bg-[#fafaf8]/75 backdrop-blur-xl transition-all duration-300 dark:border-[#29302d] dark:bg-[#141715]/80 ${isSidebarCollapsed ? 'gap-4 p-4' : 'gap-7 p-6'} max-[1120px]:static max-[1120px]:h-auto max-[1120px]:flex-row max-[1120px]:items-center max-[1120px]:p-4 max-[720px]:flex-col max-[720px]:items-start max-[720px]:gap-3.5`} aria-label="Revenue assurance navigation">
        <div className={`flex items-center gap-2.5 font-semibold text-[#111111] dark:text-[#f3f4f2] ${isSidebarCollapsed ? 'flex-col justify-center' : 'justify-between'} max-[1120px]:flex-row max-[1120px]:justify-start`}>
          <div className="flex min-w-0 items-center gap-2.5">
          <span className="grid h-[34px] w-[34px] place-items-center rounded-full border border-[#cfcbc1] text-[22px] text-[#10a37f] dark:border-[#3a423f]">◎</span>
            <span className={`${isSidebarCollapsed ? 'sr-only' : 'block'} max-[1120px]:not-sr-only`}>ControlAI</span>
          </div>
          <button
            className="grid h-8 w-8 place-items-center rounded-lg border border-[#e4e1da] bg-white/90 text-[#111111] transition hover:-translate-y-px hover:shadow-[0_14px_32px_rgba(17,17,17,0.1)] dark:border-[#29302d] dark:bg-[#1a1e1c] dark:text-[#f3f4f2] max-[1120px]:hidden"
            type="button"
            aria-label={isSidebarCollapsed ? 'Expand sidepane' : 'Collapse sidepane'}
            aria-expanded={!isSidebarCollapsed}
            onClick={() => setIsSidebarCollapsed((currentValue) => !currentValue)}
          >
            {isSidebarCollapsed ? '›' : '‹'}
          </button>
        </div>
        <nav className={`grid gap-1 max-[1120px]:flex max-[1120px]:overflow-x-auto max-[720px]:w-full ${isSidebarCollapsed ? 'justify-items-center' : ''}`}>
          {navItems.map((item) => (
            <a
              className={`flex items-center gap-2.5 rounded-lg text-sm no-underline transition hover:bg-white/90 hover:text-[#111111] dark:hover:bg-[#1d221f] dark:hover:text-[#f3f4f2] ${isSidebarCollapsed ? 'h-10 w-10 justify-center p-0' : 'px-3 py-2.5'} max-[1120px]:h-auto max-[1120px]:w-auto max-[1120px]:justify-start max-[1120px]:px-3 max-[1120px]:py-2.5 ${
                item.label === 'Overview' ? 'bg-white/90 text-[#111111] dark:bg-[#1d221f] dark:text-[#f3f4f2]' : 'text-[#525252] dark:text-[#c9cbc8]'
              }`}
              href={`#${item.label.toLowerCase()}`}
              key={item.label}
              title={isSidebarCollapsed ? item.label : undefined}
            >
              <span aria-hidden="true">{item.icon}</span>
              <span className={`${isSidebarCollapsed ? 'sr-only' : 'block'} max-[1120px]:not-sr-only`}>{item.label}</span>
            </a>
          ))}
        </nav>
        <div className={`${isSidebarCollapsed ? 'hidden' : 'block'} mt-auto rounded-lg border border-[#e4e1da] bg-white/90 p-4 text-left dark:border-[#29302d] dark:bg-[#1a1e1c] max-[1120px]:hidden`}>
          <span className="block text-xs text-[#77736c] dark:text-[#8f9691]">Current cycle</span>
          <strong className="mt-2 mb-0.5 block text-[#111111] dark:text-[#f3f4f2]">May revenue close</strong>
          <small className="block text-xs text-[#77736c] dark:text-[#8f9691]">72% complete</small>
        </div>
      </aside>

      <section className="min-w-0 p-7 max-[720px]:p-3.5">
        <header className="mb-6 flex items-center justify-between gap-6 text-left max-[720px]:grid max-[720px]:grid-cols-1">
          <div>
            <p className={eyebrowClass}>Revenue Assurance Command Center</p>
            <h1 className="max-w-[760px] text-[clamp(34px,5vw,68px)] leading-[0.98] font-semibold text-balance text-[#111111] dark:text-[#f3f4f2]">
              Manage controls, leakage, and exception recovery.
            </h1>
          </div>
          <div className="flex shrink-0 items-center gap-2.5 max-[720px]:w-full">
            <button className="min-h-[38px] w-[38px] rounded-lg border border-[#e4e1da] bg-white/90 text-xl text-[#111111] transition hover:-translate-y-px hover:shadow-[0_14px_32px_rgba(17,17,17,0.1)] dark:border-[#29302d] dark:bg-[#1a1e1c] dark:text-[#f3f4f2]" type="button" aria-label="Search controls">⌕</button>
            <button className="min-h-[38px] w-[38px] rounded-lg border border-[#e4e1da] bg-white/90 text-xl text-[#111111] transition hover:-translate-y-px hover:shadow-[0_14px_32px_rgba(17,17,17,0.1)] dark:border-[#29302d] dark:bg-[#1a1e1c] dark:text-[#f3f4f2]" type="button" aria-label="Notifications">◌</button>
            <button
              className="min-h-[38px] rounded-lg border border-[#e4e1da] bg-white/90 px-3.5 font-semibold text-[#111111] transition hover:-translate-y-px hover:shadow-[0_14px_32px_rgba(17,17,17,0.1)] dark:border-[#29302d] dark:bg-[#1a1e1c] dark:text-[#f3f4f2]"
              type="button"
              aria-pressed={isDarkMode}
              onClick={() => setIsDarkMode((currentMode) => !currentMode)}
            >
              {isDarkMode ? 'Light' : 'Dark'}
            </button>
            <button className={`${primaryButtonClass} max-[720px]:flex-1`} type="button">New control</button>
          </div>
        </header>

        <section className="mb-3 grid grid-cols-4 gap-3 max-[1120px]:grid-cols-2 max-[720px]:grid-cols-1" id="overview" aria-label="Control performance summary">
          {controlStats.map((stat) => (
            <article className="rounded-lg border border-[#e4e1da] bg-white/90 p-[18px] text-left shadow-[0_1px_2px_rgba(17,17,17,0.04)] transition-colors duration-300 dark:border-[#29302d] dark:bg-[#171b19]" key={stat.label}>
              <span className="text-[#77736c] dark:text-[#8f9691]">{stat.label}</span>
              <strong className="mt-2.5 mb-1 block text-[32px] leading-none font-semibold tracking-normal text-[#111111] dark:text-[#f3f4f2]">{stat.value}</strong>
              <small className={statTone[stat.tone]}>{stat.trend}</small>
            </article>
          ))}
        </section>

        <section className="grid grid-cols-[minmax(0,1fr)_360px] gap-3 max-[1120px]:grid-cols-1">
          <div className="grid content-start gap-3">
            <section className={panelClass} id="controls">
              <div className="mb-[18px] flex items-center justify-between gap-4">
                <div>
                  <p className={eyebrowClass}>Control register</p>
                  <h2 className="text-xl leading-tight font-semibold text-[#111111] dark:text-[#f3f4f2]">Active revenue assurance controls</h2>
                </div>
                <button className={ghostButtonClass} type="button">Export</button>
              </div>

              <div className="grid gap-0.5 overflow-x-auto" role="table" aria-label="Active controls">
                <div className="grid min-w-[760px] grid-cols-[minmax(260px,1.8fr)_1fr_0.75fr_0.9fr_0.75fr] items-center gap-4 rounded-lg px-3 py-3.5 text-xs font-bold uppercase tracking-[0.06em] text-[#77736c] dark:text-[#8f9691]" role="row">
                  <span>Control</span>
                  <span>Owner</span>
                  <span>Exposure</span>
                  <span>Status</span>
                  <span>Score</span>
                </div>
                {controls.map((control) => (
                  <div className="grid min-w-[760px] grid-cols-[minmax(260px,1.8fr)_1fr_0.75fr_0.9fr_0.75fr] items-center gap-4 rounded-lg px-3 py-3.5 hover:bg-[#fbfbf8] dark:hover:bg-[#202622]" role="row" key={control.id}>
                    <span>
                      <strong className="block font-semibold text-[#111111] dark:text-[#f3f4f2]">{control.name}</strong>
                      <small className="text-[#77736c] dark:text-[#8f9691]">{control.id} · {control.domain}</small>
                    </span>
                    <span>{control.owner}</span>
                    <span>{control.exposure}</span>
                    <span>
                      <mark className="whitespace-nowrap rounded-full bg-[rgba(16,163,127,0.12)] px-2 py-1 text-[#08745c] dark:bg-[rgba(16,185,129,0.18)] dark:text-[#5ee0be]">{control.status}</mark>
                    </span>
                    <span className="flex items-center gap-2 font-semibold text-[#111111] dark:text-[#f3f4f2]">
                      <i className="h-[7px] w-14 rounded-full bg-[#e4e1da] dark:bg-[#29302d]" aria-hidden="true">
                        <span className="block h-full rounded-full bg-[#10a37f]" style={{ width: `${control.score}%` }} />
                      </i>
                      {control.score}
                    </span>
                  </div>
                ))}
              </div>
            </section>

            <section className={`${panelClass} grid grid-cols-[220px_minmax(0,1fr)] gap-6 max-[720px]:grid-cols-1`} id="evidence">
              <div>
                <p className={eyebrowClass}>Close workflow</p>
                <h2 className="text-xl leading-tight font-semibold text-[#111111] dark:text-[#f3f4f2]">Reconciliation timeline</h2>
              </div>
              <div className="grid gap-3">
                {timeline.map(([time, title, detail]) => (
                  <div className="grid grid-cols-[62px_minmax(0,1fr)] items-start gap-3.5" key={time}>
                    <time className="font-bold text-[#08745c] dark:text-[#5ee0be]">{time}</time>
                    <div>
                      <strong className="block font-semibold text-[#111111] dark:text-[#f3f4f2]">{title}</strong>
                      <span className="text-[#77736c] dark:text-[#8f9691]">{detail}</span>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          </div>

          <aside className="grid content-start gap-3">
            <section className="rounded-lg border border-[#e4e1da] bg-[#101010] bg-[linear-gradient(145deg,rgba(16,185,129,0.14),transparent_50%)] p-5 text-left text-white/75 shadow-[0_1px_2px_rgba(17,17,17,0.04)] dark:border-[#29302d]">
              <p className="mb-2 block text-xs font-bold uppercase tracking-[0.08em] text-white">AI review</p>
              <h2 className="text-xl leading-tight font-semibold text-white">Suggested next action</h2>
              <p className="mb-[18px]">
                Prioritize RA-203. Exposure is rising and partner evidence is incomplete for the
                last two settlement files.
              </p>
              <button className="min-h-[38px] rounded-lg bg-white px-4 font-semibold text-[#111111] transition hover:-translate-y-px hover:shadow-[0_14px_32px_rgba(17,17,17,0.1)]" type="button">Draft remediation</button>
            </section>

            <section className={panelClass} id="exceptions">
              <div className="mb-3 flex items-center justify-between gap-4">
                <div>
                  <p className={eyebrowClass}>Exceptions</p>
                  <h2 className="text-xl leading-tight font-semibold text-[#111111] dark:text-[#f3f4f2]">Live alerts</h2>
                </div>
                <span className="grid h-7 min-w-7 place-items-center rounded-full bg-[rgba(16,163,127,0.12)] font-bold text-[#08745c] dark:bg-[rgba(16,185,129,0.18)] dark:text-[#5ee0be]">3</span>
              </div>
              <div className="grid gap-2.5">
                {alerts.map((alert) => (
                  <article className="rounded-lg border border-[#e4e1da] bg-[#fbfbf8] p-3.5 dark:border-[#29302d] dark:bg-[#202622]" key={alert.title}>
                    <strong className="block font-semibold text-[#111111] dark:text-[#f3f4f2]">{alert.title}</strong>
                    <span className="text-[#77736c] dark:text-[#8f9691]">{alert.detail}</span>
                    <time className="mt-2 block text-xs text-[#77736c] dark:text-[#8f9691]">{alert.time}</time>
                  </article>
                ))}
              </div>
            </section>
          </aside>
            <div>
        {loading && <p>Loading...</p>}
        {!loading && exceptions.length === 0? 
            <p>No exceptions found.</p>:
            exceptions.map((exception) => (
              <div key={exception.account_number}>
                <h3>{exception.email}</h3>
                <p>{exception.status}</p>
              </div>
            )) }
      </div>
        </section>
      </section>
    
    </main>
  )
}

export default App
