/**
 * SVG circuit primitives. Coordinates are SVG user units on a 12-unit grid.
 * Two drawing styles (DrawStyleContext): 'symbol' (proper transistor symbols) and 'box'
 * (the simplified coloured boxes from the conversation: NMOS purple, PMOS teal, passives gray).
 */
import { createContext, useContext, type ReactNode } from 'react';
import type { Region } from '../physics';

export type DrawStyle = 'symbol' | 'box';
export const DrawStyleContext = createContext<DrawStyle>('symbol');
/** Ids of elements to emphasise (signal path, the device a step talks about). */
export const HighlightContext = createContext<ReadonlySet<string>>(new Set());

const INK = 'var(--ink)';
const HL = 'var(--signal)';

function useHL(id?: string): boolean {
  const set = useContext(HighlightContext);
  return !!id && set.has(id);
}

export function stroke(hl: boolean, base = INK) {
  return { stroke: hl ? HL : base, strokeWidth: hl ? 3 : 1.5 };
}

// ─── Wires, nodes, rails ───────────────────────────────────────────────────

export function Wire({ points, id, dashed }: { points: Array<[number, number]>; id?: string; dashed?: boolean }) {
  const hl = useHL(id);
  return (
    <polyline
      points={points.map((p) => p.join(',')).join(' ')}
      fill="none"
      {...stroke(hl)}
      strokeLinejoin="round"
      strokeLinecap="round"
      strokeDasharray={dashed ? '4 4' : undefined}
    />
  );
}

export function Dot({ x, y, id }: { x: number; y: number; id?: string }) {
  const hl = useHL(id);
  return <circle cx={x} cy={y} r={hl ? 4.5 : 3} fill={hl ? HL : INK} />;
}

/** Open terminal (input/output pin). */
export function Terminal({ x, y }: { x: number; y: number }) {
  return <circle cx={x} cy={y} r={3.5} fill="var(--paper)" stroke={INK} strokeWidth={1.5} />;
}

export function Rail({ x1, x2, y, label, labelSide = 'right' }: { x1: number; x2: number; y: number; label?: string; labelSide?: 'left' | 'right' }) {
  return (
    <g>
      <line x1={x1} x2={x2} y1={y} y2={y} stroke={INK} strokeWidth={3} strokeLinecap="round" />
      {label && (
        <Label x={labelSide === 'right' ? x2 + 6 : x1 - 6} y={y + 4} anchor={labelSide === 'right' ? 'start' : 'end'} text={label} weight={600} />
      )}
    </g>
  );
}

export function Ground({ x, y }: { x: number; y: number }) {
  return (
    <g stroke={INK} strokeWidth={1.5} strokeLinecap="round">
      <line x1={x} y1={y} x2={x} y2={y + 6} />
      <line x1={x - 10} y1={y + 6} x2={x + 10} y2={y + 6} />
      <line x1={x - 6} y1={y + 10} x2={x + 6} y2={y + 10} />
      <line x1={x - 2} y1={y + 14} x2={x + 2} y2={y + 14} />
    </g>
  );
}

// ─── Labels ────────────────────────────────────────────────────────────────

export function Label({
  x,
  y,
  text,
  anchor = 'start',
  color = INK,
  size = 13,
  weight = 400,
  mono = false,
  bg = false,
}: {
  x: number;
  y: number;
  text: ReactNode;
  anchor?: 'start' | 'middle' | 'end';
  color?: string;
  size?: number;
  weight?: number;
  mono?: boolean;
  bg?: boolean;
}) {
  return (
    <text
      x={x}
      y={y}
      textAnchor={anchor}
      fill={color}
      fontSize={size}
      fontWeight={weight}
      fontFamily={mono ? 'var(--font-mono)' : 'var(--font-sans)'}
      paintOrder={bg ? 'stroke' : undefined}
      stroke={bg ? 'var(--paper)' : undefined}
      strokeWidth={bg ? 4 : undefined}
      strokeLinejoin="round"
    >
      {text}
    </text>
  );
}

