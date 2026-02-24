from flask import Flask, jsonify, render_template
import requests
from datetime import datetime

app = Flask(__name__)

# ----------------------
# FUENTES DE DATOS
# ----------------------

SSN_URL = "https://www.ssn.unam.mx/rss.xml"
IRIS_URL = "https://service.iris.edu/fdsnws/event/1/query?format=geojson&limit=5"
JMA_URL = "https://www.jma.go.jp/bosai/quake/data/list.json"

# ----------------------
# UTILIDADES
# ----------------------

def get_iris():
    try:
        r = requests.get(IRIS_URL, timeout=5).json()
        data = []
        for f in r["features"]:
            p = f["properties"]
            c = f["geometry"]["coordinates"]
            data.append({
                "fuente": "IRIS",
                "magnitud": round(p["mag"], 1),
                "lugar": p["place"],
                "tiempo": datetime.utcfromtimestamp(p["time"]/1000).isoformat(),
                "lat": c[1],
                "lon": c[0]
            })
        return data
    except:
        return []

def get_jma():
    try:
        r = requests.get(JMA_URL, timeout=5).json()
        data = []
        for e in r[:5]:
            data.append({
                "fuente": "JMA",
                "magnitud": e.get("mag", 0),
                "lugar": e.get("hypo", "Japón"),
                "tiempo": e.get("time", ""),
                "lat": e.get("lat", 0),
                "lon": e.get("lon", 0)
            })
        return data
    except:
        return []

# ----------------------
# API PRINCIPAL
# ----------------------

@app.route("/api/sismos")
def sismos():
    data = []
    data += get_iris()
    data += get_jma()
    return jsonify(data)

# ----------------------
# SIMULACRO FAKE
# ----------------------

@app.route("/api/simulacro")
def simulacro():
    return jsonify({
        "fuente": "SIMULACRO",
        "magnitud": 7.9,
        "lugar": "Ciudad de México (SIMULADO)",
        "tiempo": datetime.utcnow().isoformat(),
        "lat": 19.4326,
        "lon": -99.1332,
        "alerta": True
    })

# ----------------------
# FRONTEND
# ----------------------

@app.route("/")
def home():
    return render_template("index.html")

# ----------------------
# MAIN
# ----------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
