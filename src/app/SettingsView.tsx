import { useRef, useState } from 'react';
import { exportProgress, importProgress, resetProgress, setSettings, useProgress } from './store';

export function SettingsView() {
  const p = useProgress();
  const s = p.settings;
  const file = useRef<HTMLInputElement>(null);
  const [msg, setMsg] = useState<string | null>(null);

  const download = () => {
    const blob = new Blob([exportProgress()], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `analog-gym-progress-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(a.href);
  };

  return (
    <div className="page narrow">
      <h1>Settings</h1>
      <div className="settings">
        <label>
          Theme
          <select value={s.theme} onChange={(e) => setSettings({ theme: e.target.value as typeof s.theme })}>
            <option value="auto">Follow system</option>
            <option value="light">Light</option>
            <option value="dark">Dark</option>
          </select>
        </label>
        <label>
          Circuit drawing style
          <select value={s.drawStyle} onChange={(e) => setSettings({ drawStyle: e.target.value as typeof s.drawStyle })}>
            <option value="symbol">Transistor symbols (as in your notes)</option>
            <option value="box">Simplified labelled boxes</option>
          </select>
        </label>
        <label>
          Answer tolerance
          <select value={s.tol} onChange={(e) => setSettings({ tol: Number(e.target.value) })}>
            <option value={0.01}>±1%</option>
            <option value={0.02}>±2%</option>
            <option value={0.05}>±5%</option>
          </select>
        </label>
        <label className="check">
          <input type="checkbox" checked={s.unlockAll} onChange={(e) => setSettings({ unlockAll: e.target.checked })} />
          Unlock every unit (override mastery gating)
        </label>
      </div>

      <h2>Your progress file</h2>
      <p className="small muted">Progress is stored in this browser. Export it to move it to your phone or keep a backup.</p>
      <div className="row">
        <button type="button" className="btn" onClick={download}>
          Export progress (.json)
        </button>
        <button type="button" className="btn" onClick={() => file.current?.click()}>
          Import progress…
        </button>
        <input
          ref={file}
          type="file"
          accept="application/json,.json"
          hidden
          onChange={async (e) => {
            const f = e.target.files?.[0];
            if (!f) return;
            const r = importProgress(await f.text());
            setMsg(r.ok ? 'Progress imported.' : r.error ?? 'Import failed.');
          }}
        />
        <button
          type="button"
          className="btn ghost"
          onClick={() => {
            if (confirm('Erase all lessons, cards and the mistake log? Settings are kept.')) resetProgress();
          }}
        >
          Reset progress
        </button>
      </div>
      {msg && <p className="callout small">{msg}</p>}
    </div>
  );
}
