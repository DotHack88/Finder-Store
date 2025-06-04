# Python Scraper App

Questo progetto è un programma di scraping progettato per estrarre informazioni dai link del PlayStation Store basati sul nome del gioco fornito, "EP0700-PPSA25381_00-ERSL000000000000".

## Struttura del Progetto

Il progetto è organizzato come segue:

```
python-scraper-app
├── src
│   ├── scraper.py         # Contiene la logica principale per il programma di scraping.
│   ├── utils
│   │   └── __init__.py    # Funzioni di utilità per supportare il processo di scraping.
│   └── config
│       └── settings.py    # Impostazioni di configurazione per il progetto.
├── requirements.txt        # Elenco delle dipendenze necessarie per il progetto.
└── README.md               # Documentazione del progetto.
```

## Installazione

Per installare le dipendenze necessarie, eseguire il seguente comando:

```
pip install -r requirements.txt
```

## Esecuzione

Per eseguire il programma di scraping, utilizzare il seguente comando:

```
python src/scraper.py
```

## Dettagli sul Funzionamento

Il programma invia richieste HTTP ai vari link del PlayStation Store e estrae informazioni basate sul nome del gioco fornito. Assicurati di avere una connessione a Internet attiva e di rispettare i termini di servizio del sito web da cui stai estraendo i dati.

## Contributi

Se desideri contribuire a questo progetto, sentiti libero di aprire una pull request o segnalare problemi.