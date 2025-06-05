import requests
import tkinter as tk
from tkinter import messagebox
import os

VERSIONE_CORRENTE = "1.0.0"
URL_VERSIONE = "https://raw.githubusercontent.com/DotHack88/ps-scraper/main/version.txt"
URL_DOWNLOAD = "https://github.com/DotHack88/ps-scraper/releases/download/v1.0.0/scraper.exe"

def controlla_aggiornamenti():
    try:
        ultima_versione = requests.get(URL_VERSIONE, timeout=5).text.strip()
        if ultima_versione != VERSIONE_CORRENTE:
            root = tk.Tk()
            root.withdraw()  # Nasconde la finestra principale
            risposta = messagebox.askyesno(
                "Aggiornamento disponibile",
                f"È disponibile una nuova versione ({ultima_versione}).\nVuoi scaricarla ora?"
            )
            if risposta:
                scarica_aggiornamento()
            root.destroy()
    except Exception as e:
        print("Impossibile controllare la presenza di aggiornamenti.")

def scarica_aggiornamento():
    try:
        response = requests.get(URL_DOWNLOAD, stream=True)
        nome_file = os.path.basename(URL_DOWNLOAD)
        with open(nome_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        messagebox.showinfo("Download completato", f"Nuova versione scaricata come {nome_file}.\nChiudi il programma e avvia il nuovo file.")
    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante il download: {e}")

if __name__ == "__main__":
    controlla_aggiornamenti()
    # ...il resto del tuo programma...