/** Subscripted symbol like V_{DD} as SVG tspans: sym("V","DD"). */
export function Sym({ base, sub }: { base: string; sub?: string }) {
  return (
    <>
      {base}
      {sub && (
        <tspan baselineShift="sub" fontSize="0.75em">
          {sub}
        </tspan>
      )}
    </>
  );
}

/** A live node voltage tag, e.g. "0.90 V", in the mono face. */
export function VoltageTag({ x, y, v, anchor = 'start', id }: { x: number; y: number; v: string; anchor?: 'start' | 'middle' | 'end'; id?: string }) {
  const hl = useHL(id);
  return <Label x={x} y={y} text={v} anchor={anchor} mono size={12} color={hl ? HL : 'var(--ink-2)'} weight={hl ? 600 : 400} bg />;
}

// ─── Passives ──────────────────────────────────────────────────────────────

/** Vertical resistor between (x,y1) and (x,y2); zigzag in the middle 36 units. */
export function Resistor({ x, y1, y2, label, value, id, labelSide = 'right' }: { x: number; y1: number; y2: number; label?: ReactNode; value?: string; id?: string; labelSide?: 'left' | 'right' }) {
  const style = useContext(DrawStyleContext);
  const hl = useHL(id);
  const mid = (y1 + y2) / 2;
  const h = Math.min(36, Math.abs(y2 - y1) - 8);
  const top = mid - h / 2;
  const bottom = mid + h / 2;
  const tx = labelSide === 'right' ? x + 12 : x - 12;
  const anchor = labelSide === 'right' ? 'start' : 'end';
  let body: ReactNode;
  if (style === 'box') {
    body = <rect x={x - 6} y={top} width={12} height={h} rx={2} fill="color-mix(in srgb, var(--muted) 18%, var(--paper))" {...stroke(hl, 'var(--muted)')} />;
  } else {
    const n = 6;
    const seg = h / n;
    const pts: Array<[number, number]> = [[x, top]];
    for (let i = 0; i < n; i++) pts.push([x + (i % 2 === 0 ? 7 : -7), top + seg * (i + 0.5)]);
    pts.push([x, bottom]);
    body = <polyline points={pts.map((p) => p.join(',')).join(' ')} fill="none" {...stroke(hl)} strokeLinejoin="round" />;
  }
  return (
    <g>
      <line x1={x} y1={y1} x2={x} y2={top} {...stroke(hl)} />
      {body}
      <line x1={x} y1={bottom} x2={x} y2={y2} {...stroke(hl)} />
      {label && <Label x={tx} y={mid - (value ? 7 : -4)} text={label} anchor={anchor} />}
      {value && <Label x={tx} y={mid + 15} text={value} anchor={anchor} mono size={12} color="var(--ink-2)" />}
    </g>
  );
}

/** Horizontal resistor between (x1,y) and (x2,y). */
export function ResistorH({ x1, x2, y, label, id }: { x1: number; x2: number; y: number; label?: ReactNode; id?: string }) {
  const hl = useHL(id);
  const mid = (x1 + x2) / 2;
  const w = Math.min(36, Math.abs(x2 - x1) - 8);
  const l = mid - w / 2;
  const n = 6;
  const pts: Array<[number, number]> = [[l, y]];
  for (let i = 0; i < n; i++) pts.push([l + (w / n) * (i + 0.5), y + (i % 2 === 0 ? -7 : 7)]);
  pts.push([l + w, y]);
  return (
    <g>
      <line x1={x1} y1={y} x2={l} y2={y} {...stroke(hl)} />
      <polyline points={pts.map((p) => p.join(',')).join(' ')} fill="none" {...stroke(hl)} />
      <line x1={l + w} y1={y} x2={x2} y2={y} {...stroke(hl)} />
      {label && <Label x={mid} y={y - 12} text={label} anchor="middle" />}
    </g>
  );
}

