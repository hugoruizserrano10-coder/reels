import React from 'react';
import {
  AbsoluteFill, Audio, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, Easing,
} from 'remotion';

// ---------- tipos ----------
export type Word = {t0: number; t1: number; w: string};
export type Scene = {
  type: 'hook' | 'notifs' | 'chat' | 'agenda' | 'stat' | 'cta' | 'lista';
  from: number; dur: number;
  [k: string]: unknown;
};
export type ReelProps = {
  scenes: Scene[]; words: Word[]; voice: string | null; music: string | null;
  totalFrames: number; brand: string; musicVol?: number; sfx?: {t: number; s: string; v?: number}[];
};

// ---------- estilo ----------
const C = {
  bg1: '#FBF6EF', bg2: '#FFE9D9', ink: '#17130F', soft: '#6E655C', orange: '#FF5A14', orange2: '#FF8A3D',
  green: '#22C55E', card: '#FFFFFF', line: 'rgba(23,19,15,0.08)',
};
const fontCss = `
@font-face{font-family:'InterD';src:url(${staticFile('fonts/InterDisplay-Black.woff2')}) format('woff2');font-weight:900}
@font-face{font-family:'Inter';src:url(${staticFile('fonts/Inter-Regular.woff2')}) format('woff2');font-weight:400}
@font-face{font-family:'Inter';src:url(${staticFile('fonts/Inter-SemiBold.woff2')}) format('woff2');font-weight:600}
@font-face{font-family:'Inter';src:url(${staticFile('fonts/Inter-Bold.woff2')}) format('woff2');font-weight:700}
`;
const shadow = '0 30px 80px rgba(80,40,10,0.16), 0 6px 18px rgba(80,40,10,0.10)';

const useSpring = (delay = 0, cfg: {damping?: number; mass?: number; stiffness?: number} = {}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  return spring({frame: f - delay, fps, config: {damping: 14, mass: 0.7, stiffness: 160, ...cfg}});
};

// ---------- fondo vivo ----------
const Fondo: React.FC = () => {
  const f = useCurrentFrame();
  const b = (i: number) => ({
    x: 50 + 30 * Math.sin(f / (90 + i * 23) + i * 2), y: 40 + 25 * Math.cos(f / (110 + i * 17) + i),
  });
  const p = [b(0), b(1), b(2)];
  return (
    <AbsoluteFill style={{background: `linear-gradient(170deg, ${C.bg1} 0%, ${C.bg1} 55%, ${C.bg2} 100%)`}}>
      <AbsoluteFill style={{
        background: `radial-gradient(circle at ${p[0].x}% ${p[0].y}%, rgba(255,138,61,0.22), transparent 38%),
                     radial-gradient(circle at ${p[1].x}% ${p[1].y + 30}%, rgba(255,90,20,0.12), transparent 40%),
                     radial-gradient(circle at ${p[2].x - 20}% ${p[2].y + 10}%, rgba(255,200,150,0.25), transparent 45%)`,
      }} />
      <AbsoluteFill style={{
        backgroundImage: 'radial-gradient(rgba(23,19,15,0.07) 2px, transparent 2.5px)', backgroundSize: '44px 44px',
        maskImage: 'linear-gradient(to bottom, transparent, black 30%, black 70%, transparent)',
        transform: `translateY(${-(f * 0.4) % 44}px)`,
      }} />
    </AbsoluteFill>
  );
};

// ---------- entrada de escena (cámara) ----------
const Entrada: React.FC<{children: React.ReactNode; dur: number}> = ({children, dur}) => {
  const f = useCurrentFrame();
  const s = useSpring(0, {damping: 18, stiffness: 120});
  const zoom = interpolate(f, [0, dur], [1, 1.045]);
  const blur = interpolate(s, [0, 1], [14, 0]);
  return (
    <AbsoluteFill style={{
      transform: `scale(${interpolate(s, [0, 1], [0.9, 1]) * zoom}) translateY(${interpolate(s, [0, 1], [60, 0])}px)`,
      opacity: interpolate(s, [0, 0.4], [0, 1], {extrapolateRight: 'clamp'}), filter: `blur(${blur}px)`,
    }}>{children}</AbsoluteFill>
  );
};

