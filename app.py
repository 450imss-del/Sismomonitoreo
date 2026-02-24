from flask import Flask, jsonify, render_template
from flask_cors import CORS
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)

API_IRIS = "https://service.iris.edu/fdsnws/event/1/query?format=geojson&limit=5"
API_USGS = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"

# Endpoint principal de sismos
@app.route("/api/sismos")
def api_sismos():
    data = []
    # USGS
    try:
        r = requests.get(API_USGS, timeout=5).json()
        for f in r["features"][:5]:
            p = f["properties"]
            c = f["geometry"]["coordinates"]
            data.append({
                "fuente": "USGS",
                "magnitud": p.get("mag", 0),
                "lugar": p.get("place", "Desconocido"),
                "tiempo": datetime.utcfromtimestamp(p["time"]/1000).isoformat(),
                "lat": c[1],
                "lon": c[0]
            })
    except:
        pass
    # IRIS
    try:
        r = requests.get(API_IRIS, timeout=5).json()
        for f in r["features"]:
            p = f["properties"]
            c = f["geometry"]["coordinates"]
            data.append({
                "fuente": "IRIS",
                "magnitud": round(p.get("mag",0),1),
                "lugar": p.get("place","Desconocido"),
                "tiempo": datetime.utcfromtimestamp(p["time"]/1000).isoformat(),
                "lat": c[1],
                "lon": c[0]
            })
    except:
        pass
    return jsonify(data)

# Simulacro
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

# Servir HTML directamente desde Flask
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
