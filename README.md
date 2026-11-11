# Srikanth Chakilam — GitHub Pages portfolio

This package contains the latest complete multi-page portfolio, including all images, animations, four optimized walkthrough videos, resume, and the Python/MCP demo. No build step or dependencies are required for the website.

## Publish

1. Extract the ZIP.
2. Copy its contents into the ROOT of your `Chakilamsrikanth/chakilamsrikanth.github.io` repository. `index.html`, `styles.css`, `app.js`, `experience.css`, `assets`, and `images` should be at the root, not inside another portfolio folder. Keep your existing `.git` directory.
3. Commit and push your changes.
4. Under GitHub repository Settings → Pages, choose Deploy from a branch, select your publishing branch, and select `/ (root)`. If Pages is already configured, keep that branch.
5. Your portfolio will publish at https://chakilamsrikanth.github.io/.

The `.nojekyll` file is included. Social metadata points to the GitHub Pages address. Old page URLs remain usable, including both `schwab.html` and `charlesschwab.html`.

## Run locally

Open `index.html`, or run `python -m http.server 8000` from this folder and visit http://localhost:8000.

The contact form opens a prefilled email draft; it does not require a backend. LinkedIn, GitHub, phone, and email links are ready to use.

The embedded Python/MCP workspace has a static sample preview. To run the Python backend locally, run `python python-demo/workspace.py` and open http://127.0.0.1:8765. See `python-demo/README.txt` for details. GitHub Pages serves the static preview and downloadable source, not a Python server.

Generated interface concepts are labeled separately from original portfolio screenshots. Videos are compressed for the single-file download; all four walkthroughs are included.
