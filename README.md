# PHILO STUDIO — Local Photo Selection App

A lightweight, local-network web application built for **PHILO STUDIO**. The app enables studio clients to review their session photos on an iPad (via local Wi-Fi) and assign them into custom print-layout templates (Postcards, Photocards, 8-Photo Grids, and Darkroom Strips).

---

## 📸 Key Features

- **Local Network Operations:** Runs on a host Mac desktop and serves the interactive UI to an iPad Safari client over the local Wi-Fi network.
- **Client Session Setup:** Staff modal inputs the Desktop date folder and client name to dynamically scan and load client photos.
- **Clean 3-Column Photo Gallery:** Uniform portrait gallery grid with permanent filename overlays at the bottom of each thumbnail.
- **Custom Print Packages & Templates:**
  - **SOLO:** Single 4R Postcard & 8-Photo Grid Sheet.
  - **DUO:** 2 Postcards & 2 Photocards.
  - **GROUP:** 2 Postcards & 4 Photocards.
  - **FULL GRID LITE:** 2 Postcards & 2 Photocards.
  - **FULL GRID:** 3 Postcards & 2 8-Photo Grid Sheets.
  - **DARK ROOM:** Dark 4-Grid (2x2), 2 Dark 2-Strips, and 2 Dark Photocards.
- **Native Grid Orientations:** Standalone toggle for 8-Photo Grid layouts to switch between **Vertical Grid (2x4)** and **Horizontal Grid (4x2)** without rotation distortion or text overlaps.
- **Micro Position Controls:** Clamped vertical adjustment arrows (`▲` / `▼`) on active slots allow clients to micro-shift photos up or down without exposing white background edges or scaling incorrectly.
- **Undo / Redo System:** Full historical state tracking (`↩ Undo` and `Redo ↪`) to allow clients to experiment with photo placements stress-free.

---

## 🛠️ Tech Stack

- **Backend Engine:** Python FastAPI
- **Database:** SQLite (`philo_studio.db`)
- **Image Processing:** Python Pillow (PIL) for fast dynamic thumbnail generation
- **Frontend Stack:** Vue.js 3 (CDN), Tailwind CSS (CDN), HTML5, CSS3

---

## 📁 Project Structure

```text
philo_studio_app/
├── backend/
│   ├── app.py           # FastAPI server endpoints & media streaming
│   └── database.py      # SQLite DB schema, session tracking & package seeds
├── frontend/
│   ├── index.html       # Single-page Vue 3 app interface
│   ├── app.js           # Vue logic, state handling, offset math & Undo/Redo
│   └── styles.css       # Touch scrollbars, grid layouts & custom styling
├── .gitignore           # Excludes temporary cache & database from version control
└── README.md            # System documentation
