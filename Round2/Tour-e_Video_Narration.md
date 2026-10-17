# Tour-e · Round 2 video: script and recording guide (2:00)

The video has two parts:

1. **The film (0:00–0:36).** `tour-e-film.mp4` plays full screen. The voiceover is already in it, so you stay quiet. Your camera sits in a small box in the corner, so judges see you from the first second.
2. **You and the slides (0:36–2:00).** You share `Tour-e_Round2_Presentation.pdf` and talk over it live, one slide every 7–10 seconds, camera box still in the corner.

Pace: about 150 words a minute, which is calm and clear, not rushed. Every line below is written to fit its window with a breath to spare. **Bold** is the word to stress. *(…)* is a short pause.

---

## Part 1 · The film (0:00 – 0:36): don't speak

This is exactly what the voiceover in `tour-e-film.mp4` says, so you know where you are while it plays.

| Time | On screen | Voiceover (already in the film) |
|---|---|---|
| 0:00 – 0:01 | Black; the front fades in | *(silence while the lights come on)* |
| 0:01 – 0:08 | Light bar and "e" badge ignite, then the camera tracks along the side | "By 2030, every taxi in Delhi must be electric. Today, most of them are Marutis, running on CNG." |
| 0:08 – 0:15 | Rear: TOUR·e plate and lit emblem, then top-down over the roof | "This is Tour-e, Maruti's electric MPV. A flat floor, and three hundred kilometres of city range." |
| 0:17 – 0:22 | Side view; the sliding door opens at 0:17 | "A sliding door, room for a wheelchair, and an SOS button in every row." |
| 0:22 – 0:26 | Orbit; X-ray turns on | "The operator sees everything, so no trip is ever cut short." |
| 0:26 – 0:29 | Hero front three-quarter | "Designed for the driver. Built for the fleet." |
| 0:30 – 0:36 | Black; TOUR·e title card | "Tour-e." … "Cheaper on day one. Cheaper every kilometre." |

At 0:35, as the title card holds, take a breath and have slide 1 ready. Your first line starts the moment the film ends.

If you'd rather voice the film yourself, use `tour-e-film-silent.mp4` and read the right-hand column on the same cues.

## Part 2 · The slides (0:36 – 2:00): you speak

Change the slide *as you start* each line, not after.

| Time | Slide | Say | Words |
|---|---|---|---|
| 0:36 – 0:46 | 1 · The hook | "Delhi's fleets must be all-electric by 2030, and CAFE III counts every EV three times. *(…)* Yet Maruti has about 3% of EV sales. Tata has **42**." | 25 |
| 0:46 – 0:53 | 2 · The market | "The volume is in city trips. The **margin** is in airport, inter-city and accessible rides. Tour-e is built for both." | 20 |
| 0:53 – 1:01 | 3 · The concept | "It's the MPV shape India already buys: five seats plus two, a **sliding door** on the kerb side, and room for a wheelchair." | 22 |
| 1:01 – 1:09 | 4 · Powertrain | "Under the floor is the e VITARA's 49 kWh pack: about **300 km** in the city on one charge. Long routes get a 61 kWh version." | 24 |
| 1:09 – 1:16 | 5 · Specs and safety | "The features come from rider and driver complaints: rear AC the rider controls, **SOS in every row**, and a drowsiness camera." | 20 |
| 1:16 – 1:26 | 6 · Fleet TCO | "For a fleet, Tour-e costs ₹7.33 a kilometre against ₹8.86 on CNG. *(…)* That's ₹1.22 lakh a car a year, over **₹12 crore** for a thousand cars." | 26 |
| 1:26 – 1:35 | 7 · Driver and hubs | "An owner-driver who charges at a Maruti hub keeps about ₹5,600 more every month. *(…)* That's **₹67,000** a year." | 19 |
| 1:35 – 1:43 | 8 · Price and the Maruti case | "With the battery on a per-kilometre EMI, the car costs ₹9.2 lakh. Maruti's ₹1,500 crore pays back by **2033**." | 19 |
| 1:43 – 1:49 | 9 · FleetOS | "FleetOS ties it together: battery-aware dispatch, charging slots, and live battery health." | 12 |
| 1:49 – 1:58 | 10 · Roadmap | "Pilots from 2026, launch in 2028, a lakh a year by 2035. *(look at the camera)* India's taxi market is going electric by law. Tour-e keeps it **Maruti's**." | 27 |
| 1:58 – 2:00 | Slide 10 stays up | *(small smile, hold two seconds, stop recording)* | |

Say "₹" as "rupees" (₹7.33 is "seven rupees thirty-three"), "₹1.22 lakh" as "one point two two lakh", and "CAFE" as "café".

---

## How to record it

### What you need

