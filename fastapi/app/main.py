from fastapi import FastAPI, HTTPException
import random

def percentile_true(percentile):
    return random.random() < percentile / 100.0

app = FastAPI()

@app.get("/")
def hello_world():
    roll = random.random() * 100
    if roll < 5:
        raise HTTPException(status_code=500, detail="[500] Internal Server Error")
    elif 5 <= roll < 10:
        raise HTTPException(status_code=400, detail="[400] Bad Request")
    elif 10 <= roll < 15:
        raise HTTPException(status_code=404, detail="[404] Not Found")
    
    return {"message": "[200] OK"}
