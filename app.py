import os
import json
import sqlite3
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from PIL import Image

from database import init_db, get_db_connection

USER_HOME = Path.home()
STUDIO_ROOT = USER_HOME / "Desktop"

app = FastAPI(title="PHILO STUDIO Selection System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

def get_thumb_dir(session_path: Path) -> Path:
    thumb_dir = session_path / ".thumbnails"
    thumb_dir.mkdir(exist_ok=True)
    return thumb_dir

class LoadSessionRequest(BaseModel):
    date_folder: str
    client_name: str
    selected_package: str

class SlotAssignment(BaseModel):
    template_id: str
    slot_id: str
    filename: str

class OrderSubmitRequest(BaseModel):
    session_id: int
    package_name: str
    assignments: List[SlotAssignment]
    total_copies: int = 1

@app.post("/api/staff/load-session")
def load_session(req: LoadSessionRequest):
    """Staff inputs Date Folder & Client Name, scans ~/Desktop/<DATE>/<CLIENT>."""
    date_clean = req.date_folder.strip()
    client_clean = req.client_name.strip()

    target_path = (STUDIO_ROOT / date_clean / client_clean).resolve()

    if not target_path.exists():
        raise HTTPException(
            status_code=404, 
            detail=f"Folder not found at Desktop/{date_clean}/{client_clean}. Please check folder names."
        )

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE sessions SET is_active = 0")
    cursor.execute("SELECT id FROM sessions WHERE folder_path = ?", (str(target_path),))
    row = cursor.fetchone()

    if row:
        session_id = row["id"]
        cursor.execute("UPDATE sessions SET is_active = 1, selected_package = ? WHERE id = ?", (req.selected_package, session_id))
    else:
        cursor.execute(
            "INSERT INTO sessions (date_folder, client_name, folder_path, selected_package, is_active) VALUES (?, ?, ?, ?, 1)",
            (date_clean, client_clean, str(target_path), req.selected_package)
        )
        session_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return {"status": "success", "session_id": session_id}

@app.get("/api/client/active-session")
def get_active_session():
    """Returns photos and package templates directly to iPad Safari."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessions WHERE is_active = 1 LIMIT 1")
    session = cursor.fetchone()

    if not session:
        conn.close()
        return {"has_active_session": False}

    session_dict = dict(session)
    session_path = Path(session_dict["folder_path"])

    valid_extensions = {".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"}
    photos = []
    if session_path.exists():
        for file in sorted(os.listdir(session_path)):
            if Path(file).suffix in valid_extensions and not file.startswith('.'):
                photos.append(file)

    pkg_name = session_dict.get("selected_package", "SOLO")
    cursor.execute("SELECT * FROM package_templates WHERE package_name = ?", (pkg_name,))
    templates = [dict(t) for t in cursor.fetchall()]
    for t in templates:
        t["slots"] = json.loads(t["slots_json"])

    conn.close()

    return {
        "has_active_session": True,
        "session": {
            "id": session_dict["id"],
            "date_folder": session_dict["date_folder"],
            "client_name": session_dict["client_name"],
            "package_name": pkg_name
        },
        "photos": photos,
        "templates": templates
    }

@app.get("/api/media/thumbnail/{session_id}/{filename}")
def get_thumbnail(session_id: int, filename: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT folder_path FROM sessions WHERE id = ?", (session_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Session not found.")

    session_path = Path(row["folder_path"])
    image_path = session_path / filename

    thumb_dir = get_thumb_dir(session_path)
    thumb_path = thumb_dir / f"thumb_{filename}"

    if not thumb_path.exists():
        try:
            with Image.open(image_path) as img:
                img.thumbnail((300, 300))
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                img.save(thumb_path, "JPEG", quality=80)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Thumbnail error: {str(e)}")

    with open(thumb_path, "rb") as f:
        return Response(content=f.read(), media_type="image/jpeg")

@app.get("/api/media/full/{session_id}/{filename}")
def get_full_image(session_id: int, filename: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT folder_path FROM sessions WHERE id = ?", (session_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Session not found.")

    image_path = Path(row["folder_path"]) / filename
    ext = image_path.suffix.lower()
    media_type = "image/png" if ext == ".png" else "image/jpeg"

    with open(image_path, "rb") as f:
        return Response(content=f.read(), media_type=media_type)

@app.post("/api/orders/submit")
def submit_order(order_req: OrderSubmitRequest):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT folder_path, date_folder, client_name FROM sessions WHERE id = ?", (order_req.session_id,))
    session = cursor.fetchone()

    if not session:
        conn.close()
        raise HTTPException(status_code=404, detail="Session not found.")

    order_ref = f"PHILO-{order_req.package_name}-{session['client_name']}"
    assignments_data = [a.dict() for a in order_req.assignments]

    cursor.execute("""
        INSERT INTO orders (session_id, order_ref, status, layouts_json, total_copies)
        VALUES (?, ?, 'SUBMITTED', ?, ?)
    """, (order_req.session_id, order_ref, json.dumps(assignments_data), order_req.total_copies))

    conn.commit()
    conn.close()

    # Save manifest into client folder
    manifest_path = Path(session["folder_path"]) / f"ORDER_{order_ref}.json"
    with open(manifest_path, "w") as f:
        json.dump({
            "order_ref": order_ref,
            "package": order_req.package_name,
            "client": session["client_name"],
            "assignments": assignments_data
        }, f, indent=2)

    return {"status": "success", "order_ref": order_ref}

# Mount static frontend files
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")

# ENTRY POINT BLOCK (Starts Uvicorn server directly when running `python3 app.py`)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)