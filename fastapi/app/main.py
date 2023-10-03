from fastapi import FastAPI, HTTPException
import random

def percentile_true(percentile):
    return random.random() < percentile / 100.0

app = FastAPI()

@app.get("/")
def hello_world():
    roll = random.random() * 100
    if roll < 20:
        raise HTTPException(status_code=500, detail="[500] Internal Server Error")
    elif 20 <= roll < 40:
        raise HTTPException(status_code=400, detail="[400] Bad Request")
    elif 40 <= roll < 60:
        raise HTTPException(status_code=404, detail="[404] Not Found")
    
    return {"message": "[200] OK"}

    # useful comment :(
