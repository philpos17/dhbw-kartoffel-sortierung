import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'sorter.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Table for production statistics
    c.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            good_count INTEGER DEFAULT 0,
            bad_count INTEGER DEFAULT 0,
            stone_count INTEGER DEFAULT 0
        )
    ''')
    
    # Table for settings
    c.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY,
            model_path TEXT,
            belt_speed_delay REAL,
            threshold_bad_area REAL,
            counting_line_y REAL DEFAULT 80.0,
            counting_orientation TEXT DEFAULT 'horizontal'
        )
    ''')
    
    # Try to add column if upgrading from older DB
    try:
        c.execute('ALTER TABLE settings ADD COLUMN counting_line_y REAL DEFAULT 80.0')
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE settings ADD COLUMN counting_orientation TEXT DEFAULT 'horizontal'")
    except sqlite3.OperationalError:
        pass
    
    # Table for model class mappings
    c.execute('''
        CREATE TABLE IF NOT EXISTS model_class_mappings (
            model_name TEXT,
            class_id INTEGER,
            action TEXT,
            confidence_threshold REAL DEFAULT 0.5,
            PRIMARY KEY (model_name, class_id)
        )
    ''')
    
    try:
        c.execute("ALTER TABLE model_class_mappings ADD COLUMN confidence_threshold REAL DEFAULT 0.5")
    except sqlite3.OperationalError:
        pass
    
    # Insert default settings if not exists
    c.execute('SELECT COUNT(*) FROM settings')
    if c.fetchone()[0] == 0:
        c.execute('''
            INSERT INTO settings (id, model_path, belt_speed_delay, threshold_bad_area, counting_line_y, counting_orientation)
            VALUES (1, 'yolov8n.pt', 2.5, 10.0, 80.0, 'horizontal')
        ''')
        
    conn.commit()
    conn.close()

def log_stats(good, bad):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO stats (good_count, bad_count)
        VALUES (?, ?)
    ''', (good, bad))
    conn.commit()
    conn.close()

def get_settings():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM settings WHERE id = 1')
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def update_settings(model_path, belt_speed_delay, threshold_bad_area, counting_line_y=80.0, counting_orientation='horizontal'):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        UPDATE settings
        SET model_path = ?, belt_speed_delay = ?, threshold_bad_area = ?, counting_line_y = ?, counting_orientation = ?
        WHERE id = 1
    ''', (model_path, belt_speed_delay, threshold_bad_area, counting_line_y, counting_orientation))
    conn.commit()
    conn.close()

def get_model_mapping(model_name):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM model_class_mappings WHERE model_name = ?', (model_name,))
    rows = c.fetchall()
    conn.close()
    
    mapping = {}
    for row in rows:
        conf = row['confidence_threshold'] if 'confidence_threshold' in row.keys() else 0.5
        mapping[int(row['class_id'])] = {
            "action": row['action'],
            "confidence": conf if conf is not None else 0.5
        }
    return mapping

def save_model_mapping(model_name, mapping):
    conn = get_db_connection()
    c = conn.cursor()
    # Remove old mapping
    c.execute('DELETE FROM model_class_mappings WHERE model_name = ?', (model_name,))
    # Insert new
    for class_id_str, class_data in mapping.items():
        # Ensure backwards compatibility if old frontend sends just string
        if isinstance(class_data, dict):
            action = class_data.get("action", "ignore")
            confidence = class_data.get("confidence", 0.5)
        else:
            action = class_data
            confidence = 0.5
            
        c.execute('INSERT INTO model_class_mappings (model_name, class_id, action, confidence_threshold) VALUES (?, ?, ?, ?)',
                  (model_name, int(class_id_str), action, confidence))
    conn.commit()
    conn.close()

# Initialize DB when module is imported
init_db()
