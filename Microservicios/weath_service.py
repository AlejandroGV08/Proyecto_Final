from fastapi import FastAPI, HTTPException, Depends
import requests
import os
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer

# Configuración
SECRET_KEY = "990823"
ALGORITHM = "HS256"
OPENWEATHER_API_KEY = "105dded23f4d99400b18fdbacdaf891b"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

# Verificación de token JWT
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=403, detail="Token inválido")

@app.get("/clima/{ciudad}")
def obtener_clima(ciudad: str, usuario: str = Depends(verify_token)):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")

    data = response.json()
    return {
        "ciudad": ciudad,
        "temperatura": data["main"]["temp"],
        "humedad": data["main"]["humidity"],
        "descripcion": data["weather"][0]["description"]
    }