export function Capacitor({ x, y1, y2, label, id }: { x: number; y1: number; y2: number; label?: ReactNode; id?: string }) {
  const hl = useHL(id);
  const mid = (y1 + y2) / 2;
  return (
    <g>
      <line x1={x} y1={y1} x2={x} y2={mid - 4} {...stroke(hl)} />
      <line x1={x - 12} y1={mid - 4} x2={x + 12} y2={mid - 4} {...stroke(hl)} strokeWidth={2.5} />
      <line x1={x - 12} y1={mid + 4} x2={x + 12} y2={mid + 4} {...stroke(hl)} strokeWidth={2.5} />
      <line x1={x} y1={mid + 4} x2={x} y2={y2} {...stroke(hl)} />
      {label && <Label x={x + 16} y={mid + 4} text={label} />}
    </g>
  );
}

/** Current source (circle with arrow) between (x,y1) top and (x,y2) bottom; arrow points down by default. */
export function CurrentSource({ x, y1, y2, label, value, id, up = false, labelSide = 'right' }: { x: number; y1: number; y2: number; label?: ReactNode; value?: string; id?: string; up?: boolean; labelSide?: 'left' | 'right' }) {
  const hl = useHL(id);
  const mid = (y1 + y2) / 2;
  const r = 12;
  const tx = labelSide === 'right' ? x + r + 6 : x - r - 6;
  const anchor = labelSide === 'right' ? 'start' : 'end';
  return (
    <g>
      <line x1={x} y1={y1} x2={x} y2={mid - r} {...stroke(hl)} />
      <circle cx={x} cy={mid} r={r} fill="var(--paper)" {...stroke(hl)} />
      <line x1={x} y1={mid + (up ? 7 : -7)} x2={x} y2={mid + (up ? -7 : 7)} {...stroke(hl)} />
      <polyline
        points={up ? `${x - 4},${mid - 3} ${x},${mid - 8} ${x + 4},${mid - 3}` : `${x - 4},${mid + 3} ${x},${mid + 8} ${x + 4},${mid + 3}`}
        fill="none"
        {...stroke(hl)}
      />
      <line x1={x} y1={mid + r} x2={x} y2={y2} {...stroke(hl)} />
      {label && <Label x={tx} y={mid - (value ? 2 : -4)} text={label} anchor={anchor} />}
      {value && <Label x={tx} y={mid + 13} text={value} anchor={anchor} mono size={12} color="var(--ink-2)" />}
    </g>
  );
}

/** Voltage source (circle with + and −) between (x,y1) top (+) and (x,y2) bottom (−). */
export function VoltageSource({ x, y1, y2, label }: { x: number; y1: number; y2: number; label?: ReactNode }) {
  const mid = (y1 + y2) / 2;
  const r = 12;
  return (
    <g>
      <line x1={x} y1={y1} x2={x} y2={mid - r} stroke={INK} strokeWidth={1.5} />
      <circle cx={x} cy={mid} r={r} fill="var(--paper)" stroke={INK} strokeWidth={1.5} />
      <Label x={x} y={mid - 3} text="+" anchor="middle" size={10} />
      <Label x={x} y={mid + 11} text="−" anchor="middle" size={10} />
      <line x1={x} y1={mid + r} x2={x} y2={y2} stroke={INK} strokeWidth={1.5} />
      {label && <Label x={x - r - 6} y={mid + 4} text={label} anchor="end" />}
    </g>
  );
}

/** Arrow showing a current along a vertical or horizontal wire, with an optional label. */
export function CurrentArrow({ x, y, dir = 'down', label, color = HL }: { x: number; y: number; dir?: 'down' | 'up' | 'left' | 'right'; label?: ReactNode; color?: string }) {
  const rot = { down: 0, up: 180, left: 90, right: -90 }[dir];
  return (
    <g>
      <g transform={`translate(${x},${y}) rotate(${rot})`}>
        <polygon points="-5,-4 5,-4 0,5" fill={color} />
      </g>
      {label && (
        <Label x={dir === 'left' || dir === 'right' ? x : x + 9} y={dir === 'left' || dir === 'right' ? y - 9 : y + 4} text={label} anchor={dir === 'left' || dir === 'right' ? 'middle' : 'start'} color={color} size={12} mono />
      )}
    </g>
  );
}

