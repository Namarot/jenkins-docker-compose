from fastapi import FastAPI, HTTPException
import random

def percentile_true(percentile):
    return random.random() < percentile / 100.0

app = FastAPI()

@app.get("/")
def hello_world():
    roll = random.random() * 100
    if roll < 4:
        raise HTTPException(status_code=500, detail="[500] Internal Server Error")
    elif 4 <= roll < 8:
        raise HTTPException(status_code=400, detail="[400] Bad Request")
    elif 8 <= roll < 12:
        raise HTTPException(status_code=404, detail="[404] Not Found")
    
    return {"message": "[200] OK"}
