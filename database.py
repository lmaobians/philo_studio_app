import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "philo_studio.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_folder TEXT NOT NULL,
            client_name TEXT NOT NULL,
            folder_path TEXT UNIQUE NOT NULL,
            selected_package TEXT NOT NULL,
            is_active INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS package_templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            package_name TEXT NOT NULL,
            template_key TEXT NOT NULL,
            title TEXT NOT NULL,
            width_mm REAL NOT NULL,
            height_mm REAL NOT NULL,
            bg_theme TEXT DEFAULT 'light',
            slots_json TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            order_ref TEXT UNIQUE NOT NULL,
            status TEXT DEFAULT 'SUBMITTED',
            layouts_json TEXT NOT NULL,
            total_copies INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    seed_packages()

def seed_packages():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM package_templates")

    # Native Vertical 8-Photo Grid (2 cols x 4 rows)
    v_grid_8_slots = []
    for row in range(4):
        for col in range(2):
            v_grid_8_slots.append({
                "id": f"slot_v_{row}_{col}",
                "x": 2 + (col * 49),
                "y": 2 + (row * 35),
                "width": 47,
                "height": 33
            })

    templates = [
        # --- SOLO PACKAGE ---
        {"package_name": "SOLO", "template_key": "solo_post", "title": "4R Postcard Single", "width_mm": 100, "height_mm": 150, "bg_theme": "light", "slots_json": json.dumps([{"id": "s1", "x": 4, "y": 4, "width": 92, "height": 134}])},
        {"package_name": "SOLO", "template_key": "solo_grid", "title": "8-Photo Grid Sheet", "width_mm": 100, "height_mm": 150, "bg_theme": "light", "slots_json": json.dumps(v_grid_8_slots)},

        # --- DUO PACKAGE ---
        {"package_name": "DUO", "template_key": "duo_post1", "title": "Postcard #1", "width_mm": 100, "height_mm": 150, "bg_theme": "light", "slots_json": json.dumps([{"id": "s1", "x": 4, "y": 4, "width": 92, "height": 134}])},
        {"package_name": "DUO", "template_key": "duo_post2", "title": "Postcard #2", "width_mm": 100, "height_mm": 150, "bg_theme": "light", "slots_json": json.dumps([{"id": "s1", "x": 4, "y": 4, "width": 92, "height": 134}])},
        {"package_name": "DUO", "template_key": "duo_pc1", "title": "Photocard #1", "width_mm": 70, "height_mm": 100, "bg_theme": "light", "slots_json": json.dumps([{"id": "s1", "x": 5, "y": 5, "width": 60, "height": 82}])},
        {"package_name": "DUO", "template_key": "duo_pc2", "title": "Photocard #2", "width_mm": 70, "height_mm": 100, "bg_theme": "light", "slots_json": json.dumps([{"id": "s1", "x": 5, "y": 5, "width": 60, "height": 82}])},

        # --- FULL GRID LITE ---
        {"package_name": "FULL GRID LITE", "template_key": "fgl_post1", "title": "Postcard #1", "width_mm": 100, "height_mm": 150, "bg_theme": "light", "slots_json": json.dumps([{"id": "s1", "x": 4, "y": 4, "width": 92, "height": 134}])},
        {"package_name": "FULL GRID LITE", "template_key": "fgl_post2", "title": "Postcard #2", "width_mm": 100, "height_mm": 150, "bg_theme": "light", "slots_json": json.dumps([{"id": "s1", "x": 4, "y": 4, "width": 92, "height": 134}])},
        {"package_name": "FULL GRID LITE", "template_key": "fgl_pc1", "title": "Photocard #1", "width_mm": 70, "height_mm": 100, "bg_theme": "light", "slots_json": json.dumps([{"id": "s1", "x": 5, "y": 5, "width": 60, "height": 82}])},
        {"package_name": "FULL GRID LITE", "template_key": "fgl_pc2", "title": "Photocard #2", "width_mm": 70, "height_mm": 100, "bg_theme": "light", "slots_json": json.dumps([{"id": "s1", "x": 5, "y": 5, "width": 60, "height": 82}])},

        # --- GROUP PACKAGE ---
        {"package_name": "GROUP", "template_key": "grp_post1", "title": "Postcard #1", "width_mm": 100, "height_mm": 150, "bg_theme": "light", "slots_json": json.dumps([{"id": "s1", "x": 4, "y": 4, "width": 92, "height": 134}])},
        {"package_name": "GROUP", "template_key": "grp_post2", "title": "Postcard #2", "width_mm": 100, "height_mm": 150, "bg_theme": "light", "slots_json": json.dumps([{"id": "s1", "x": 4, "y": 4, "width": 92, "height": 134}])},
        {"package_name": "GROUP", "template_key": "grp_pc1", "title": "Photocard #1", "width_mm": 70, "height_mm": 100, "bg_theme": "light", "slots_json": json.dumps([{"id": "s1", "x": 5, "y": 5, "width": 60, "height": 82}])},
        {"package_name": "GROUP", "template_key": "grp_pc2", "title": "Photocard #2", "width_mm": 70, "height_mm": 100, "bg_theme": "light", "slots_json": json.dumps([{"id": "s1", "x": 5, "y": 5, "width": 60, "height": 82}])},
        {"package_name": "GROUP", "template_key": "grp_pc3", "title": "Photocard #3", "width_mm": 70, "height_mm": 100, "bg_theme": "light", "slots_json": json.dumps([{"id": "s1", "x": 5, "y": 5, "width": 60, "height": 82}])},
        {"package_name": "GROUP", "template_key": "grp_pc4", "title": "Photocard #4", "width_mm": 70, "height_mm": 100, "bg_theme": "light", "slots_json": json.dumps([{"id": "s1", "x": 5, "y": 5, "width": 60, "height": 82}])},

        # --- FULL GRID PACKAGE ---
        {"package_name": "FULL GRID", "template_key": "fg_post1", "title": "Postcard #1", "width_mm": 100, "height_mm": 150, "bg_theme": "light", "slots_json": json.dumps([{"id": "s1", "x": 4, "y": 4, "width": 92, "height": 134}])},
        {"package_name": "FULL GRID", "template_key": "fg_post2", "title": "Postcard #2", "width_mm": 100, "height_mm": 150, "bg_theme": "light", "slots_json": json.dumps([{"id": "s1", "x": 4, "y": 4, "width": 92, "height": 134}])},
        {"package_name": "FULL GRID", "template_key": "fg_post3", "title": "Postcard #3", "width_mm": 100, "height_mm": 150, "bg_theme": "light", "slots_json": json.dumps([{"id": "s1", "x": 4, "y": 4, "width": 92, "height": 134}])},
        {"package_name": "FULL GRID", "template_key": "fg_grid1", "title": "8-Photo Grid Sheet #1", "width_mm": 100, "height_mm": 150, "bg_theme": "light", "slots_json": json.dumps(v_grid_8_slots)},
        {"package_name": "FULL GRID", "template_key": "fg_grid2", "title": "8-Photo Grid Sheet #2", "width_mm": 100, "height_mm": 150, "bg_theme": "light", "slots_json": json.dumps(v_grid_8_slots)},

        # --- DARK ROOM PACKAGE (2 Photocards) ---
        {"package_name": "DARK ROOM", "template_key": "dr_grid", "title": "Dark 4-Grid (2x2)", "width_mm": 100, "height_mm": 150, "bg_theme": "dark", "slots_json": json.dumps([
            {"id": "dr_top_left",  "x": 4,  "y": 4,  "width": 44, "height": 65},
            {"id": "dr_top_right", "x": 52, "y": 4,  "width": 44, "height": 65},
            {"id": "dr_bot_left",  "x": 4,  "y": 72, "width": 44, "height": 65},
            {"id": "dr_bot_right", "x": 52, "y": 72, "width": 44, "height": 65}
        ])},
        {"package_name": "DARK ROOM", "template_key": "dr_strip1", "title": "Dark 2-Strip Vertical #1", "width_mm": 50, "height_mm": 150, "bg_theme": "dark", "slots_json": json.dumps([
            {"id": "s1", "x": 4, "y": 4, "width": 42, "height": 65},
            {"id": "s2", "x": 4, "y": 72, "width": 42, "height": 65}
        ])},
        {"package_name": "DARK ROOM", "template_key": "dr_strip2", "title": "Dark 2-Strip Vertical #2", "width_mm": 50, "height_mm": 150, "bg_theme": "dark", "slots_json": json.dumps([
            {"id": "s1", "x": 4, "y": 4, "width": 42, "height": 65},
            {"id": "s2", "x": 4, "y": 72, "width": 42, "height": 65}
        ])},
        {"package_name": "DARK ROOM", "template_key": "dr_pc1", "title": "Dark Photocard #1", "width_mm": 70, "height_mm": 100, "bg_theme": "dark", "slots_json": json.dumps([{"id": "s1", "x": 6, "y": 6, "width": 58, "height": 78}])},
        {"package_name": "DARK ROOM", "template_key": "dr_pc2", "title": "Dark Photocard #2", "width_mm": 70, "height_mm": 100, "bg_theme": "dark", "slots_json": json.dumps([{"id": "s1", "x": 6, "y": 6, "width": 58, "height": 78}])}
    ]

    for t in templates:
        cursor.execute("""
            INSERT INTO package_templates (package_name, template_key, title, width_mm, height_mm, bg_theme, slots_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (t["package_name"], t["template_key"], t["title"], t["width_mm"], t["height_mm"], t["bg_theme"], t["slots_json"]))

    conn.commit()
    conn.close()