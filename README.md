# 🎮 PS Store Scraper ![PS Logo](https://upload.wikimedia.org/wikipedia/commons/4/4e/Playstation_logo_colour.svg)

> Un potente scraper per il PlayStation Store, semplice da usare e personalizzare! 🚀

---

## ✨ Funzionalità

- 🔍 Estrazione automatica dei dati dal PlayStation Store
- 🌍 Confronto prezzi tra store internazionali
- 🗣️ Estrazione lingue audio e testo
- 🖼️ Immagini di copertina incluse
- 📦 Salvataggio dei risultati in vari formati (CSV, JSON, ecc.)
- 🆕 Funzione aggiornata "Nuovi giochi"
- 🔍 Ricerca per nome, ID o con filtri avanzati
- ⚡ Interfaccia semplice e intuitiva (CLI + Tkinter)
- 🛠️ Facile da personalizzare per le tue esigenze

---

## 📦 Installazione

1. **Clona il repository**
   ```bash
   git clone https://github.com/DotHack88/ps-scraper.git
   cd ps-scraper
   ```

2. **Installa le dipendenze**
   ```bash
   pip install -r requirements.txt
   ```

3. *(Facoltativo)* Installa anche [Google Chrome](https://www.google.com/chrome/) se vuoi usare Selenium per l’automazione avanzata.

---

## 🚀 Utilizzo

Esegui lo scraper con:
```bash
python scraper.1.1.2.py
```

Segui il menu interattivo:

```
1. 🔎 Cerca per ID gioco
2. 🔍 Cerca con filtri avanzati
3. 🔤 Cerca per nome gioco
4. ℹ️ Info sul programma
5. 🆕 Pre-ordini
6. 🆕 Nuovi giochi
7. ❌ Esci
```

Puoi personalizzare i parametri nel file Python per adattare la ricerca alle tue esigenze.

---

## 🧾 Esempio di output

```
🎮 Titolo: FINAL FANTASY VII REBIRTH
💰 Prezzo: 79,99 € | 💶 EUR: 79.99
🌍 Store: https://store.playstation.com/it-it/product/EP0082-PPSA08477_00-FF7REMAKEPART200
🔊 Audio: inglese, giapponese
📝 Testi: italiano, inglese, spagnolo
🖼️ Copertina: https://image.api.playstation.com/...
```

---

## 📁 Struttura del progetto

```
ps-scraper/
├── scraper.1.1.2.py         # File principale
├── requirements.txt         # Dipendenze
├── README.md
└── ...
```

---

## 🖼️ Screenshot

![Esempio di output](https://placehold.co/600x200/222/fff?text=PS+Scraper+Output)

---

## 🔗 Download versione EXE (Windows)

Puoi usare anche la versione **standalone per Windows**:

📥 [Download scraper.exe](https://github.com/DotHack88/ps-scraper/releases/download/v1.0.0/scraper.exe)

---

## 💡 Suggerimenti

- Modifica le funzioni `search_generic`, `fetch_game_info`, `mostra_nuovi_giochi` per adattare il tool a nuovi bisogni
- Esporta i dati in Excel o inviali via Telegram
- Consulta il codice sorgente per creare bot o report automatici

---

## 🤝 Contribuisci

Contributi, segnalazioni di bug e suggerimenti sono benvenuti!  
Apri una issue o una pull request per partecipare allo sviluppo.

---

## 📄 Licenza

### ⚠️ Licenza

Questo progetto è protetto da copyright.  
**Tutti i diritti riservati.**  
Non è consentito copiare, modificare, distribuire o utilizzare il codice, in tutto o in parte, senza il consenso scritto dell’autore e senza il pagamento di un compenso economico.

---

> Made with ❤️ by DotHack88