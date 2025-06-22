import uuid
import hashlib

def get_machine_id():
    return hashlib.sha256(str(uuid.getnode()).encode()).hexdigest()[:16]

def genera_chiave(salt="dotHack88_scraper"):
    machine_id = get_machine_id()
    lic_key = hashlib.sha256((machine_id + salt).encode()).hexdigest()[:16]
    print(f"🖥️ ID macchina: {machine_id}")
    print(f"🔑 Chiave licenza: {lic_key}")

genera_chiave()
