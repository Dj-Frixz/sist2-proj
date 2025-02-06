# La dieta influisce sulla salute?

In questa breve analisi esplorativa di dati dal mondo provo a capire se quanto la dieta influisce 
sulla salute delle persone e sulla longevità, attraverso alcune analisi interessanti ma anche alcuni 
errori di valutazione, e provo a ragionare sui risultati.

# Strumenti utilizzati

Il linguaggio utilizzato è Python 3.13, con l'utilizzo di uv per la gestione delle dipendenze,
e di tre librerie: streamlit, polars e altair.

# Preprocessing dei dati

Per i dati provenienti da Ourworldindata.org non è servita pulizia, solo rinominare qualche colonna.
Con l'eccezione però dei dati sulla dieta, dove ho dovuto fare un 'unpivot' delle colonne in modo da avere il formato lungo dei dati, ideale per la visualizzazione grafica. In più ho abbreviato i nomi delle varie categorie.

Invece per i dati sulla popolazione, provenienti da Gapminder, è stato molto più laborioso: i numeri erano scritti con le lettere, ad esempio '1M' al posto di 1000000, e gli Stati Uniti e il Regno Unito erano abbreviati. Per questi ultimi è bastato cambiare il nome. Per i numeri invece ho dovuto usare delle regex per modificare le lettere con la corrispondente notazione esponenziale, per esempio cambiando 'k' con 'e3', e poi facendo una conversione delle stringa in float64.