- **A laptop with a webcam** (or a phone on a stand as the camera).
- **A wired earphone mic or any USB mic.** These sound much better than the laptop mic. Phone earphones with a mic are fine.
- **OBS Studio (free, obsproject.com).** It lets you put your camera in a corner over both the film and the slides, and records straight to MP4. Simpler alternatives: PowerPoint's "Record" (import the PDF pages as slides), Zoom (record a meeting with yourself sharing your screen), or Loom.

### Set up OBS once (about 15 minutes)

1. **Settings → Video:** Base and Output resolution 1920×1080, 30 FPS.
2. **Settings → Output → Recording:** format MP4, quality "High Quality, Medium File Size".
3. **Scene "Film":** add a *Media Source* pointing to `tour-e-film.mp4` and tick "Restart playback when source becomes active". Then add a *Video Capture Device* (your webcam), resize it to **300 × 169 px** (right-click → Transform → Edit Transform), and place it 16 px in from the bottom-right corner. It sits over the black bar and the empty floor, not the car.
4. **Scene "Slides":** add a *Window Capture* of the PDF in full-screen presentation mode (in Adobe Reader or Edge, press Ctrl+L or F5), plus the same webcam box (300 × 169 px, 16 px from the bottom-right corner; copy it from the Film scene with Ctrl+C / Ctrl+V so it lines up exactly). At that size it clears all the slide text and only covers the slide number.
5. **Audio:** in the mixer, keep your mic at about −12 dB when you speak (the meter peaks in the yellow) and the film's audio at 0 dB. Mute the desktop audio so nothing else leaks in.
6. Set a hotkey to switch scenes (e.g. F1 for Film, F2 for Slides) so you don't fumble with the mouse.

### Camera, light and room

- Camera at eye level. Put books under the laptop. Frame your head and shoulders, with a little space above your head.
- Face a window or a lamp; never have the light behind you.
- A plain wall behind you. Dark clothes suit the dark slides; avoid busy patterns.
- Fan and AC off while you record. Phone on silent.

### The take

1. Open the PDF on slide 1 in presentation mode. Start OBS on the **Film** scene.
2. Click **Start Recording**. Wait one second, then let the film play. Stay still and look at the camera.
3. At 0:36, when the film ends, press your **Slides** hotkey and start the slide 1 line straight away.
4. Advance each slide as you begin its line (arrow key or clicker).
5. On the last line, look into the camera lens, not the screen. Hold two seconds and stop recording.

Expect three to five takes. Use the best one. Don't stitch takes unless you have to.

### Rehearse first

- Read Part 2 out loud with a stopwatch three times. It should land between 1:20 and 1:24. If you run long, cut the *(…)* pauses before you speed up.
- Practise the two numbers that matter most (slides 6 and 7) until you can say them without looking.
- Keep a printout of Part 2 taped just under the webcam. Glance at it; don't read it.

### Check before you submit

- Length is **2:00 or less** (right-click the file → Properties → Details).
- 1080p MP4, and the file plays on a phone.
- You are visible the whole time; the voiceover and your voice are both clear and at a similar loudness.
- Every slide is readable when it's on screen; none flashes past in under five seconds.
- Upload the MP4 together with `Tour-e_Round2_Presentation.pdf` before **18 Oct 2026, 11:59 PM IST**.

---

## Numbers you're saying, and where they come from

All of these come from `Tour-e_TCO_Model_R2.xlsx`, so you can answer follow-up questions.

| Line | Figure | Sheet |
|---|---|---|
| City range | 307 km (46 kWh usable at 0.150 kWh/km) | Inputs |
| Long-route pack | 61 kWh (57 usable), 317 km highway | Inputs |
| Fleet cost per km | ₹7.33 (battery EMI) vs ₹8.86 (CNG) | TCO |
| Fleet saving | ₹1.22 lakh per car per year; ₹12.2 crore per 1,000 cars | Fleet_Economics |
| Driver gain | ₹5,600 a month at hub tariff, car bought outright = ₹67,200 a year | Driver_Economics |
| Car price with battery EMI | ₹9.20 lakh (2028), battery at ₹2.1/km | Price_Walk, BaaS |
| Programme | ₹1,500 crore capex, payback 2033 | Maruti_Case |
| Volumes | 10k in 2028, 50k in 2031, 1 lakh in 2035 | Maruti_Case |

If a judge pushes on the driver number: on battery EMI the gain is ₹5,150 a month, and without hub charging it's still positive at ₹1,400. Even if the battery were leased with 18% GST, it stays at +₹3,250.

## Delivery notes

- Don't read the slide. The slide shows the number; you say what it means.
- Slow down on 6 and 7. Those two are the case.
- The last line is the first headline. Say it to the camera, not the screen.
