# PHILO STUDIO — Local Photo Selection App

A lightweight, local-network web application built for **PHILO STUDIO**. The application allows photo studio clients to view their session photos on an iPad (via local Wi-Fi) and organize them into custom print templates (Postcards, Photocards, 8-Photo Grids, and Darkroom Strips).

---

## 📖 How to Use

### 1. Staff Setup (Starting a Client Session)
1. Ensure your client's photos are saved on your Mac Desktop inside a structured date and client folder (e.g., `Desktop/OCT 28/BIANCA`).
2. Launch the backend server on your Mac (see [Getting Started](#-getting-started)).
3. Open the app on your Mac or iPad Safari.
4. Click **⚙️ Staff Setup** in the top-right corner of the header.
5. Enter the **Date Folder Name** (e.g., `OCT 28`) and **Client Folder Name** (e.g., `BIANCA`).
6. Select the client's package type (**SOLO**, **DUO**, **GROUP**, **FULL GRID LITE**, **FULL GRID**, or **DARK ROOM**).
7. Click **🔍 Load Photos from Mac Desktop**. The client's photos will load instantly into the 3-column gallery on the left.

---

### 2. Client Selection & Layout Adjustments
Hand the iPad to the client to complete their photo selections:

- **Assigning Photos to Slots:**
  1. Tap any empty slot (`+ Slot`) on a print template on the right side of the screen to activate it (it will highlight with a brown border).
  2. Tap a photo from the left gallery to place it into the selected slot.

- **Micro-Adjusting Photo Position (Up / Down):**
  1. Tap an assigned photo slot to activate it.
  2. Tap the small **`▲` (Up)** or **`▼` (Down)** arrows in the top-right corner of the slot to shift the photo vertically.
  3. Movement is automatically clamped to strict boundaries so no white edges or background gaps ever show.

- **Toggling Grid Layout Orientations (8-Photo Grids):**
  - For 8-Photo Grid sheets, use the header toggle to switch between:
    - **📱 Vertical Grid (2x4):** Fits portrait-oriented prints.
    - **🖼️ Horizontal Grid (4x2):** Fits landscape-oriented prints.
  - Photo assignments automatically persist when toggling between vertical and horizontal views.

- **Using Undo & Redo:**
  - If a client makes a mistake or wants to change a placement, tap **`↩ Undo`** or **`Redo ↪`** in the top navigation bar to revert or re-apply changes.

---

## 📸 Supported Print Packages & Templates

- **SOLO:** 1x 4R Postcard Single & 1x 8-Photo Grid Sheet.
- **DUO:** 2x Postcards & 2x Photocards.
- **GROUP:** 2x Postcards & 4x Photocards.
- **FULL GRID LITE:** 2x Postcards & 2x Photocards.
- **FULL GRID:** 3x Postcards & 2x 8-Photo Grid Sheets.
- **DARK ROOM:** 1x Dark 4-Grid (2x2), 2x Dark 2-Strips, and 2x Dark Photocards.

---

## 🛠️ Tech Stack

- **Backend:** Python FastAPI
- **Database:** SQLite (`philo_studio.db`)
- **Image Processing:** Python Pillow (PIL) for thumbnail generation
- **Frontend:** Vue.js 3, Tailwind CSS, HTML5, CSS3

---

## 📂 Project Structure

```text
philo_studio_app/
├── backend/
│   ├── app.py           # FastAPI server & media endpoints
│   └── database.py      # SQLite schema & package seeds
├── frontend/
│   ├── index.html       # Single-page Vue 3 app interface
│   ├── app.js           # Selection logic, index mapping & history state
│   └── styles.css       # Custom scrollbars & grid layout styles
├── .gitignore           # Ignores temp files, cache & local database
└── README.md            # App documentation & guide