// ─── Transistors ───────────────────────────────────────────────────────────

export interface MosProps {
  /** Centre of the device. Gate lead ends at (x−30, y); drain/source leads end at (x, y∓30). */
  x: number;
  y: number;
  name?: string;
  id?: string;
  /** Gate on the right instead of the left. */
  flip?: boolean;
  region?: Region;
  current?: string;
  /** Diode connection: draw the gate tied to the drain. */
  diode?: boolean;
}

export const REGION_TEXT: Record<Region, string> = { off: 'OFF', triode: 'TRI', saturation: 'SAT' };

export function RegionBadge({ x, y, region, anchor = 'start' }: { x: number; y: number; region: Region; anchor?: 'start' | 'end' }) {
  const ok = region === 'saturation';
  const color = ok ? 'var(--ok)' : 'var(--bad)';
  const w = 30;
  const bx = anchor === 'start' ? x : x - w;
  return (
    <g>
      <rect x={bx} y={y - 10} width={w} height={14} rx={3} fill="var(--paper)" stroke={color} strokeWidth={1.2} />
      <Label x={bx + w / 2} y={y + 1} text={REGION_TEXT[region]} anchor="middle" size={10} mono color={color} weight={600} />
    </g>
  );
}

function MosBody({ x, y, kind, hl, flip }: { x: number; y: number; kind: 'n' | 'p'; hl: boolean; flip?: boolean }) {
  const style = useContext(DrawStyleContext);
  const color = kind === 'n' ? 'var(--nmos)' : 'var(--pmos)';
  const s = flip ? -1 : 1;
  const X = (dx: number) => x + s * dx;
  if (style === 'box') {
    return (
      <g>
        <line x1={X(-30)} y1={y} x2={X(-14)} y2={y} {...stroke(hl)} />
        <rect
          x={Math.min(X(-14), X(4))}
          y={y - 18}
          width={18}
          height={36}
          rx={3}
          fill={`color-mix(in srgb, ${color} 22%, var(--paper))`}
          stroke={hl ? HL : color}
          strokeWidth={hl ? 3 : 2}
        />
        <Label x={X(-5)} y={y + 4} text={kind === 'n' ? 'N' : 'P'} anchor="middle" size={12} weight={700} color={color} />
        <line x1={X(0)} y1={y - 18} x2={X(0)} y2={y - 30} {...stroke(hl)} />
        <line x1={X(0)} y1={y + 18} x2={X(0)} y2={y + 30} {...stroke(hl)} />
      </g>
    );
  }
  const ch = { stroke: hl ? HL : color, strokeWidth: hl ? 3.5 : 3 };
  // Arrow on the source leg: NMOS points out of the channel (source at bottom), PMOS points in (source at top).
  const srcY = kind === 'n' ? y + 12 : y - 12;
  const arrow =
    kind === 'n'
      ? `${X(-1)},${srcY - 4} ${X(-1)},${srcY + 4} ${X(4)},${srcY}`
      : `${X(0)},${srcY - 4} ${X(0)},${srcY + 4} ${X(-5)},${srcY}`;
  return (
    <g>
      <line x1={X(-30)} y1={y} x2={X(-13)} y2={y} {...stroke(hl)} />
      <line x1={X(-13)} y1={y - 12} x2={X(-13)} y2={y + 12} {...stroke(hl)} strokeWidth={2} />
      <line x1={X(-8)} y1={y - 17} x2={X(-8)} y2={y + 17} {...ch} />
      <polyline points={`${X(-8)},${y - 12} ${X(0)},${y - 12} ${X(0)},${y - 30}`} fill="none" {...stroke(hl)} />
      <polyline points={`${X(-8)},${y + 12} ${X(0)},${y + 12} ${X(0)},${y + 30}`} fill="none" {...stroke(hl)} />
      <polygon points={arrow} fill={hl ? HL : color} />
    </g>
  );
}

