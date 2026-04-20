import json
import os

DATA_FILE = "students.json"
CONFIG_FILE = "config.json"

def load_records():
    """Loads student data from JSON."""
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_records(records):
    """Saves student dictionary to JSON."""
    with open(DATA_FILE, 'w') as f:
        json.dump(records, f, indent=4)

def load_thresholds():
    """Persists threshold settings across sessions."""
    if not os.path.exists(CONFIG_FILE):
        return {"grade": 40.0, "attendance": 80.0}
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_thresholds(thresholds):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(thresholds, f, indent=4)

def update_student_data(name, data_type, new_data):
    """Updates specific student attributes."""
    records = load_records()
    if name not in records:
        records[name] = {"grades": [], "attendance": 100}
    
    if data_type == "grade":
        records[name]["grades"].append(new_data)
    elif data_type == "attendance":
        records[name]["attendance"] = new_data
        
    save_records(records)