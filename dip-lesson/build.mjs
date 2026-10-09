// Builds a DIP lesson into one offline HTML file. Run: node build.mjs a|b   (output in dist/)
import { readFileSync, writeFileSync, mkdirSync, readdirSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const src = (f) => readFileSync(join(here, 'src', f), 'utf8');
const kdir = join(here, 'node_modules', 'katex', 'dist');
const kcss = readFileSync(join(kdir, 'katex.min.css'), 'utf8').replace(/src:url\(fonts\/([^)]+\.woff2)\) format\("woff2"\)(,url\([^)]+\) format\("[a-z]+"\))*/g, (_m, f) =>
  `src:url(data:font/woff2;base64,${readFileSync(join(kdir, 'fonts', f)).toString('base64')}) format("woff2")`);
const b64dir = (d, ext, mime) => existsSync(d) ? Object.fromEntries(readdirSync(d).filter((f) => f.endsWith(ext)).map((f) => [f.slice(0, -ext.length), `data:${mime};base64,` + readFileSync(join(d, f)).toString('base64')])) : {};
const LESSONS = {
  a: { out: 'dip-lec1-2.html', title: 'DIP: Lec 1–2', h1: 'DIP · Lectures 1–2: Overview and Digital Image Fundamentals', sub: 'the eye, light, sensors, sampling and quantization, pixels and their neighbours, the maths toolbox · every quiz and past-paper question, solved by you first',
    files: ['engine.js', 'voice.js', 'lib.js', 'frame.js', 'd_lib.js', 'a_intro.js', 'a_overview.js', 'a_eye.js', 'a_sample.js', 'a_pixels.js', 'a_tools.js', 'a_outro.js', 'app.js'] },
  b: { out: 'dip-lec3.html', title: 'DIP: Lec 3', h1: 'DIP · Lecture 3: Intensity Transformations and Spatial Filtering', sub: 'point transforms, bit planes, histograms (equalization and matching), correlation and convolution, smoothing and sharpening · every quiz and past-paper question, solved by you first',
    files: ['engine.js', 'voice.js', 'lib.js', 'frame.js', 'd_lib.js', 'b_intro.js', 'b_point.js', 'b_hist.js', 'b_filter.js', 'b_smooth.js', 'b_sharp.js', 'b_outro.js', 'app.js'] },
};
const key = process.argv[2] || 'a';
const L = LESSONS[key];
let audio = {};
const man = join(here, 'audio', key + '.json');
const mp3 = (k) => join(here, 'audio', 'mp3', k + '.mp3');
if (existsSync(man)) for (const { k } of JSON.parse(readFileSync(man, 'utf8'))) if (existsSync(mp3(k))) audio[k] = 'data:audio/mpeg;base64,' + readFileSync(mp3(k)).toString('base64');
if (existsSync(man) && Object.keys(audio).length < 0.5 * JSON.parse(readFileSync(man, 'utf8')).length) audio = {};
const answers = readFileSync(join(here, 'num', 'answers.json'), 'utf8');
const meta = readFileSync(join(here, 'assets', 'meta.json'), 'utf8');
const imgs = b64dir(join(here, 'assets'), '.webp', 'image/webp');
const papers = b64dir(join(here, 'papers'), '.webp', 'image/webp');
const app = `const AUDIO = ${JSON.stringify(audio)};\nconst PROBLEMS = {};\nconst ANSWERS = ${answers};\nconst META = ${meta};\nconst IMGS = ${JSON.stringify(imgs)};\nconst PAPERS = ${JSON.stringify(papers)};\nvar FORMULAS = [], CARDS = [];\n`
  + L.files.filter((f) => existsSync(join(here, 'src', f))).map((f) => `/* ── ${f} ── */\n` + src(f)).join('\n');
const out = src('shell.html')
  .replace('/*KATEXCSS*/', () => kcss)
  .replace('/*STYLE*/', () => src('style.css'))
  .replace(/\/\*TITLE\*\//g, L.title).replace('/*H1*/', L.h1).replace('/*SUB*/', L.sub)
  .replace('/*KATEXJS*/', () => readFileSync(join(kdir, 'katex.min.js'), 'utf8'))
  .replace('/*APPJS*/', () => app.replace(/<\/script/g, '<\\/script'));
const outDir = process.env.ANIM_OUT || join(here, 'dist');
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, L.out), out);
console.log('built', L.out, (out.length / 1e6).toFixed(2), 'MB,', Object.keys(audio).length, 'recorded lines');