function MosAnnotations({ x, y, name, flip, region, current, kind }: MosProps & { kind: 'n' | 'p' }) {
  const color = kind === 'n' ? 'var(--nmos)' : 'var(--pmos)';
  const s = flip ? -1 : 1;
  const tx = x + s * 8;
  const anchor = flip ? 'end' : 'start';
  return (
    <g>
      {name && <Label x={tx} y={y - 4} text={name} anchor={anchor} color={color} weight={600} bg />}
      {region && <RegionBadge x={tx} y={y + 14} region={region} anchor={anchor} />}
      {current && <Label x={region ? tx + s * 36 : tx} y={y + 15} text={current} anchor={anchor} mono size={11} color="var(--ink-2)" bg />}
    </g>
  );
}

export function Nmos(p: MosProps) {
  const hl = useHL(p.id);
  const s = p.flip ? -1 : 1;
  return (
    <g data-id={p.id}>
      <MosBody x={p.x} y={p.y} kind="n" hl={hl} flip={p.flip} />
      {p.diode && <polyline points={`${p.x - s * 30},${p.y} ${p.x - s * 30},${p.y - 24} ${p.x},${p.y - 24}`} fill="none" {...stroke(hl)} />}
      {p.diode && <Dot x={p.x} y={p.y - 24} />}
      <MosAnnotations {...p} kind="n" />
    </g>
  );
}

export function Pmos(p: MosProps) {
  const hl = useHL(p.id);
  const s = p.flip ? -1 : 1;
  return (
    <g data-id={p.id}>
      <MosBody x={p.x} y={p.y} kind="p" hl={hl} flip={p.flip} />
      {p.diode && <polyline points={`${p.x - s * 30},${p.y} ${p.x - s * 30},${p.y + 24} ${p.x},${p.y + 24}`} fill="none" {...stroke(hl)} />}
      {p.diode && <Dot x={p.x} y={p.y + 24} />}
      <MosAnnotations {...p} kind="p" />
    </g>
  );
}

/** Simple op-amp triangle; inputs at (x−36, y∓12), output at (x+36, y). */
export function OpAmp({ x, y, id }: { x: number; y: number; id?: string }) {
  const hl = useHL(id);
  return (
    <g>
      <polygon points={`${x - 30},${y - 30} ${x - 30},${y + 30} ${x + 30},${y}`} fill="var(--paper)" {...stroke(hl)} />
      <Label x={x - 24} y={y - 8} text="+" size={13} />
      <Label x={x - 24} y={y + 17} text="−" size={13} />
      <line x1={x - 36} y1={y - 12} x2={x - 30} y2={y - 12} stroke={INK} strokeWidth={1.5} />
      <line x1={x - 36} y1={y + 12} x2={x - 30} y2={y + 12} stroke={INK} strokeWidth={1.5} />
      <line x1={x + 30} y1={y} x2={x + 36} y2={y} stroke={INK} strokeWidth={1.5} />
    </g>
  );
}

// ─── Frame ─────────────────────────────────────────────────────────────────

/** Responsive SVG canvas: scales to its container but never beyond maxWidth. */
export function Canvas({ w, h, children, title, maxWidth, highlight, style }: { w: number; h: number; children: ReactNode; title: string; maxWidth?: number; highlight?: string[]; style?: DrawStyle }) {
  const outerStyle = useContext(DrawStyleContext);
  const svg = (
    <svg
      viewBox={`0 0 ${w} ${h}`}
      role="img"
      aria-label={title}
      style={{ width: '100%', maxWidth: maxWidth ?? w * 1.25, height: 'auto', display: 'block', overflow: 'visible' }}
    >
      <title>{title}</title>
      {children}
    </svg>
  );
  return (
    <DrawStyleContext.Provider value={style ?? outerStyle}>
      <HighlightContext.Provider value={new Set(highlight ?? [])}>{svg}</HighlightContext.Provider>
    </DrawStyleContext.Provider>
  );
}
