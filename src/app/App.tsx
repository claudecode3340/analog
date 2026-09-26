import { useEffect, useState } from 'react';
import { DrawStyleContext } from '../circuits/primitives';
import { LessonView } from '../learn/LessonView';
import { LearnIndex } from '../learn/LearnIndex';
import { DcStepper } from '../labs/DcStepper';
import { LabsIndex } from '../labs/LabsIndex';
import { MosfetLab } from '../labs/MosfetLab';
import { PracticeView } from '../practice/PracticeView';
import { ReviewView } from '../review/ReviewView';
import { Gallery } from './Gallery';
import { PathView } from './PathView';
import { SettingsView } from './SettingsView';
import { today, useProgress } from './store';

function useHash(): string {
  const [h, setH] = useState(() => window.location.hash || '#/path');
  useEffect(() => {
    const on = () => setH(window.location.hash || '#/path');
    window.addEventListener('hashchange', on);
    return () => window.removeEventListener('hashchange', on);
  }, []);
  return h;
}

const NAV = [
  { key: '1', href: '#/path', label: 'Path', match: 'path' },
  { key: '2', href: '#/learn', label: 'Learn', match: 'learn' },
  { key: '3', href: '#/labs', label: 'Labs', match: 'labs' },
  { key: '4', href: '#/practice', label: 'Practice', match: 'practice' },
  { key: '5', href: '#/review', label: 'Review', match: 'review' },
];

export function App() {
  const hash = useHash();
  const p = useProgress();
  const [, section, arg] = hash.split('/');

  useEffect(() => {
    const root = document.documentElement;
    if (p.settings.theme === 'auto') root.removeAttribute('data-theme');
    else root.setAttribute('data-theme', p.settings.theme);
  }, [p.settings.theme]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const t = e.target as HTMLElement;
      if (t.closest('input, textarea, select, [contenteditable]') || e.metaKey || e.ctrlKey || e.altKey) return;
      const n = NAV.find((x) => x.key === e.key);
      if (n) window.location.hash = n.href;
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);

  const due = Object.values(p.cards).filter((c) => c.due <= today()).length;

  let view: React.ReactNode;
  switch (section) {
    case 'learn':
      view = arg ? <LessonView id={arg} /> : <LearnIndex />;
      break;
    case 'labs':
      view = arg === 'mosfet' ? <MosfetLab /> : arg === 'dc' ? <DcStepper /> : <LabsIndex />;
      break;
    case 'practice':
      view = <PracticeView />;
      break;
    case 'review':
      view = <ReviewView />;
      break;
    case 'settings':
      view = <SettingsView />;
      break;
    case 'gallery':
      view = <Gallery />;
      break;
    default:
      view = <PathView />;
  }

  return (
    <DrawStyleContext.Provider value={p.settings.drawStyle}>
      <a className="skip" href="#main">
        Skip to content
      </a>
      <header className="topbar">
        <a className="brand" href="#/path" aria-label="Analog Gym home">
          <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true">
            <path d="M3 12h4l2-6 4 12 2-6h6" fill="none" stroke="var(--signal)" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
          <span>Analog Gym</span>
        </a>
        <nav className="mainnav" aria-label="Main">
          {NAV.map((n) => (
            <a key={n.href} href={n.href} className={section === n.match || (!section && n.match === 'path') ? 'active' : ''} aria-current={section === n.match ? 'page' : undefined} title={`${n.label} (key ${n.key})`}>
              {n.label}
              {n.match === 'review' && due > 0 && <span className="pill">{due}</span>}
            </a>
          ))}
          <a href="#/settings" className={section === 'settings' ? 'active' : ''} aria-label="Settings" title="Settings">
            ⚙
          </a>
        </nav>
      </header>
      <main id="main">{view}</main>
    </DrawStyleContext.Provider>
  );
}
