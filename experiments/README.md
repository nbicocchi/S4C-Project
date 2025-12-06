# 📍 Mobility Forecasting Project – Emilia Romagna (Italy)

## 📁 Struttura del progetto

| Cartella | Descrizione |
|---------|-------------|
| `data_analysis_and_cleansing/` | Script Python per la pulizia e caricamento su PostgreSQL (`data_cleansing1.py`, `data_cleansing2.py`) e analisi dei dati aggregati (`data_analysis_province.ipynb`, `data_analysis_ACE.ipynb`). |
|`EventDetection/`| Sviluppo di algoritmo z-score per rilevazione anomalie nel traffico (`EventDetectionProvincia.ipynb`, `EventDetectionSingleACE.ipynb`) e analisi delle presenze per rilevazione eventi (`presence_Analysis.ipynb`). |
| `experiments_on_single_ACE/` | Analisi dettagliata su singole aree ACE. Contiene: <br>• `ACE_in-out.ipynb`: analisi degli spostamenti in entrata/uscita da un singolo ACE. <br>• `ACE_in-out_CATEGORIES.ipynb`: analisi con suddivisione demografica (età, sesso, ecc). <br>• `Dozza_Analisys/`: approfondimento sull’area di Dozza con analisi specifiche. |
|`flowOD/`| Script per la visualizzazione dei flussi di spostamento (`Flussi.ipynb`, `Flussi_interni_citta.ipynb`, `Flussi_verso_citta.ipynb`) e risultati (`mappageneraleARCHI.html`, `mappageneraleLINEE.html`). |
| `GradientBoosting/` | Sviluppo modello Gradient Boosting Regressor per la predizione di persone in ingresso in un singolo ACE utilizzando due approcci: `Dozza/onlyDozza/Regression_compare.ipynb` dove il modello è allenato con i soli dati dell'ACE e `Dozza/fullDataset/Regression_toid_singleACE.ipynb` dove il modello viene allenato con anche i dati degli altri ACE. Infine `Generalization/BestFeature_all.ipynb` dove il modello del primo approccio viene applicato a tutti gli ACE e vengono confrontati tre set di feature. |
| `mobility_api/` | API sviluppata con **FastAPI** per esporre il modello predittivo. Contiene: <br>• `main.py`: definizione dell'endpoint `/predict` che riceve `date` e `layerid` e restituisce la previsione. <br>• `mobility_model.pkl`, `label_encoder.pkl`, `scaler.pkl`: oggetti salvati del modello e preprocessori. <br>• `requirements.txt`: librerie richieste per l’esecuzione dell’API. Inoltre, contiene `model/Regressions_toid.ipynb` il modello utilizzato per l'API. |
| `regressions/` | Notebook per regressioni: `Regressions_layerid.ipynb` (numero di persone che lasciano un ACE in una certa data), `Regressions_toid.ipynb` (numero di persone che entrano in un ACE in una certa data), `Regressions_ACE.ipynb` (numero di persone che lasciano un ACE per entrare in un altro ACE), `Regressions_province.ipynb` (numero di persone che lasciano una provincia per entare in un altra provincia). Include test con Random Forest, KNN, Gradient Boosting. |
| `visualization/` | Mappa interattiva della mobilità (Folium) nel file `Folium_visualization.ipynb`. Rappresentazione dei flussi in partenza/arrivo per area geografica. Strumento per visualizzazione singolo ACE nel file `ACE_visualization.ipynb`. |

## 🧪 Dataset

- **Fonte**: TIM Enterprise – dati agosto/settembre 2019.
- **Contenuti**: Spostamenti tra aree (layerid → toid), dati demografici, motivi di spostamento, coordinate GeoJSON.
- **Importazione**: I CSV vengono puliti e caricati su database PostgreSQL.

## 📊 Modelli e Tecniche

- **Modelli usati**: Random Forest, K-Nearest Neighbors (KNN), Gradient Boosting.
- **Feature**: Data, giorno della settimana, weekend, etc.
- **Valutazione**: MAE, MAPE.
- **Output multi-target**: Previsioni su sesso, età, nazionalità e motivo dello spostamento.

## 📌 Risultati principali

- Visualizzazione efficace tramite Folium e dei flussi.
- Corrispondenza tra anomalie rilevate ed eventi reali.
- Gradient Boosting ha fornito i migliori risultati in termini di MAPE.
- Utilizzando i solo dati dell'ACE il risultato migliore è stato MAPE 8.107% con le feature date e festivo, mentre utilizzando intero dataset si è arrivati a MAPE 8.041% con le feature: date, weekday, week, festivo, month.
- Generalizzando il modello del primo approccio su tutti gli ACE e confrontando tre set di feature:
   - set1 : date, weekday, weekend, week con MAPE 9.92% 
   - set2 : date, festivo, month con MAPE 12.08% 
   - set3 : date, lag_1, lag_2, lag_3, lag_7 con MAPE 12.47%
- Il modello utilizzato per l'API, dove i dati sono stati divisi considerando il 70%
dei giorni per l’addestramento e il restante 30% per il test, utilizzando come feature:
date, toid, weekday, week e weekend, questo ha portato a un MAE di 969 e un MAPE 8.92%.
