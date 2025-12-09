import streamlit as st
import pandas as pd
import geopandas as gpd
import json
import os
from sqlalchemy import create_engine
import streamlit.components.v1 as components

# Caricamento dei dati
engine = create_engine("postgresql://admin:admin123@localhost:5432/DozzaDB")
query = "SELECT * FROM presences;"
df = pd.read_sql(query, engine)
df["data_analisi"] = pd.to_datetime(df["data_analisi"])

# sezionamento ACE notte precedente
df["COD_REG"] = df["ace_notte_precedente"].str[0:3]
df["COD_PROV"] = df["ace_notte_precedente"].str[3:6]
df["COD_COM"] = df["ace_notte_precedente"].str[6:9]
df["PRO_COM_T"] = df["COD_PROV"] + df["COD_COM"]

# sezionamento ACE notte successiva
df["COD_REG_S"] = df["ace_notte_successiva"].str[0:3]
df["COD_PROV_S"] = df["ace_notte_successiva"].str[3:6]
df["COD_COM_S"] = df["ace_notte_successiva"].str[6:9]
df["PRO_COM_T_S"] = df["COD_PROV_S"] + df["COD_COM_S"]

# caricamento e standardizzazione dati shapefile
gdf_comuni = gpd.read_file("raw_data/Limiti01012025_g/Com01012025_g/Com01012025_g_WGS84.shp")
for col in ["COD_REG", "COD_PROV", "PRO_COM_T"]:
    if col in gdf_comuni.columns:
        gdf_comuni[col] = gdf_comuni[col].astype(str).str.zfill(6 if col == "PRO_COM_T" else 3)
gdf_comuni = gdf_comuni.to_crs(epsg=4326)
gdf_comuni["geometry"] = gdf_comuni["geometry"].simplify(tolerance=0.001)
gdf_comuni.to_file("comuni_simplified.geojson", driver="GeoJSON")
gdf_comuni = gpd.read_file("comuni_simplified.geojson")

# Preparazione e utilizzo della sidebar
st.sidebar.header("Filtri")

date_min = df["data_analisi"].min()
date_max = df["data_analisi"].max()
date_range = st.sidebar.date_input(
    "Seleziona intervallo date",
    [date_min, date_max],
    min_value=date_min,
    max_value=date_max
)

classi = ["Tutte"] + sorted(df["classe"].dropna().unique().tolist())
classe_sel = st.sidebar.selectbox("Seleziona classe", classi)

# Filtri per il dataframe e conteggi
if isinstance(date_range, list) or isinstance(date_range, tuple):
    d_start, d_end = pd.to_datetime(date_range)
else:
    d_start = d_end = pd.to_datetime(date_range)

df_filt = df[(df["data_analisi"] >= d_start) & (df["data_analisi"] <= d_end)]
if classe_sel != "Tutte":
    df_filt = df_filt[df_filt["classe"] == classe_sel]

count_comuni_precedente = df_filt.groupby("PRO_COM_T").size().reset_index(name="count_precedente")
count_comuni_successiva = df_filt.groupby("PRO_COM_T_S").size().reset_index(name="count_successiva")

gdf_count_precedente = gdf_comuni.merge(count_comuni_precedente, on="PRO_COM_T", how="left")

# Elimina geometria prima del merge per non sovrascrivere
gdf_count_successiva = gdf_comuni.merge(count_comuni_successiva, left_on="PRO_COM_T", right_on="PRO_COM_T_S", how="left")
gdf_count_successiva = gdf_count_successiva.drop(columns="geometry")

# Merge mantenendo solo la geometria del primo
gdf_count = gdf_count_precedente.merge(
    gdf_count_successiva[["PRO_COM_T", "count_successiva"]],
    on="PRO_COM_T", how="left"
)

gdf_count = gdf_count.fillna({"count_precedente": 0, "count_successiva": 0})

geojson_data = gdf_count.to_json()

# Costruzione della mappa
html = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>
  <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
</head>
<body style="margin:0; padding:0;">
<div id="map" style="width:100%; height:100vh;"></div>
<script>
var map = L.map('map').setView([42.5, 12.5], 6);
L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{maxZoom:19, attribution:'© OpenStreetMap'}}).addTo(map);

var geojson = {geojson_data};
maxCount = Math.max(...geojson.features.map(f => ((f.properties.count_precedente + f.properties.count_successiva)/2)));

function getColor(d) {{
    if(d === 0) return '#FFFFFF';
    var ratio = d / maxCount;
    if(ratio > 0.8) return '#800026';
    else if(ratio > 0.6) return '#BD0026';
    else if(ratio > 0.4) return '#E31A1C';
    else if(ratio > 0.2) return '#FC4E2A';
    else return '#FD8D3C';
}}

function style(feature) {{
    return {{
        fillColor: getColor((feature.properties.count_precedente + feature.properties.count_successiva)/2),
        weight: 0.5,
        opacity: 1,
        color: 'black',
        fillOpacity: 0.7
    }};
}}

function onEachFeature(feature, layer) {{
    var count_precedente = feature.properties.count_precedente ?? 0;
    var count_successiva = feature.properties.count_successiva ?? 0;
    layer.bindPopup("<b>Comune:</b> " + feature.properties.COMUNE +
        "<br><b>Rilevazioni notte precedente:</b> " + count_precedente +
        "<br><b>Rilevazioni notte successiva:</b> " + count_successiva);
}}

L.geoJson(geojson, {{
    style: style,
    onEachFeature: onEachFeature
}}).addTo(map);

</script>
</body>
</html>
"""

# Mostra la mappa
components.html(html, height=900, scrolling=True)