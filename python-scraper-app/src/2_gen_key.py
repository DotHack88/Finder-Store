import hashlib

def genera_chiave(machine_id, salt="dotHack88_scraper"):
    lic_key = hashlib.sha256((machine_id + salt).encode()).hexdigest()[:16]
    print(f"🖥️ ID macchina: {machine_id}")
    print(f"🔑 Chiave licenza: {lic_key}")

if __name__ == "__main__":
    machine_id = input("Inserisci l'ID macchina del cliente: ").strip()
    genera_chiave(machine_id)