// ---------- piezas ----------
const Pill: React.FC<{children: React.ReactNode; bg?: string; color?: string; size?: number}> = ({children, bg = C.ink, color = '#fff', size = 34}) => (
  <span style={{background: bg, color, borderRadius: 999, padding: `${size * 0.35}px ${size * 0.8}px`, fontFamily: 'Inter', fontWeight: 700, fontSize: size, display: 'inline-flex', alignItems: 'center', gap: 12}}>{children}</span>
);

const TituloKinetico: React.FC<{lineas: [string, boolean][]; top: number; size?: number; delay?: number}> = ({lineas, top, size = 104, delay = 0}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  let k = 0;
  return (
    <div style={{position: 'absolute', top, left: 70, right: 70}}>
      {lineas.map(([txt, acento], li) => (
        <div key={li} style={{display: 'flex', flexWrap: 'wrap', gap: '0 22px', marginBottom: 6}}>
          {txt.split(' ').map((w, wi) => {
            const d = delay + (k++) * 3;
            const s = spring({frame: f - d, fps, config: {damping: 13, stiffness: 180, mass: 0.6}});
            return (
              <span key={wi} style={{
                fontFamily: 'InterD', fontWeight: 900, fontSize: size, lineHeight: 1.02, letterSpacing: -3,
                color: acento ? C.orange : C.ink, display: 'inline-block',
                transform: `translateY(${interpolate(s, [0, 1], [70, 0])}px) rotate(${interpolate(s, [0, 1], [6, 0])}deg)`,
                opacity: interpolate(s, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'}),
              }}>{w}</span>
            );
          })}
        </div>
      ))}
    </div>
  );
};

const Contador: React.FC<{valor: number; prefijo?: string; sufijo?: string; delay?: number; size?: number; color?: string}> = ({valor, prefijo = '', sufijo = '', delay = 0, size = 300, color = C.orange}) => {
  const f = useCurrentFrame();
  const v = Math.round(interpolate(f - delay, [0, 24], [0, valor], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)}));
  const s = useSpring(delay, {damping: 9, stiffness: 200});
  return <div style={{fontFamily: 'InterD', fontWeight: 900, fontSize: size, color, letterSpacing: -12, lineHeight: 1, transform: `scale(${interpolate(s, [0, 1], [0.6, 1])})`}}>{prefijo}{v}{sufijo}</div>;
};

