# CMOS Inverter guide (Lectures 23–25), sources

The finished PDF is `../CMOS_Inverter_Guide_Revised.pdf`.

Rebuild:

```bash
pip install matplotlib numpy          # figures
python3 src/figs.py                   # writes figs/*.svg
python3 src/check_numbers.py          # re-checks every number against a brute-force VTC model
npm install                           # KaTeX
node src/build.js guide.html out.pdf  # Chromium (Playwright) renders the PDF
```
