from fastapi import FastAPI, HTTPException
import matplotlib.pyplot as plt
import io
import base64
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelo de datos esperado
class ClimaData(BaseModel):
    ciudades: List[str]
    temperaturas: List[float]

@app.post("/graficar/")
def generar_grafico(data: ClimaData):
    if len(data.ciudades) != len(data.temperaturas):
        raise HTTPException(status_code=400, detail="Los datos no coinciden")

    plt.figure(figsize=(8, 5))
    plt.bar(data.ciudades, data.temperaturas, color="skyblue")
    plt.xlabel("Ciudades")
    plt.ylabel("Temperatura (°C)")
    plt.title("Temperatura por Ciudad")

    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plt.close()

    return {"grafico_base64": base64.b64encode(img.getvalue()).decode()}