// ---------- escenas ----------
const Hook: React.FC<{sc: Scene}> = ({sc}) => {
  const lineas = sc.titulo as [string, boolean][];
  const stat = sc.stat as {valor: number; prefijo?: string; sufijo?: string; etiqueta: string} | undefined;
  const s = useSpring(10);
  return (
    <AbsoluteFill>
      {sc.chip ? <div style={{position: 'absolute', top: 210, left: 70, opacity: s, transform: `translateY(${(1 - s) * 30}px)`}}><Pill bg={C.orange} size={32}>{String(sc.chip)}</Pill></div> : null}
      <TituloKinetico lineas={lineas} top={330} delay={4} size={122} />
      {stat ? (
        <div style={{position: 'absolute', top: 1000, left: 70, right: 70, background: C.card, borderRadius: 48, boxShadow: shadow, padding: '40px 56px', display: 'flex', alignItems: 'center', gap: 36, transform: `translateY(${(1 - useSpring(16)) * 200}px)`, opacity: useSpring(16)}}>
          <Contador valor={stat.valor} prefijo={stat.prefijo} sufijo={stat.sufijo} delay={20} size={190} />
          <div style={{fontFamily: 'Inter', fontWeight: 600, fontSize: 42, color: C.soft, lineHeight: 1.25}}>{stat.etiqueta}</div>
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

const Notifs: React.FC<{sc: Scene}> = ({sc}) => {
  const items = sc.items as {app: string; titulo: string; texto: string; hora: string}[];
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 230, width: '100%', textAlign: 'center', fontFamily: 'InterD', fontSize: 230, color: C.ink, letterSpacing: -8}}>{String(sc.reloj)}</div>
      <div style={{position: 'absolute', top: 500, width: '100%', textAlign: 'center', fontFamily: 'Inter', fontWeight: 600, fontSize: 42, color: C.soft}}>{String(sc.subreloj)}</div>
      {items.map((it, i) => {
        const s = spring({frame: f - 10 - i * 22, fps, config: {damping: 12, stiffness: 170, mass: 0.6}});
        return (
          <div key={i} style={{
            position: 'absolute', left: 60, right: 60, top: 640 + i * 200, height: 172, borderRadius: 44,
            background: 'rgba(255,255,255,0.86)', boxShadow: shadow, display: 'flex', alignItems: 'center', gap: 28, padding: '0 36px',
            transform: `translateY(${interpolate(s, [0, 1], [-160, 0])}px) scale(${interpolate(s, [0, 1], [0.85, 1])})`, opacity: s,
          }}>
            <div style={{width: 92, height: 92, borderRadius: 24, background: it.app === 'WhatsApp' ? '#25D366' : C.orange, color: '#fff', fontFamily: 'InterD', fontSize: 46, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>{it.app === 'WhatsApp' ? '✆' : '☎'}</div>
            <div style={{flex: 1, minWidth: 0}}>
              <div style={{display: 'flex', justifyContent: 'space-between', fontFamily: 'Inter', fontWeight: 700, fontSize: 36, color: C.ink}}><span>{it.titulo}</span><span style={{fontWeight: 400, color: C.soft, fontSize: 30}}>{it.hora}</span></div>
              <div style={{fontFamily: 'Inter', fontSize: 34, color: C.soft, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis'}}>{it.texto}</div>
            </div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

const Chat: React.FC<{sc: Scene}> = ({sc}) => {
  const msgs = sc.mensajes as {de: 'cliente' | 'ia'; texto: string; t: number}[];
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const enter = useSpring(0, {damping: 16});
  return (
    <AbsoluteFill style={{alignItems: 'center'}}>
      <div style={{position: 'absolute', top: 150, width: 860, height: 1240, borderRadius: 72, background: '#F3EEE8', boxShadow: shadow, overflow: 'hidden', border: '14px solid #17130F', transform: `translateY(${(1 - enter) * 300}px) rotate(${(1 - enter) * -4}deg)`}}>
        <div style={{height: 150, background: '#fff', display: 'flex', alignItems: 'center', gap: 24, padding: '30px 40px 0', borderBottom: `2px solid ${C.line}`}}>
          <div style={{width: 76, height: 76, borderRadius: 38, background: C.orange, color: '#fff', fontFamily: 'InterD', fontSize: 38, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>{String(sc.inicial ?? 'N')}</div>
          <div><div style={{fontFamily: 'Inter', fontWeight: 700, fontSize: 38, color: C.ink}}>{String(sc.negocio)}</div><div style={{fontFamily: 'Inter', fontSize: 28, color: C.green, fontWeight: 600}}>en línea · responde al momento</div></div>
        </div>
        <div style={{padding: '36px 34px', display: 'flex', flexDirection: 'column', gap: 22}}>
          {msgs.map((m, i) => {
            const start = Math.round(m.t * fps);
            const typing = m.de === 'ia' && f >= start - 30 && f < start;
            const s = spring({frame: f - start, fps, config: {damping: 13, stiffness: 190, mass: 0.6}});
            if (f < start - (m.de === 'ia' ? 30 : 0)) return null;
            const yo = m.de === 'ia';
            return (
              <div key={i} style={{alignSelf: yo ? 'flex-end' : 'flex-start', maxWidth: '82%'}}>
                {typing ? (
                  <div style={{background: C.orange, borderRadius: 34, padding: '26px 34px', display: 'flex', gap: 10}}>
                    {[0, 1, 2].map((d) => <div key={d} style={{width: 16, height: 16, borderRadius: 8, background: '#fff', opacity: 0.4 + 0.6 * Math.abs(Math.sin((f + d * 5) / 5))}} />)}
                  </div>
                ) : (
                  <div style={{
                    background: yo ? C.orange : '#fff', color: yo ? '#fff' : C.ink, borderRadius: 34, padding: '24px 32px',
                    fontFamily: 'Inter', fontWeight: 600, fontSize: 36, lineHeight: 1.3, boxShadow: '0 6px 18px rgba(0,0,0,0.06)',
                    transformOrigin: yo ? 'right bottom' : 'left bottom', transform: `scale(${interpolate(s, [0, 1], [0.6, 1])})`, opacity: s,
                  }}>{m.texto}</div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};

const Agenda: React.FC<{sc: Scene}> = ({sc}) => {
  const slots = sc.huecos as {hora: string; nombre: string; t: number}[];
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const e = useSpring(0);
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 190, left: 70, fontFamily: 'Inter', fontWeight: 700, fontSize: 36, color: C.orange, opacity: e}}>{String(sc.dia)}</div>
      <div style={{position: 'absolute', top: 240, left: 70, fontFamily: 'InterD', fontSize: 92, color: C.ink, letterSpacing: -3, opacity: e}}>{String(sc.titulo)}</div>
      {slots.map((sl, i) => {
        const at = Math.round(sl.t * fps);
        const s = spring({frame: f - at, fps, config: {damping: 12, stiffness: 200, mass: 0.6}});
        const lleno = f >= at;
        return (
          <div key={i} style={{position: 'absolute', left: 70, right: 70, top: 420 + i * 178, height: 150, display: 'flex', gap: 28, alignItems: 'center'}}>
            <div style={{width: 150, fontFamily: 'Inter', fontWeight: 700, fontSize: 40, color: C.soft}}>{sl.hora}</div>
            <div style={{flex: 1, height: 150, borderRadius: 36, border: `4px dashed ${lleno ? 'transparent' : 'rgba(23,19,15,0.15)'}`, position: 'relative'}}>
              <div style={{position: 'absolute', inset: -4, borderRadius: 36, background: C.card, boxShadow: shadow, display: 'flex', alignItems: 'center', gap: 26, padding: '0 34px', transform: `scale(${interpolate(s, [0, 1], [0.7, 1])})`, opacity: lleno ? s : 0}}>
                <div style={{width: 64, height: 64, borderRadius: 32, background: C.green, color: '#fff', fontSize: 40, fontFamily: 'InterD', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>✓</div>
                <div style={{fontFamily: 'Inter', fontWeight: 700, fontSize: 40, color: C.ink}}>{sl.nombre}</div>
                <div style={{marginLeft: 'auto'}}><Pill bg="#FFF1E8" color={C.orange} size={26}>IA</Pill></div>
              </div>
            </div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

const Lista: React.FC<{sc: Scene}> = ({sc}) => {
  const items = sc.items as {texto: string; t: number}[];
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{background: C.ink}}>
      <div style={{position: 'absolute', top: 260, left: 80, fontFamily: 'Inter', fontWeight: 700, fontSize: 36, color: C.orange2}}>{String(sc.titulo)}</div>
      {items.map((it, i) => {
        const at = Math.round(it.t * fps); const s = spring({frame: f - at, fps, config: {damping: 14, stiffness: 180}});
        const ok = spring({frame: f - at - 8, fps, config: {damping: 10, stiffness: 220}});
        return (
          <div key={i} style={{position: 'absolute', left: 80, right: 80, top: 360 + i * 170, height: 140, borderRadius: 36, background: '#241E19', display: 'flex', alignItems: 'center', padding: '0 40px', opacity: s, transform: `translateX(${(1 - s) * -120}px)`}}>
            <div style={{fontFamily: 'Inter', fontWeight: 700, fontSize: 46, color: '#fff'}}>{it.texto}</div>
            <div style={{marginLeft: 'auto', width: 70, height: 70, borderRadius: 35, background: C.green, color: C.ink, fontFamily: 'InterD', fontSize: 42, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${ok})`}}>✓</div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

const Cta: React.FC<{sc: Scene; brand: string}> = ({sc, brand}) => {
  const f = useCurrentFrame();
  const s = useSpring(0, {damping: 9, stiffness: 160});
  const pulse = 1 + 0.03 * Math.sin(f / 5);
  return (
    <AbsoluteFill style={{alignItems: 'center'}}>
      <div style={{position: 'absolute', top: 520, fontFamily: 'InterD', fontSize: 110, color: C.ink, letterSpacing: -4, opacity: s}}>{String(sc.arriba ?? 'Comenta')}</div>
      <div style={{position: 'absolute', top: 680, transform: `scale(${interpolate(s, [0, 1], [0.4, 1]) * pulse})`}}>
        <div style={{background: C.orange, color: '#fff', fontFamily: 'InterD', fontSize: 120, letterSpacing: -3, padding: '28px 64px', borderRadius: 40, boxShadow: '0 30px 70px rgba(255,90,20,0.35)'}}>{String(sc.palabra ?? 'RECEPCIÓN')}</div>
      </div>
      <div style={{position: 'absolute', top: 920, fontFamily: 'Inter', fontWeight: 600, fontSize: 46, color: C.soft, opacity: useSpring(10)}}>{String(sc.abajo ?? 'y te lo monto en tu negocio')}</div>
      <div style={{position: 'absolute', bottom: 260, fontFamily: 'Inter', fontWeight: 700, fontSize: 52, color: C.orange, opacity: useSpring(16)}}>{brand}</div>
    </AbsoluteFill>
  );
};

// ---------- subtítulos palabra a palabra ----------
const Subtitulos: React.FC<{words: Word[]; ocultar: [number, number][]}> = ({words, ocultar}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig(); const t = f / fps;
  if (ocultar.some(([a, b]) => t >= a && t < b)) return null;
  // páginas de hasta 3 palabras
  const pages: Word[][] = []; let cur: Word[] = [];
  words.forEach((w, i) => {
    cur.push(w);
    const gap = i + 1 < words.length ? words[i + 1].t0 - w.t1 : 1;
    const largo = cur.map((x) => x.w).join(' ').length;
    const sig = i + 1 < words.length ? words[i + 1].w.length + 1 : 0;
    if (cur.length === 3 || largo + sig > 17 || gap > 0.35 || /[.,?!]$/.test(w.w)) { pages.push(cur); cur = []; }
  });
  if (cur.length) pages.push(cur);
  const page = pages.find((p) => t >= p[0].t0 - 0.05 && t <= p[p.length - 1].t1 + 0.25);
  if (!page) return null;
  const s = spring({frame: f - Math.round(page[0].t0 * fps), fps, config: {damping: 12, stiffness: 220, mass: 0.5}});
  return (
    <div style={{position: 'absolute', bottom: 300, width: '100%', display: 'flex', justifyContent: 'center', gap: 18, transform: `scale(${interpolate(s, [0, 1], [0.8, 1])})`}}>
      {page.map((w, i) => {
        const on = t >= w.t0 && t <= w.t1 + 0.08;
        return (
          <span key={i} style={{
            fontFamily: 'InterD', fontSize: 76, letterSpacing: -1.5, textTransform: 'uppercase', padding: '6px 18px', borderRadius: 18,
            color: on ? '#fff' : C.ink, background: on ? C.orange : 'rgba(255,255,255,0.92)',
            boxShadow: '0 10px 30px rgba(0,0,0,0.12)',
          }}>{w.w.replace(/[.,]$/, '')}</span>
        );
      })}
    </div>
  );
};

// ---------- composición ----------
export const ReelPro: React.FC<ReelProps> = ({scenes, words, voice, music, brand, musicVol = 0.12, sfx = []}) => {
  const {fps} = useVideoConfig();
  const ocultar: [number, number][] = scenes.filter((s) => s.type === 'cta' || s.subtitulos === false).map((s) => [s.from / fps, (s.from + s.dur) / fps]);
  return (
    <AbsoluteFill>
      <style>{fontCss}</style>
      <Fondo />
      {scenes.map((sc, i) => (
        <Sequence key={i} from={sc.from} durationInFrames={sc.dur}>
          <Entrada dur={sc.dur}>
            {sc.type === 'hook' && <Hook sc={sc} />}
            {sc.type === 'notifs' && <Notifs sc={sc} />}
            {sc.type === 'chat' && <Chat sc={sc} />}
            {sc.type === 'agenda' && <Agenda sc={sc} />}
            {sc.type === 'lista' && <Lista sc={sc} />}
            {sc.type === 'cta' && <Cta sc={sc} brand={brand} />}
          </Entrada>
        </Sequence>
      ))}
      <Subtitulos words={words} ocultar={ocultar} />
      {voice ? <Audio src={staticFile(voice)} /> : null}
      {music ? <Audio src={staticFile(music)} volume={(f) => interpolate(f, [0, 15], [0, musicVol], {extrapolateRight: 'clamp'})} /> : null}
      {sfx.map((x, i) => <Sequence key={'s' + i} from={Math.round(x.t * fps)}><Audio src={staticFile(x.s)} volume={x.v ?? 0.5} /></Sequence>)}
    </AbsoluteFill>
  );
};
