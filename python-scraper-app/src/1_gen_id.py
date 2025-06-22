import uuid
import hashlib

def get_machine_id():
    return hashlib.sha256(str(uuid.getnode()).encode()).hexdigest()[:16]

if __name__ == "__main__":
    machine_id = get_machine_id()
    print(f"🖥️ Il tuo ID macchina è: {machine_id}")
